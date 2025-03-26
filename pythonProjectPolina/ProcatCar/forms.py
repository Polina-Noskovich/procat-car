from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import forms, CharField, PasswordInput, TextInput, ModelForm, ChoiceField, Textarea, Select, EmailField, HiddenInput, ModelChoiceField
from django import forms
from .models import Contacts

from .models import Feedbacks, Seller, Customer, Car, CarMark, OrderItem

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['name', 'contactimg', 'phone_number', 'mail']

class RegisterUserForm(UserCreationForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-input'}))
    password1 = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-input'}))
    password2 = CharField(label='Повтор пароля', widget=PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Можно добавить email, first_name и другие поля


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-input'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-input'}))

class FeedbackForm(ModelForm):
    text = forms.CharField(
        label='Отзыв',
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'cols': 50})
    )

    class Meta:
        model = Feedbacks
        fields = ['text']


class SellerForm(ModelForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-input'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-input'}))
    name = CharField(label='Имя', max_length=20,
                     widget=TextInput(attrs={'class': 'form-input'}))
    companyname = CharField(label='Имя компании', max_length=20,
                            widget=TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Seller
        fields = ['username', 'password', 'name', 'companyname']

from django.forms import ModelForm, CharField, TextInput, PasswordInput, EmailField, IntegerField
from django.core.validators import MinValueValidator

class CustomerForm(ModelForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-input'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-input'}))
    name = CharField(label='Ваше имя', max_length=20, widget=TextInput(attrs={'class': 'form-input'}))
    phone_number = CharField(label='Номер', max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )], widget=TextInput(attrs={'class': 'form-input'}))
    city = CharField(label='Город', max_length=20, widget=TextInput(attrs={'class': 'form-input'}))
    adress = CharField(label='Адрес', max_length=100, widget=TextInput(attrs={'class': 'form-input'}))
    email = EmailField(label='Почта', widget=TextInput(attrs={'class': 'form-input'}))
    age = IntegerField(label='Возраст', validators=[MinValueValidator(18)], widget=TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Customer
        fields = ['username', 'password', 'name', 'phone_number', 'city', 'adress', 'email', 'age']



class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['contactimg', 'mark', 'price', 'model']


class AddSpeciesForm(ModelForm):
    class Meta:
        model = CarMark
        fields = ['contactimg', 'mark']

class FilterForm(forms.Form):
    mark = ModelChoiceField(
        queryset=CarMark.objects.all(),
        label='Марка',
        required=False
    )

class SearchForm(ModelForm):
    class Meta:
        model = Car
        fields = ['query']
    query = CharField(label='Поиск', max_length=100)

class UpdateOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['count']