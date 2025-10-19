from django.db import models

class CheckupStatus(models.TextChoices):
    Pending = "pending", "Ожидание"
    In_progress = "in_progress", "В процессе"
    Completed = "completed", "Завершено"
    Error = "error", "Ошибка"
    Cancelled = "cancelled", "Отменено"


class ObjectType(models.TextChoices):
    TREE = "tree", "Tree"
    SHRUB = "shrub", "Shrub"


class Breed(models.TextChoices):
    UNKNOWN = "unknown", "Не определено"
    OAK = "oak", "Дуб"
    ASH = "ash", "Ясень"
    POPLAR = "poplar", "Тополь"
    PINE = "pine", "Сосна"
    BIRCH = "birch", "Берёза"
    ELM = "elm", "Вяз"
    MAPLE = "maple", "Клён"
    SPRUCE = "spruce", "Ель"
    CATALPA = "catalpa", "Катальпа"
    WILLOW = "willow", "Ива"
    LINDEN = "linden", "Липа"
    ACACIA = "acacia", "Акация"
    ASPEN = "aspen", "Осина"
    CHESTNUT = "chestnut", "Каштан"
    APPLE = "apple", "Яблоня"
    CHERRY = "cherry", "Вишня"
    # ель
    # катальпа
    # ива
    # липа
    # акация
    # осина
    # рябина

class Condition(models.TextChoices):
    NORMAL = "normal", "Нормальное"
    FALLING = "falling", "Заваливающееся"
    FALLEN = "fallen", "Упавшее"
    EMERGENCY = "emergency", "Аварийное"
    UNSATISFACTORY = "unsatisfactory", "Не удовлетворительное"
    STUMP = "stump", "Пенёк"


class Season(models.TextChoices):
    VEGETATIVE = "vegetative", "Вегетативный"
    NON_VEGETATIVE = "non_vegetative", "Не вегетативный"


class Artifact(models.TextChoices):
    CRACK = "crack", "Трещина"
    HOLLOW = "hollow", "Дупло"
    BARK_REMOVED = "bark_removed", "Содранная кора"
    ROOTS_EXPOSED = "roots_exposed", "Обнажены корни"
    FUNGI = "fungi", "Грибы"
    ROT = "rot", "Гниль"
    STEM_DAMAGE = "stem_damage", "Повреждение ствола"
    CROWN_DAMAGE = "crown_damage", "Повреждение кроны"
    BROKEN_BRANCHES = "broken_branches", "Обломанные ветки"
    BROKEN_TRUNK = "broken_trunk", "Сломанный ствол"


RUS_TO_ENUM = {
    "дерево": ObjectType.TREE,
    "кустарник": ObjectType.SHRUB,
    "дуб": Breed.OAK,
    "ясень": Breed.ASH,
    "тополь": Breed.POPLAR,
    "сосна": Breed.PINE,
    "берёза": Breed.BIRCH,
    "вяз": Breed.ELM,
    "клён": Breed.MAPLE,
    "ель": Breed.SPRUCE,
    "не определено": Breed.UNKNOWN,
    "катальпа": Breed.CATALPA,
    "ива": Breed.WILLOW,
    "липа": Breed.LINDEN,
    "акация": Breed.ACACIA,
    "осина": Breed.ASPEN,
    "каштан": Breed.CHESTNUT,
    "яблоня": Breed.APPLE,
    "вишня": Breed.CHERRY,

    "нормальное": Condition.NORMAL,
    "заваливающееся": Condition.FALLING,
    "упавшее": Condition.FALLEN,
    "аварийное": Condition.EMERGENCY,
    "не удовлетворительное": Condition.UNSATISFACTORY,
    "пенёк": Condition.STUMP,

    "вегетативный": Season.VEGETATIVE,
    "не вегетативный": Season.NON_VEGETATIVE,
    "трещина": Artifact.CRACK,
    "дупло": Artifact.HOLLOW,
    "содранная кора": Artifact.BARK_REMOVED,
    "обнажены корни": Artifact.ROOTS_EXPOSED,
    "грибы": Artifact.FUNGI,
    "гниль": Artifact.ROT,
    "повреждение ствола": Artifact.STEM_DAMAGE,
    "повреждение кроны": Artifact.CROWN_DAMAGE,
    "обломанные ветки": Artifact.BROKEN_BRANCHES,
    "сломанный ствол": Artifact.BROKEN_TRUNK,
}