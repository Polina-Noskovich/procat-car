from statistics import mean, median, mode
from django.db.models import Sum
import matplotlib.pyplot as plt
from .models import Car, Order, OrderItem, Sales, Customer

def get_total_sales():
    total_sales = Sales.objects.aggregate(total=Sum('about'))['total']
    return total_sales or 0  # чтобы избежать None, если нет данных

def get_average_sales():
    all_sales = Sales.objects.values_list('about', flat=True)
    average_sales = mean(all_sales)
    return average_sales or 0  # чтобы избежать None, если нет данных

def get_sales_statistics():
    all_sales = Sales.objects.values_list('about', flat=True)
    sales_mode = mode(all_sales)
    sales_median = median(all_sales)
    return sales_mode or 0, sales_median or 0  # чтобы избежать None, если нет данных

def get_average_customer_age():
    all_ages = Customer.objects.exclude(age=None).values_list('age', flat=True)
    average_age = mean(all_ages)
    return average_age or 0  # чтобы избежать None, если нет данных

def get_median_customer_age():
    all_ages = Customer.objects.exclude(age=None).values_list('age', flat=True)
    median_age = median(all_ages)
    return median_age or 0  # чтобы избежать None, если нет данных

def get_customer_list():
    customer_list = Customer.objects.all().order_by('name')
    return customer_list

def get_car_list():
    car_list = Car.objects.all().order_by('model')
    return car_list

def generate_graph():
    # Example code for generating a simple bar chart
    sales_data = Car.objects.values('model').annotate(total_sales=Sum('sales__about'))
    models = [data['model'] for data in sales_data]
    sales = [data['total_sales'] for data in sales_data]

    plt.bar(models, sales)
    plt.xlabel('Car Models')
    plt.ylabel('Total Sales')
    plt.title('Sales by Car Model')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a file or render it directly in the view
    plt.savefig('sales_graph.png')


def generate_sales_graph():
    # Example code for generating a simple bar chart
    sales_data = Car.objects.values('model').annotate(total_sales=models.Sum('sales__about'))
    models = [data['model'] for data in sales_data]
    sales = [data['total_sales'] for data in sales_data]

    plt.bar(models, sales)
    plt.xlabel('Car Models')
    plt.ylabel('Total Sales')
    plt.title('Sales by Car Model')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a file or render it directly in the view
    plt.savefig('sales_graph.png')
