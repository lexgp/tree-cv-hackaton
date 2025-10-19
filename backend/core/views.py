import json
from django.db.models import Q
from django.db.models import F
from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from core import serializers as core_serializers

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from core.paginators import StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from .models import Checkup, CheckupPhoto, CheckupPhotoAnnotation, DistrictArea
from .serializers import (
    CheckupSerializer,
    CheckupDetailSerializer,
    CheckupPhotoSerializer,
    CheckupPrototypeSerializer,
    DistrictAreaSerializer,
    DistrictAreaDetailSerializer,
)

from core.choices import ObjectType, Breed, Condition, Season, Artifact, CheckupStatus, RUS_TO_ENUM
import core.utils.image_utils as image_utils
import core.service.yolo as yolo_service
from core.service.prompts_choices import PromptOptions
from core.service.llmtunnel_provider import LLMProvider
from django.conf import settings

from core.utils.annotator import annotate_photo

class CheckupViewSet(ModelViewSet):
    queryset = Checkup.objects.all().order_by("-id")
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CheckupDetailSerializer
        return CheckupSerializer


    @action(detail=False, methods=["get"])
    def prototype(self, request):
        """
        Вернёт пустой Checkup (пример структуры для фронта)
        """
        serializer = CheckupPrototypeSerializer(Checkup(
            report_date=timezone.now().date(),
            area=DistrictArea.objects.first()
        ))
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
        responses={
            200: CheckupSerializer,
            400: openapi.Response(description="Bad Request"),
        }
    )
    @action(detail=True, methods=["post"])
    def finish(self, request, pk=None):
        """
        Завершает обследование.
        """

        provider = LLMProvider(
            settings.PROVIDER_SECRET_KEY,
            settings.PROVIDER_URL,
            settings.PROVIDER_SUBMODEL,
        )

        checkup = Checkup.objects.get(pk=pk)
        for photo in checkup.photos.all():
            # Породы надо на ЙОЛЛУ переделать

            IMAGE_SIZE = 1024
            image = image_utils.get_image(photo.photo)

            # ???: может не стоит добавлять паддинги при ресайзе? Наверное всё таки стоит, йола лучше отрабатывает при стандартизации. Вроде бы.
            resized_image = image_utils.resize_to_square(image, IMAGE_SIZE)

            angle = provider.predict(PromptOptions.PHOTO_ANGLE.value, resized_image, submodel='llama-4-maverick')
            if angle and isinstance(angle['angle'], int) and angle['angle']:
                resized_image = image_utils.rotate_image_90(resized_image, 360 - angle['angle'])
            
            results = yolo_service.analyze_plant_image(resized_image, '../mlmodels_store/yolo-segmentation build 2.8.pt')
            bboxes = yolo_service.get_prediction_boxes(results)

            tree = None
            if bboxes:
                primary_bbox = yolo_service.select_primary_object(bboxes, resized_image.size)
                if primary_bbox:
                    cropped_img = yolo_service.crop_with_padding(resized_image, primary_bbox, padding_ratio=0.1)
                    tree = provider.predict(PromptOptions.MAIN.value, cropped_img, submodel='llama-4-maverick')

            if not hasattr(photo, 'annotation'):
                photo.annotation = CheckupPhotoAnnotation.objects.create(photo=photo)
            
            if tree:
                llm_models = ['llama-4-maverick', 'gemini-2.5-flash', 'llama-4-scout']
                for llm_model in llm_models:
                    breed_data = provider.predict(PromptOptions.GET_BREED.value, cropped_img, submodel=llm_model)
                    print('breed_data', breed_data, llm_model)
                    breed = 'не определено'
                    if breed_data and breed_data['breed'] and breed_data['breed']!='не определено':
                        breed = breed_data['breed']
                        break

                photo.annotation.object_type = RUS_TO_ENUM[tree["type"]]
                photo.annotation.breed = RUS_TO_ENUM.get(breed, Breed.UNKNOWN)
                photo.annotation.condition = RUS_TO_ENUM[tree["condition"]]
                photo.annotation.is_dry = tree["is_dry"]
                photo.annotation.percentage_dried = tree["percentage_dried"]
                photo.annotation.artifacts = [RUS_TO_ENUM[a] for a in tree.get("artifacts", [])]
                photo.annotation.description = tree.get("description", "")
                photo.annotation.season = RUS_TO_ENUM.get(tree["season"])
                photo.annotation.is_tree_finded = True
                annotate_photo(photo, primary_bbox, results)
            else:
                photo.annotation.description = 'Деревья не обнаружены'
                photo.annotation.is_tree_finded = False

            photo.annotation.save()

        
        checkup.status = CheckupStatus.Completed
        checkup.save()
        serializer = self.get_serializer(checkup, many=False)
        return Response(serializer.data)


class CheckupPhotoViewSet(ModelViewSet):
    serializer_class = CheckupPhotoSerializer
    http_method_names = ["post", "delete", "get", "patch", "head", "options"]

    def get_queryset(self):
        return CheckupPhoto.objects.all()

    @action(detail=False, methods=["get"], url_path="by-checkup/(?P<checkup_id>[^/.]+)")
    def by_checkup(self, request, checkup_id=None):
        """
        Получить все фото по обследованию
        """
        photos = self.get_queryset().filter(checkup_id=checkup_id)
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='patch',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['coords'],
            properties={
                'coords': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_NUMBER),
                    description='Coordinate: [x, y]'
                ),
            },
        ),
        responses={
            200: CheckupPhotoSerializer,
            400: openapi.Response("Bad Request"),
        },
        operation_description="Обновление координат фото",
    )
    @action(detail=True, methods=["patch"], url_path="update-coords")
    def update_coords(self, request, pk=None):
        instance = self.get_object()
        coords = request.data.get('coords')

        if not coords or not isinstance(coords, list) or len(coords) != 2:
            return Response(
                {"detail": "coords должно быть массивом из 2 чисел"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.coords = coords
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DistrictAreaViewSet(viewsets.ModelViewSet):
    queryset = DistrictArea.objects.all()
    serializer_class = DistrictAreaSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DistrictAreaDetailSerializer
        return DistrictAreaSerializer
