from django.contrib import admin
from .models import custom_user, Product, media_files, Wilaya,car_model,car_serie,piece
# Register your models here.
admin.site.register(Wilaya)
admin.site.register(car_serie)
admin.site.register(car_model)
admin.site.register(piece)

