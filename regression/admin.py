from django.contrib import admin
from regression.models import Regression_ideal

# Create model admin here
class Regression_idealAdmin(admin.ModelAdmin):
    #Set list_display to control which fields are displayed on the change list page of the admin.
    list_display = ["__str__", "quantity"]

    class Meta:
        model = Regression_ideal

# Register your models here.
admin.site.register(Regression_ideal, Regression_idealAdmin) #This connect post model with post model admin.
