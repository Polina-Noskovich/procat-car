from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from .models import Feedbacks, FAQ, About, News, Contacts, Vac, Sales, Seller, Customer, Car, OrderItem, Order, Fine
import requests
from django.shortcuts import render
from django.utils import timezone
from .forms import RegisterUserForm, LoginUserForm, FeedbackForm, SellerForm, CustomerForm, CarForm, AddSpeciesForm, \
    FilterForm, SearchForm, UpdateOrderItemForm
from django.conf import settings
import matplotlib.pyplot as plt
import mpld3
import numpy as np
from collections import Counter
from statistics import mean, median, mode
import base64
from io import BytesIO


import logging


logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s, %(levelname)s, %(message)s')

from .models import Partner, Article, Banner
from datetime import datetime

from .forms import ContactForm

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)  # Получаем данные из формы (с файлом)
        if form.is_valid():
            form.save()  # Сохраняем в базу данных
            return redirect('contacts')  # Переходим на страницу со списком контактов
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})

# Create your views here.
def about(request):
    abouts = About.objects.all()
    if abouts.exists():
        for about in abouts:
            logging.info(f'company_info: {about.ustext}')
    else:
        logging.warning('не найдено')
    return render(request, 'about.html', {'abouts': abouts})

def anym(request):
    abouts = About.objects.all()
    if abouts.exists():
        for about in abouts:
            logging.info(f'company_info: {about.ustext}')
    else:
        logging.warning('не найдено')
    return render(request, 'anym.html', {'abouts': abouts})


def contacts(request):
    contacts = Contacts.objects.all()
    if contacts.exists():
        for contact in contacts:
            logging.info(f'contact_info: {contact.name}')
    else:
        logging.warning('Контакты не найдены')
    return render(request, 'contacts.html', {'contacts': contacts})


from django.shortcuts import render
from django.http import HttpResponse

def lr3(request): 
    contacts = Contacts.objects.all()
    
    if request.method == 'POST':
        selected_contacts = request.POST.getlist('contact')
        # Логика для обработки выбранных контактов (например, отправка email)
        if selected_contacts:
            # Ваши действия с выбранными контактами
            print(f"Выбраны следующие контакты: {selected_contacts}")
            return HttpResponse("Контакты выбраны и обработаны.")
    
    return render(request, 'lr3.html', {'contacts': contacts})


def feedback(request):
    feedbacks = Feedbacks.objects.all()
    if feedbacks.exists():
        for feedback in feedbacks:
            logging.info(f'feedback_info: {feedback.name}')
    else:
        logging.warning('Отзывы не найдены')
    return render(request, 'feedback.html', {'feedbacks': feedbacks})




from django.shortcuts import render, get_object_or_404

def news_list(request):
    news_items = News.objects.all()
    return render(request, 'news.html', {'news_items': news_items})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})

def news(request):
    news_items = News.objects.all()
    if news_items.exists():
        for news in news_items:
            logging.info(f'news_info: {news.newscrat}')
    else:
        logging.warning('Новости не найдены')
    return render(request, 'news.html', {'news': news_items})


def sales(request):
    sales_items = Sales.objects.all()
    if sales_items.exists():
        for sale in sales_items:
            logging.info(f'sale_info: {sale.code}')
    else:
        logging.warning('Скидки не найдены')
    return render(request, 'sales.html', {'sales': sales_items})


def shtraf(request):
    return render(request, 'shtraf.html')


'''def slovar(request):
    faqs = FAQ.objects.all()
    if faqs.exists():
        for faq in faqs:
            logging.info(f'faq_info: {faq.question}')
    else:
        logging.warning('FAQ не найдено')
    return render(request, 'slovar.html', {'faqs': faqs})'''


def vac(request):
    vacs = Vac.objects.all()
    if vacs.exists():
        for vac in vacs:
            logging.info(f'vac_info: {vac.vac}')
    else:
        logging.warning('Вакансии не найдены')
    return render(request, 'vac.html', {'vacs': vacs})

class BaseViewContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['title'] = kwargs.get('title', 'Default Title')
        return context


def reversex_lazy(param):
    pass

from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect

