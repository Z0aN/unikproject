from django.shortcuts import render
from .models import Car
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Count

def home(request):
    per_page = request.GET.get('per_page', 4)
    try:
        per_page = int(per_page)
        if per_page not in [4, 8, 12]:
            per_page = 4
    except ValueError:
        per_page = 4

    car_list = Car.available.all().exclude(price__lt=2000).order_by('price')
    paginator = Paginator(car_list, per_page)
    page = request.GET.get('page')

    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        # Если пользователь ввёл несуществующую страницу — покажем последнюю
        cars = paginator.page(paginator.num_pages)

    car_stats = Car.available.aggregate(
    total=Count('id'),
    avg_price=Avg('price')
    )

    return render(request, 'index.html', {
    'cars': cars,
    'per_page': per_page,
    'car_stats': car_stats
})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car_list = Car.available.exclude(id=car.id).order_by('?')[:3]  # 3 случайных

    return render(request, 'car_detail.html', {
        'car': car,
        'car_list': car_list
    })
