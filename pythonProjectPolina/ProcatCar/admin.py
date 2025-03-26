from django.contrib import admin

from .models import FAQ, About, News, Contacts, Vac, Sales, Car, Seller, Customer, CarMark, Fine, Feedbacks
from .models import Partner, Article, Banner, CompanyLogo

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    search_fields = ('title',)

@admin.register(CompanyLogo)
class CompanyLogoAdmin(admin.ModelAdmin):
    list_display = ('description', 'image')

admin.site.register(FAQ)
admin.site.register(About)
admin.site.register(News)
admin.site.register(Contacts)
admin.site.register(Vac)
admin.site.register(Sales)
admin.site.register(Car)
admin.site.register(CarMark)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Fine)
admin.site.register(Feedbacks)
admin.site.register(Banner)