from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
import json
from reversion_compare.admin import CompareVersionAdmin

from users.serializers import ProfileSerializer
from .models import User, Family, Profile







from django.utils.translation import gettext_lazy as _

class ParashotListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = _('פרשת בר-מצווה')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'bar_mitzvah_parasha_bool'

    def lookups(self, request, model_admin):
        return (
            (True, _('יש')),
            (False, _('אין')),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        elif self.value() == 'True':
            return queryset.filter(bar_mitzvah_parasha__isnull=False).distinct()
        else:
            return queryset.filter(bar_mitzvah_parasha__isnull=True)


class DodListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = _('יארצייט')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'dod_bool'

    def lookups(self, request, model_admin):
        return (
            (True, _('יש')),
            (False, _('אין')),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        elif self.value() == 'True':
            return queryset.filter(dod_month__isnull=False).distinct()
        else:
            return queryset.filter(dod_month__isnull=True)












@admin.register(Family)
class FamilyAdmin(CompareVersionAdmin, admin.ModelAdmin):
    filter_horizontal = ('parents', 'children')


class ProfileInline(admin.TabularInline):
    model = Profile
    #list_display = ('__all__x',)#''full_name', 'father_details')
    #fk_name = 'details_profile'

class ProfileParentsInline(admin.TabularInline):
    model = Profile
    #list_display = ('__all__x',)#''full_name', 'father_details')
    fk_name = 'children'


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'link_to_profile')
    #exclude = ('children',)
    inlines = [
        ProfileInline,
    ]

    def link_to_profile(self, obj):
        if obj.profile:
            link = reverse("admin:users_profile_change", args=[obj.profile.id])
            return format_html('<a href="{}">{}</a>', link, str(obj.profile) + '\u200f')

        #return str(obj.profile) + '\u200f'
    link_to_profile.short_description = 'פרופיל'


@admin.register(Profile)
class ProfileAdmin(CompareVersionAdmin, DjangoObjectActions, admin.ModelAdmin):
    list_display = ('display_name_with_family', 'first_name', 'last_name', 'family_links', 'verification_code', 'link_to_user', 'head_of_household', 'gender', 'bar_mitzvahed', 'bar_mitzvah_parasha', 'rcv_user_emails', 'rcv_admin_emails', 'dod_day', 'dod_month')
    read_only_fields = ('family_links',)
    actions = ['export', 'set_head_of_household', 'unset_head_of_household']
    list_filter = ('gender', 'bar_mitzvahed', 'head_of_household', ParashotListFilter, DodListFilter)
    #exclude = ('children',)
    inlines = [
        #ProfileParentsInline,
    ]
    search_fields = ['_display_name', '^first_name', '^last_name', 'full_name', 'verification_code']
    change_list_template = 'admin/users/profile/change_list.html'

    def family_links(self, obj):

        def prepare_html(families, family, relation):
            # families = families + family.__str__() + ', '
            families = families + '<a href="{}">{}</a>'.format(
                reverse("admin:users_family_change", args=(family.pk,)), family.display_name()) + ' [' + relation + '], '
            return families

        families = ""
        for family in obj.family_of_children.all():
            families = prepare_html(families, family, 'ילד')
        for family in obj.family_of_parent.all():
            families = prepare_html(families, family, 'הורה')
        return mark_safe(families[:-2] + '&#x200f;')
    family_links.short_description = 'משפחות'

    Profile.display_name_with_family.fget.short_description = 'שם'          #https://stackoverflow.com/questions/7241000/django-short-description-for-property
    #get_family.admin_order_field = 'book__author'

    def link_to_user(self, obj):
        if obj.user:
            link = reverse("admin:users_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', link, obj.user.id)
    link_to_user.short_description = 'משתמש'
    link_to_user.admin_order_field  = 'user__id'

    def export(self, request, queryset):
        serializer = ProfileSerializer(queryset, many=True)
        data = json.dumps(serializer.data)
        response = HttpResponse(data, content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename=profile.json'
        return response
    export.short_description = "Export selected profiles"

    def XXXset_head_of_household(self, request, queryset):
        queryset.update(head_of_household=True)

    def XXXunset_head_of_household(self, request, queryset):
        queryset.update(head_of_household=False)

    def export_this(self, request, queryset):
        response = HttpResponse(queryset.count(), content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename=profile.json'
        return response

        #return self.export(request, queryset.count())
    export_this.label = "Export All"  # optional
    export_this.short_description = "Export profiles"  # optional

    changelist_actions = ('export_this', )

    def reversion_register(self, model, **options):
        options['follow'] = ('duties', 'bar_mitzvah_parasha', 'default_family_to_add_children')
        #options['exclude'] = ['bar_mitzvah_parasha', 'default_family_to_add_children']
        super().reversion_register(model, **options)
    compare_exclude = ['bar_mitzvah_parasha', 'default_family_to_add_children']

    def compare_bar_mitzvah_parasha(self, obj_compare):
        if obj_compare.value1 != obj_compare.value2:
            return "%r > %r" % (obj_compare.value1, obj_compare.value2)
