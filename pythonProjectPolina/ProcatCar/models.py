from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()
    logo = models.ImageField(upload_to='partner_logos/')

    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']  # Сортировать по дате публикации

class CompanyLogo(models.Model):
    image = models.ImageField(upload_to='company_logos/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description or "Company Logo"
    
class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Feedbacks(models.Model):
    name = models.CharField('Имя пользователя', max_length=20)
    rating = models.IntegerField('Оценка', choices=[(i, i) for i in range(1, 6)])  # Оценка от 1 до 5
    text = models.TextField('Текст отзыва', max_length=2500)
    date = models.DateField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating} звезды)"

'''class Feedbacks(models.Model):  # отзывы
    name = models.CharField('Имя пользователя', max_length=20)
    rating = models.IntegerField()
    text = models.TextField('Отзыв', max_length=2500)
    date = models.DateField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.rating}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'''

from django.utils import timezone

class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=255)
    answer = models.TextField('Ответ')
    date_added = models.DateTimeField('Дата добавления', default=timezone.now)

    def __str__(self):
        return self.question

class About(models.Model):
    aboutimg = models.ImageField('Картинка', upload_to='static', default=True)
    ustext = models.CharField('МЫ', max_length=100)
    logo = models.ImageField('Логотип', upload_to='static', null=True, blank=True)  # Логотип компании
    video = models.URLField('Видео о компании', max_length=200, null=True, blank=True)  # URL на видео
    history = models.TextField('История компании по годам', null=True, blank=True)  # История компании
    requisites = models.TextField('Реквизиты компании', null=True, blank=True)  # Реквизиты компании
    certificate = models.TextField('Сертификаты компании', null=True, blank=True)  # Сертификаты компании

    def __str__(self):
        return self.ustext


class News(models.Model):
    newscrat = models.CharField('Краткая', max_length=100)
    news = models.CharField('Полная', max_length=300)
    newsimg = models.ImageField('Картинка', upload_to='static')
    def str(self):
        return self.newscrat


class Contacts(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default=True)
    name= models.CharField('Имя', max_length=100)
    mail = models.CharField('Почта', max_length=300)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона"
            )
        ],
        blank=True
    )
    def str(self):
        return self.name




class Vac(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default=True)
    vac = models.CharField('Название', max_length=100)
    vacopis = models.CharField('Полное описание', max_length=300)
    def str(self):
        return self.vac

class Sales(models.Model):
    sales = models.CharField('Название', max_length=100)
    saleopis = models.CharField('Полное описание', max_length=300)
    def str(self):
        return self.sales


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Имя пользователя', max_length=20)
    phone_number = models.CharField('Номер телефона', max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )], blank=True)
    city = models.CharField('Город', max_length=20)
    adress = models.CharField('Адрес', max_length=100)
    email = models.EmailField('Почта')
    age = models.PositiveIntegerField('Возраст')

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.age is not None and self.age < 18:
            raise ValidationError('Возраст должен быть 18 или больше.')


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Имя пользователя', max_length=20)
    companyname = models.CharField('Название компании', max_length=20)
    def __str__(self):
        return self.name


class CarMark(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default='default.jpg')
    mark = models.CharField('Марка', max_length=30)

    def __str__(self):
        return self.mark

class Car(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default='default.jpg')
    mark = models.ForeignKey(CarMark, related_name='cars', on_delete=models.CASCADE)
    model = models.CharField('Модель', max_length=30)
    year = models.IntegerField('Год выпуска')
    price = models.DecimalField('Стоимость автомобиля', max_digits=10, decimal_places=2)
    daily_rent = models.DecimalField('Суточная стоимость проката', max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.mark} {self.model} ({self.year})"

class Sales(models.Model):
    active = models.BooleanField('Действует', default=True)
    code = models.CharField('Промокод', max_length=30)
    discount = models.DecimalField('Скидка в рублях', max_digits=10, decimal_places=2)

class Fine(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    amount = models.DecimalField('Сумма штрафа', max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    count=models.IntegerField('Время')
    object=models.ForeignKey(Car, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)  # Изменено на ForeignKey
    date = models.DateField('Дата заказа', auto_now_add=True)
    cars = models.ManyToManyField(OrderItem, blank=True)



