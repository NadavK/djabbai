from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from rest_framework.reverse import reverse

#https://stackoverflow.com/a/46527083
class RelatedObjectLinkMixin(object):
    """
    Generate links to related links. Add this mixin to a Django admin model. Add a 'link_fields' attribute to the admin
    containing a list of related model fields and then add the attribute name with a '_link' suffix to the
    list_display attribute. For Example a Student model with a 'teacher' attribute would have an Admin class like this:

    class StudentAdmin(RelatedObjectLinkMixin, ...):
        link_fields = ['teacher']

        list_display = [
            ...
            'teacher_link'
            ...
        ]
    """

    link_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.link_fields:
            for field_name in self.link_fields:
                func_name = field_name + '_link'
                setattr(self, func_name, self._generate_link_func(field_name))

    def _generate_link_func(self, field_name):
        def _func(obj, *args, **kwargs):
            related_obj = getattr(obj, field_name)
            if related_obj:
                content_type = ContentType.objects.get_for_model(related_obj.__class__)
                url_name = 'admin:%s_%s_change' % (content_type.app_label, content_type.model)
                url = reverse(url_name, args=[related_obj.pk])
                return format_html('<a href="{}" class="changelink">{}</a>', url, str(related_obj))
            else:
                return None
        return _func