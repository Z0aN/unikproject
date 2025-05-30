from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Кастомный менеджер
class AvailableCarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)

class Service(models.Model):
    name = models.CharField("Название услуги", max_length=100)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField("Название", max_length=100)
    brand = models.CharField("Бренд", max_length=100)
    type = models.CharField("Тип кузова", max_length=50)
    price = models.DecimalField("Цена за сутки", max_digits=10, decimal_places=2)
    is_available = models.BooleanField("Доступна", default=True)

    # Стандартный и кастомный менеджеры
    objects = models.Manager()
    available = AvailableCarManager()

    image = models.ImageField("Фото", upload_to="cars/", blank=True, null=True)

    services = models.ManyToManyField(
        "Service",
        verbose_name="Дополнительные услуги",
        blank=True
    )

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.name}"
    
    def get_absolute_url(self):
        return reverse("car_detail", args=[str(self.id)])

class Booking(models.Model):
    user = models.ForeignKey(User, verbose_name="Клиент", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, verbose_name="Автомобиль", on_delete=models.CASCADE)
    date_from = models.DateField("Дата начала")
    date_to = models.DateField("Дата окончания")
    status = models.CharField("Статус", max_length=20, choices=[
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ])

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"

class maexam(models.Model):
    name = models.CharField("Название экзамена", max_length=200)
    created_at = models.DateTimeField("Дата создания записи", default=timezone.now)
    exam_date = models.DateField("Дата проведения экзамена")
    image = models.ImageField("Изображение задания", upload_to="exams/", blank=True, null=True)
    users = models.ManyToManyField(User, verbose_name="Пользователи, пишущие экзамен")
    is_public = models.BooleanField("Опубликовано", default=False)

    class Meta:
        verbose_name = "Экзамен"
        verbose_name_plural = "Экзамены"

    def __str__(self):
        return self.name