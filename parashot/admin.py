from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin
from .models import Parasha, Segment


#from django.contrib.contenttypes.admin import GenericTabularInline
#class InputToOutputInline(GenericTabularInline):
class InputToOutputInline(admin.TabularInline):
    model = Segment
    extra = 0


@admin.register(Parasha)
class ParashaAdmin(CompareVersionAdmin):
    inlines = (InputToOutputInline, )


admin.site.register(Segment)
