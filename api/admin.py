from django.contrib import admin
from .models import Bay, Booking, Customer

# Register your models here.
admin.site.register([Bay, Booking, Customer])
