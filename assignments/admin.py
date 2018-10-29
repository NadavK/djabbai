from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from nested_admin.nested import NestedModelAdmin, NestedTabularInline
from reversion_compare.admin import CompareVersionAdmin

from .models import Duty, Assignment, Shabbat, Roster


class AssignmentInline(NestedTabularInline):
    #model = Shabbat.assignments.through
    model = Assignment
    extra = 1

class RosterInline(NestedTabularInline):
    #model = Shabbat.assignments.through
    model = Roster
    extra = 5
    inlines = [AssignmentInline]

class ShabbatInline(NestedTabularInline):
    model = Shabbat
    extra = 5

#
# class ShabbatForm(forms.ModelForm):
#     class Meta:
#         model = Shabbat
#         fields = '__all__'
#
#     def clean(self):
#         categories = self.cleaned_data.get('shabbat_assoc')
#         print(self.cleaned_data)
#         print(categories)
#         if categories and categories.count() > 3:
#             raise ValidationError('Maximum three readings are allowed.')
#
#         return self.cleaned_data



@admin.register(Shabbat)
class ShabbatAdmin(NestedModelAdmin):
    inlines = [RosterInline, ]
    #exclude = ('assignments',)
    #form = ShabbatForm
    list_display = ('parasha', 'dayt')


    def XXXformfield_for_manytomany(self, db_field, request, **kwargs):

        from users.models import Profile

        print(db_field.name)
        if db_field.name == 'readingsxxxx':
            kwargs['initial'] = [Assignment.objects.all()[5], Assignment.objects.all()[3]]
            return db_field.formfield(**kwargs)
        if db_field.name == 'toransxxx':
            kwargs['initial'] = [Profile.objects.all()[0]]
            return db_field.formfield(**kwargs)

        return super(ShabbatAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    #
    # def get_form(self, request, obj=None, **kwargs):
    #     from users.models import User
    #     form = super(ShabbatAdmin, self).get_form(request, obj, **kwargs)
    #     print(form.base_fields['maariv'])
    #     form.base_fields['maariv'].initial = [User.objects.all()[0]]
    #     return form


#admin.site.register(Assignment)
@admin.register(Assignment)
class RosterAdmin1(NestedModelAdmin):
    pass

@admin.register(Roster)
class RosterAdmin2(NestedModelAdmin):
    inlines = [AssignmentInline, ]

#@admin.register(Assignment)
#class AssignmentAdmin(admin.ModelAdmin):
#    inlines = (ShabbatInline,)

#admin.site.register(Duty)
@admin.register(Duty)
class DutyAdmin(CompareVersionAdmin, NestedModelAdmin):
    list_display = ('name', 'category', 'order_id', 'applicable_for_profile', 'not_applicable_for_roster', 'applicable_for_adults', 'applicable_for_children')
