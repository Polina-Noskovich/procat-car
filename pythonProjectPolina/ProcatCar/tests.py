from django.test import TestCase
from django.contrib.auth.models import User
from .models import Feedbacks, FAQ, About, News, Contacts, Vac, Sales, Customer, Seller, CarMark, Car, Shtraf, OrderItem, Order

class FeedbacksTestCase(TestCase):
    def test_feedback_creation(self):
        feedback = Feedbacks.objects.create(name='Test User', rating=5, text='Test feedback')
        self.assertEqual(feedback.name, 'Test User')
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.text, 'Test feedback')

class FAQTestCase(TestCase):
    def test_faq_creation(self):
        faq = FAQ.objects.create(question='Test Question', answer='Test Answer', date='2024-05-30')
        self.assertEqual(faq.question, 'Test Question')
        self.assertEqual(faq.answer, 'Test Answer')
        self.assertEqual(faq.date, '2024-05-30')

class AboutTestCase(TestCase):
    def test_about_creation(self):
        about = About.objects.create(aboutimg='test.jpg', ustext='Test text')
        self.assertEqual(about.ustext, 'Test text')

class NewsTestCase(TestCase):
    def test_news_creation(self):
        news = News.objects.create(newscrat='Test Summary', news='Test news', newsimg='test.jpg')
        self.assertEqual(news.newscrat, 'Test Summary')
        self.assertEqual(news.news, 'Test news')

class ContactsTestCase(TestCase):
    def test_contacts_creation(self):
        contacts = Contacts.objects.create(contactimg='test.jpg', name='Test Name', mail='test@example.com', phone_number='+1234567890')
        self.assertEqual(contacts.name, 'Test Name')
        self.assertEqual(contacts.mail, 'test@example.com')
        self.assertEqual(contacts.phone_number, '+1234567890')

class VacTestCase(TestCase):
    def test_vac_creation(self):
        vac = Vac.objects.create(contactimg='test.jpg', vac='Test Vacancy', vacopis='Test description')
        self.assertEqual(vac.vac, 'Test Vacancy')

class SalesTestCase(TestCase):
    def test_sales_creation(self):
        sales = Sales.objects.create(name='Test Sale', about=100)
        self.assertEqual(sales.name, 'Test Sale')
        self.assertEqual(sales.about, 100)

class CustomerTestCase(TestCase):
    def test_customer_creation(self):
        user = User.objects.create(username='test_user')
        customer = Customer.objects.create(user=user, name='Test Customer', phone_number='+1234567890', city='Test City', adress='Test Address', email='test@example.com')
        self.assertEqual(customer.name, 'Test Customer')
        self.assertEqual(customer.phone_number, '+1234567890')

class SellerTestCase(TestCase):
    def test_seller_creation(self):
        user = User.objects.create(username='test_seller')
        seller = Seller.objects.create(user=user, name='Test Seller', companyname='Test Company')
        self.assertEqual(seller.name, 'Test Seller')
        self.assertEqual(seller.companyname, 'Test Company')

class CarMarkTestCase(TestCase):
    def test_carmark_creation(self):
        carmark = CarMark.objects.create(mark='Test Mark')
        self.assertEqual(carmark.mark, 'Test Mark')

class CarTestCase(TestCase):
    def test_car_creation(self):
        carmark = CarMark.objects.create(mark='Test Mark')
        car = Car.objects.create(mark=carmark, price=10000, model='Test Model')
        self.assertEqual(car.mark, carmark)
        self.assertEqual(car.price, 10000)
        self.assertEqual(car.model, 'Test Model')

class ShtrafTestCase(TestCase):
    def test_shtraf_creation(self):
        user = User.objects.create(username='test_user')
        carmark = CarMark.objects.create(mark='Test Mark')
        car = Car.objects.create(mark=carmark, price=10000, model='Test Model')
        shtraf = Shtraf.objects.create(user=user, car=car, cost=500)
        self.assertEqual(shtraf.user, user)
        self.assertEqual(shtraf.car, car)
        self.assertEqual(shtraf.cost, 500)

class OrderTestCase(TestCase):
    def test_order_creation(self):
        user = User.objects.create(username='test_user')
        carmark = CarMark.objects.create(mark='Test Mark')
        car = Car.objects.create(mark=carmark, price=10000, model='Test Model')
        order_item = OrderItem.objects.create(count=1, object=car)
        order = Order.objects.create(user=user)
        order.cars.add(order_item)
        self.assertEqual(order.user, user)
        self.assertEqual(order.cars.first(), order_item)


