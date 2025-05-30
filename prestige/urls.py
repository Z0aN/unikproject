from django.contrib import admin
from django.urls import path, include  # подключаем include

urlpatterns = [
    path('admin/', admin.site.urls),         # путь к админке
    path('', include('rental.urls')),        # путь к твоему сайту (главной)
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