class RegisterView(BaseViewContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')  # Или любая другая страница, куда ты хочешь перенаправить пользователя после регистрации

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()  # Сохраняем пользователя
        login(self.request, user)  # Выполняем автоматический вход
        return redirect(self.get_success_url())  # Перенаправляем на нужную страницу после входа


from django.contrib.auth import login


class LoginUser(BaseViewContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')  # Перенаправление на главную страницу после выхода

@login_required
def add_feedback(request):
    error = ''
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.name = request.user.username  # Используем имя залогиненного пользователя
            feedback.save()
            return redirect('feedback')  # Перенаправление на страницу отзывов
        else:
            error = 'Некорректное заполнение формы'
    else:
        form = FeedbackForm()

    return render(request, 'add_feedback.html', {'form': form, 'error': error})



from django.shortcuts import render, get_object_or_404
from .models import FAQ

# Список вопросов
def faq_list(request):
    faqs = FAQ.objects.all().order_by('-date_added')
    return render(request, 'faq_list.html', {'faqs': faqs})

# Детальная информация о вопросе
def faq_detail(request, faq_id):
    faq = get_object_or_404(FAQ, pk=faq_id)
    return render(request, 'faq_detail.html', {'faq': faq})



import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from django.shortcuts import render

def foradmin(request):
    # Генерация графиков
    graph_sales = generate_sales_graph()
    graph_age = generate_age_graph()
    graph_popularity = generate_popularity_graph()

    return render(request, 'ProcatCar/foradmin.html', {
        'graph_sales': graph_sales,
        'graph_age': graph_age,
        'graph_popularity': graph_popularity
    })

def generate_sales_graph():
    # Рандомные данные для графика продаж по категориям
    categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
    sales = np.random.randint(100, 1000, size=len(categories))

    plt.figure(figsize=(8, 6))
    plt.bar(categories, sales, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Sales')
    plt.title('Sales by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Кодирование графика в строку base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64

def generate_age_graph():
    # Рандомные данные для графика возраста клиентов
    ages = np.random.randint(18, 70, size=100)

    plt.figure(figsize=(8, 6))
    plt.hist(ages, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.title('Age Distribution of Customers')
    plt.tight_layout()

    # Кодирование графика в строку base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64

def generate_popularity_graph():
    # Рандомные данные для графика популярности товаров
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    popularity = np.random.randint(50, 500, size=len(products))

    plt.figure(figsize=(8, 6))
    plt.bar(products, popularity, color='skyblue')
    plt.xlabel('Products')
    plt.ylabel('Popularity')
    plt.title('Popularity of Products')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Кодирование графика в строку base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64




def customer(request):
    error = ''
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            cust = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Создаем пользователя с полученными данными
            user = User.objects.create_user(username=username, password=password)
            cust.user = user  # Используем имя пользователя текущего пользователя
            cust.save()
            return redirect('index')  # Перенаправляем на список отзывов после успешного добавления
        else:
            error = 'Введите верное значение'
            # Можно также добавить дополнительную обработку ошибок валидации, если нужно
    else:
        form = CustomerForm()
    data = {'error': error, 'form': form}
    return render(request, 'custom.html', data)


def seller(request):
    error = ''
    if request.method == "POST":
        form = SellerForm(request.POST)
        if form.is_valid():
            sell = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Создаем пользователя с полученными данными
            user = User.objects.create_user(username=username, password=password)
            sell.user = user  # Используем имя пользователя текущего пользователя
            sell.save()
            return redirect('index')  # Перенаправляем на список отзывов после успешного добавления
        else:
            error = 'Неверное заполнение'
    form = SellerForm()
    data = {'error': error, 'form': form}
    return render(request, 'sell.html', data)


def get_joke_of_the_day():
    try:
        request = requests.get('https://icanhazdadjoke.com', headers={'Accept': 'application/json'})
        request.raise_for_status()
        response = request.json()
        return response.get('joke', 'No joke available today.')
    except requests.RequestException:
        return 'No joke available today.'

def get_car_fact():
    try:
        fact_url = "https://api.aakhilv.me/fun/facts"
        response = requests.get(fact_url)
        response.raise_for_status()
        facts = response.json()
        return facts[0] if facts else "No car fact available today."
    except requests.RequestException:
        return "No car fact available today."

from .models import CompanyLogo
def index(request):
       # Получение последней статьи из базы данных
    latest_article = Article.objects.first()  # Убедитесь, что это извлечение работает корректно
    # Получение списка партнеров
    partners = Partner.objects.all()  # Убедитесь, что это извлечение работает корректно
    # Получение активных баннеров
    banners = Banner.objects.filter(is_active=True)
    # Получаем логотип компании
    company_logo = CompanyLogo.objects.first()  # Предположим, что у вас только один логотип

    # Текущее время
    now = datetime.now()
    catalog_items = [
        {'name': 'Услуга 1', 'description': 'Описание услуги 1'},
        {'name': 'Товар 1', 'description': 'Описание товара 1'},
        {'name': 'Продукт 1', 'description': 'Описание продукта 1'},
        # Добавьте другие элементы каталога по необходимости
    ]
    company_logo_url = 'pythonProjectPolina/static/images/logo.jpg'  # Замените на реальный путь к логотипу
    banners = Banner.objects.all()
    now = timezone.now()

    # Get cat fact
    try:
        cat_fact_url = "https://catfact.ninja/fact"
        cat_fact_response = requests.get(cat_fact_url)
        cat_fact_response.raise_for_status()
        cat_fact_data = cat_fact_response.json()
        cat_fact = cat_fact_data.get("fact", "No cat fact available today.")
    except requests.RequestException:
        cat_fact = "No cat fact available today."

    # Get cat image
    cat_image_url = "https://cataas.com/cat"

    # Get the latest news
    latest_news = News.objects.order_by('id').first()

    return render(request, "index.html", context={
        'fact': cat_fact,
        'joke': get_joke_of_the_day(),
        'now': now,
        'car_fact': get_car_fact(),
        'cat_image_url': cat_image_url,
        'latest_news': latest_news,
        'latest_article': latest_article,
        'partners': partners,
        'banners': banners,
        'catalog_items': catalog_items,
        'company_logo_url': company_logo_url,
        'company_logo': company_logo,
        # Добавьте другие необходимые контексты
        'now': now
    })





class viewnew(DetailView):
    model = News
    template_name = 'onenew.html'
    context_object_name = 'onenew'  # передаем объект по названию context object name-a - onenew

def car(request):
    car= Car.objects.all
    return render(request, 'car.html', {'car': car})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Car, Sales, Fine

@login_required
def car_list(request):
    cars = Car.objects.all()
    sales = Sales.objects.filter(active=True)
    fines = Fine.objects.filter(user=request.user)

    # Считаем общую скидку и штрафы для текущего пользователя
    total_discount = sum(sale.discount for sale in sales)
    total_fine = sum(fine.amount for fine in fines)

    car_data = []
    for car in cars:
        rent_price = car.daily_rent
        if total_discount:
            rent_price -= total_discount
        if total_fine:
            rent_price += total_fine
        car_data.append({
            'car': car,
            'rent_price': max(rent_price, 0)  # Прократ не может быть отрицательным
        })

    return render(request, 'car_list.html', {'cars': car_data})


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.company = seller  # Убедитесь, что `seller` определен и имеет правильное значение
            car.save()
            return redirect('index') 
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


import logging

logger = logging.getLogger(__name__)
from datetime import timedelta
from decimal import Decimal, getcontext

# Установите точность для Decimal (по умолчанию 28 знаков)
getcontext().prec = 1

@login_required
def add_to_bron(request, car_id):
    logger.info("Handling add_to_bron request")
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        logger.info("Customer does not exist, redirecting to index")
        return redirect('index')
    
    car = Car.objects.get(pk=car_id)
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if not start_date or not end_date:
            logger.info("Dates are missing, rendering add_to_bron with error")
            return render(request, 'add_to_bron.html', {'error': 'Дата начала или окончания не указана'})
        
        try:
            start_date = timezone.datetime.fromisoformat(start_date)
            end_date = timezone.datetime.fromisoformat(end_date)
            if start_date >= end_date:
                raise ValueError("Дата окончания должна быть позже даты начала.")
        except (ValueError, TypeError):
            logger.info("Invalid date format, rendering add_to_bron with error")
            return render(request, 'add_to_bron.html', {'error': 'Неверный формат даты'})
        
        # Рассчитайте стоимость
        duration = end_date - start_date
        if duration <= timedelta(hours=0):
            logger.info("Invalid duration, rendering add_to_bron with error")
            return render(request, 'add_to_bron.html', {'error': 'Продолжительность аренды должна быть положительной'})
        
        duration_hours = Decimal(duration.total_seconds()) / Decimal(3600)  # Изменено на 3600 для часов
        total_cost = car.price * duration_hours
        
        # Примените штрафы
        try:
            fine = Fine.objects.get(user=request.user, car=car)
            total_cost += fine.amount
        except Fine.DoesNotExist:
            pass
        
        # Примените скидки
        active_sales = Sales.objects.filter(active=True)
        for sale in active_sales:
            total_cost -= sale.discount
        
        # Создайте заказ
        order = Order.objects.create(user=request.user)
        order_item = OrderItem.objects.create(count=duration_hours, object=car)
        order.cars.add(order_item)
        
        order.save()  # Сохранение заказа
        
        booking_info = {
            'start_date': start_date,
            'end_date': end_date,
            'total_cost': total_cost
        }
        
        logger.info("Order processed, displaying booking information")
        return render(request, 'add_to_bron.html', {'booking_info': booking_info})
    
    logger.info("Rendering add_to_bron template")
    return render(request, 'add_to_bron.html')



@login_required
def add_mark(request):
    if request.method == 'POST':
        form = AddSpeciesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddSpeciesForm()
    return render(request, 'add_mark.html', {'form': form})

def foradmin(request):
    customers_by_city = Customer.objects.values('city')
    mebel_with_highest_demand = Car.objects.annotate(total_sales=Sum('price')).order_by('-total_sales').first()
    return render(request, 'foradmin.html', {'_with_highest_demand': mebel_with_highest_demand,'customers_by_city':customers_by_city})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal

from decimal import Decimal, ROUND_DOWN

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('cars__object')
    order_details = []

    for order in orders:
        # Расчёт стоимости заказа
        base_cost = Decimal('0.00')
        fine_amount = Decimal('0.00')
        discount = Decimal('0.00')

        for order_item in order.cars.all():
            car = order_item.object
            duration_hours = Decimal(order_item.count) / Decimal(3600)  # Изменено на 3600 для часов
            base_cost += car.price * duration_hours

            # Получаем штраф
            try:
                fine = Fine.objects.get(user=request.user, car=car)
                fine_amount += fine.amount
            except Fine.DoesNotExist:
                pass

            # Получаем скидку
            active_sales = Sales.objects.filter(active=True)
            for sale in active_sales:
                discount += sale.discount

        # Рассчитываем итоговую стоимость
        total_cost = base_cost + fine_amount - discount

        # Округление
        base_cost = base_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        fine_amount = fine_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        discount = discount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        total_cost = total_cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        order_details.append({
            'date': order.date,
            'base_cost': base_cost,
            'fine_amount': fine_amount,
            'discount': discount,
            'total_cost': total_cost,
            'order': order
        })
    
    return render(request, 'order_list.html', {'orders': order_details})


# Представление каталога автомобилей
def catalog_view(request, service_type):
    # Задаем заголовок каталога в зависимости от типа услуги
    catalog_titles = {
        'with_driver': 'Аренда автомобилей с водителем',
        'without_driver': 'Аренда автомобилей без водителя',
        'limousine': 'Долгосрочная аренда',
        'suv': 'Аренда с выездом за границу'
    }
    
    catalog_title = catalog_titles.get(service_type, 'Каталог автомобилей')
    
    # Получение всех автомобилей из базы данных
    cars = Car.objects.all()
    
    return render(request, 'catalog.html', {'cars': cars, 'catalog_title': catalog_title})


@login_required
def order_cost(request):
    orders = Order.objects.filter(user=request.user).order_by()
    return render(request, 'order_cost.html', {'orders': orders})

@login_required
def orders_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)

    # Получаем активный промокод
    try:
        active_discount = Sales.objects.get(work=True).about
    except Sales.DoesNotExist:
        active_discount = 0

    # Обработка заказов
    for order in orders:
        for car in order.cars.all():
            base_price = car.object.price * car.day
            try:
                fine = Fine.objects.get(user=user, car=car.object).cost
            except Fine.DoesNotExist:
                fine = 0

            car.total_price = base_price + fine - active_discount

    return render(request, "orders.html", context={'orders': orders, 'active_discount': active_discount})


def calculate_total_price(car_item):
    # Initial price of the car
    total_price = car_item.object.price

    # Check if there's any fine associated with the car
    try:
        fine = Fine.objects.get(car=car_item.object)
        total_price += fine.cost
    except Fine.DoesNotExist:
        pass

    # Check if there's any active sales or promo code
    try:
        sales = Sales.objects.get(name='promo_code', work=True)
        total_price -= sales.about  # Subtract promo code amount from total price
    except Sales.DoesNotExist:
        pass

    return total_price    


def user_fines(request):
    user = request.user  # Assuming user is authenticated
    fines = Fine.objects.filter(user=user)
    return render(request, 'shtraf_list.html', {'fines': fines})

def filter_cars(request):
    form = FilterForm()
    results = []

    if 'mark' in request.GET:
        form = FilterForm(request.GET)
        if form.is_valid():
            selected_mark = form.cleaned_data['mark']
            if selected_mark:
                results = Car.objects.filter(mark=selected_mark)

    return render(request, 'filter.html', {'form': form, 'results': results})

def search_view(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Car.objects.filter(model__icontains=query)

    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})
@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Логика для изменения заказа, например, показ формы для редактирования
    return render(request, 'update_order.html', {'order': order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'confirm_delete.html', {'order': order})

def update_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        form = UpdateOrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Adjust the redirect to your cart view
    else:
        form = UpdateOrderItemForm(instance=order_item)
    return render(request, 'update_order_item.html', {'form': form, 'order_item': order_item})

def delete_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_item.delete()
    return redirect('order_list')  # Adjust the redirect to your cart view