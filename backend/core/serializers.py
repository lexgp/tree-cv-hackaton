from rest_framework import serializers
from easy_thumbnails.files import get_thumbnailer

from django.db.models import Count
from collections import Counter

from .models import Checkup, CheckupPhoto, CheckupPhotoAnnotation, DistrictArea
from .choices import (
    RUS_TO_ENUM,
    Condition,
)
# Реверс-маппинг: из EN -> RU
ENUM_TO_RUS = {v: k for k, v in RUS_TO_ENUM.items()}


class CheckupPhotoAnnotationSerializer(serializers.ModelSerializer):

    annotated_photo = serializers.SerializerMethodField()

    @staticmethod
    def get_annotated_photo(obj):
        crop_options = {'size': (250, 250), 'crop': 'scale'}
        try:
            return get_thumbnailer(obj.annotated_photo).get_thumbnail(crop_options).url
        except Exception as e:
            pass

    class Meta:
        model = CheckupPhotoAnnotation
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # заменяем на русский
        for field in ["object_type", "breed", "condition", "season"]:
            if data.get(field):
                data[field] = ENUM_TO_RUS.get(data[field], data[field])

        if data.get("artifacts"):
            data["artifacts"] = [ENUM_TO_RUS.get(a, a) for a in data["artifacts"]]

        return data

    def to_internal_value(self, data):
        """
        Поддержка входа с русскими значениями
        """
        new_data = data.copy()

        for field in ["object_type", "breed", "condition", "season"]:
            if field in new_data and new_data[field] in RUS_TO_ENUM:
                new_data[field] = RUS_TO_ENUM[new_data[field]]

        if "artifacts" in new_data:
            new_data["artifacts"] = [
                RUS_TO_ENUM.get(a, a) for a in new_data["artifacts"]
            ]

        return super().to_internal_value(new_data)

class CheckupPhotoSerializer(serializers.ModelSerializer):
    annotation = CheckupPhotoAnnotationSerializer(many=False, read_only=True)
    preview = serializers.SerializerMethodField()

    class Meta:
        model = CheckupPhoto
        fields = "__all__"

    def validate_photo(self, value):
        max_size = 10 * 1024 * 1024  # 10 MB
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']

        if value.size > max_size:
            raise serializers.ValidationError("Размер файла превышает 10 MB.")

        if hasattr(value, "content_type") and value.content_type not in allowed_types:
            raise serializers.ValidationError("Недопустимый тип файла. Разрешены JPG, JPEG, PNG, GIF.")

        return value

    @staticmethod
    def get_preview(obj):
        crop_options = {'size': (450, 450), 'crop': 'scale'}
        try:
            return get_thumbnailer(obj.photo).get_thumbnail(crop_options).url
        except Exception as e:
            pass


class DistrictAreaSerializer(serializers.ModelSerializer):

    last_checkup_date = serializers.SerializerMethodField()

    def get_last_checkup_date(self, obj: DistrictArea):
        # Берём последний Checkup по report_date
        last_checkup = Checkup.objects.filter(area=obj).order_by('-report_date').first()
        return last_checkup.report_date if last_checkup else None
        
    class Meta:
        model = DistrictArea
        fields = "__all__"

def trees_condition_statistic(trees):
    # Считаем количество по каждому condition
    counts = trees.values('condition').annotate(count=Count('id'))
    condition_count_map = {c['condition']: c['count'] for c in counts}

    categories = [
        {
            'key': 'normal',
            'color': 'success',
            'title': 'Здоровые',
            'conditions': [Condition.NORMAL],
            'count': 0,
            'rate': 0,
        },
        {
            'key': 'damaged',
            'color': 'warning',
            'title': 'Повреждены',
            'conditions': [Condition.FALLING, Condition.UNSATISFACTORY, Condition.STUMP],
            'count': 0,
            'rate': 0,
        },
        {
            'key': 'critial',
            'color': 'error',
            'title': 'Критично',
            'conditions': [Condition.FALLEN, Condition.EMERGENCY],
            'count': 0,
            'rate': 0,
        },
        {
            'key': 'total',
            'color': 'primary',
            'title': 'Всего деревьев',
            'conditions': [key for key, _ in Condition.choices],
            'count': 0,
            'rate': 0,
        },
    ]

    total_trees = len(trees)

    for cat in categories:
        cat_count = sum(condition_count_map.get(cond, 0) for cond in cat['conditions'])
        cat['count'] = cat_count
        cat['rate'] = round(cat_count / total_trees * 100, 1) if total_trees else 0

    return categories



class DistrictAreaDetailSerializer(DistrictAreaSerializer):

    condition_statistic = serializers.SerializerMethodField()
    artifacts_statistic = serializers.SerializerMethodField()
    
    def get_condition_statistic(self, obj):
        trees = CheckupPhotoAnnotation.objects.filter(
            photo__checkup__area=obj,
            is_tree_finded=True
        )

        return trees_condition_statistic(trees)

    def get_artifacts_statistic(self, obj):
        # Берём все массивы artifacts
        artifacts_qs = CheckupPhotoAnnotation.objects.filter(
            photo__checkup__area=obj,
            is_tree_finded=True
        ).values_list('artifacts', flat=True)

        # Для обратного поиска: ENUM -> название
        ENUM_TO_RUS = {v: k for k, v in RUS_TO_ENUM.items()}

        # Склеиваем все списки в один
        all_artifacts = []
        for arr in artifacts_qs:
            all_artifacts.extend(arr)

        # Считаем частоту каждого артефакта
        counter = Counter(all_artifacts)

        # Топ-5
        top5 = counter.most_common(5)

        # Форматируем результат: [{'title': '...', 'count': n}, ...]
        result = [{'title': ENUM_TO_RUS[t[0]], 'count': t[1]} for t in top5]

        return result

    class Meta:
        model = DistrictArea
        fields = "__all__"


class CheckupSerializer(serializers.ModelSerializer):

    photos = CheckupPhotoSerializer(many=True, read_only=True)
    area_detail = DistrictAreaSerializer(source='area', read_only=True)

    class Meta:
        model = Checkup
        fields = "__all__"


class CheckupDetailSerializer(CheckupSerializer):

    condition_statistic = serializers.SerializerMethodField()

    def get_condition_statistic(self, obj):
        trees = CheckupPhotoAnnotation.objects.filter(
            photo__checkup=obj,
            is_tree_finded=True
        )

        return trees_condition_statistic(trees)

    class Meta:
        model = Checkup
        fields = "__all__"


class CheckupPrototypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkup
        fields = "__all__"
