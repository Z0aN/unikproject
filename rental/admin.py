from django.contrib import admin
from .models import Car, Booking, Service
from .models import Maexam

# Регистрация модели "Услуга"
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# Inline-модель: бронирования внутри карточки машины
class BookingInline(admin.TabularInline):  # Можно заменить на StackedInline для вертикального отображения
    model = Booking
    extra = 1  # количество пустых форм для добавления
    raw_id_fields = ("user",)  # избегаем выпадающих списков на 1000+ юзеров

# Админка для автомобиля
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "name", "type", "price", "is_available", "car_display_name")
    list_filter = ("brand", "type", "is_available")
    search_fields = ("name", "brand")
    list_display_links = ("brand", "name")
    readonly_fields = ("id",)
    filter_horizontal = ("services",)  # для выбора ManyToMany услуг
    inlines = [BookingInline]          # показываем связанные бронирования

    @admin.display(description="Модель авто")
    def car_display_name(self, obj):
        return f"{obj.brand} {obj.name}"

# Админка для бронирований
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "car", "date_from", "date_to", "status")
    list_filter = ("status", "date_from")
    date_hierarchy = "date_from"
    search_fields = ("user__username", "car__name")
    raw_id_fields = ("user", "car")  # чтобы не грузить большой список

@admin.register(Maexam)
class MaexamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'users__email')
    list_filter = ('exam_date', 'is_public', 'created_at')
    filter_horizontal = ('users',)
    list_display = ('name', 'exam_date', 'is_public', 'created_at')
    date_hierarchy = 'created_at'
