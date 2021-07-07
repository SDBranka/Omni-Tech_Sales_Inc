"""ImgFieldProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# to run app urls
from django.urls import path, include

# to use ImageField
from django.conf.urls.static import static
from django.conf import settings

# to use admin dashboard
from django.contrib import admin
from imgfield_app.models import User, Product, EnteredItem, Photo, Category, Order, OrderProduct, OrderItem, Quote, QuoteProduct, QuoteItem, ContactInfo, Review
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)
class EnteredItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(EnteredItem, EnteredItemAdmin)
class PhotoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Photo, PhotoAdmin)
class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)
class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)
class OrderProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderProduct, OrderProductAdmin)
class OrderItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderItem, OrderItemAdmin)
class QuoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Quote, QuoteAdmin)
class QuoteProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuoteProduct, QuoteProductAdmin)
class QuoteItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuoteItem, QuoteItemAdmin)  
class ContactInfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(ContactInfo, ContactInfoAdmin)
class ReviewAdmin(admin.ModelAdmin):
    pass
admin.site.register(Review, ReviewAdmin)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('imgfield_app.urls')),
    path('signon/', include('login_app.urls')),
    path('admin_access/', include('admin_app.urls')),
]

# to use ImageField
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)