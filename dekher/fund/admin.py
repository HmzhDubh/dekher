from django.contrib import admin
from .models import Fund, Review, Favorite
# Register your models here.

admin.site.register(Fund)
admin.site.register(Review)
admin.site.register(Favorite)
