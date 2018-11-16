"""djabbai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_nested import routers
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_jwt import views as jwt_views

from parashot.views import ParashaViewSet, SegmentViewSet
from assignments.views import DutyViewSet, ShabbatViewSet, AssignmentViewSet, RosterViewSet
from users.views import ProfileViewSet, FamilyViewSet, SpouseProfileViewSet, check_user, check_verification_code, ChildProfileViewSet, MyUserCreateView, get_current_profile, ParentProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
#router.register(r'families', FamilyViewSet)
router.register(r'parashas', ParashaViewSet)
#router.register(r'segments', SegmentViewSet)
router.register(r'duties', DutyViewSet)
#router.register(r'shabbats', ShabbatViewSet)
#router.register(r'roster', RosterViewSet)

#roster_router = routers.NestedDefaultRouter(router, r'roster', lookup='roster')
#roster_router.register(r'assignments', AssignmentViewSet, base_name='roster-assignment')

profiles_router = routers.NestedDefaultRouter(router, r'profiles', lookup='profile')
#profiles_router.register(r'families', FamilyViewSet, base_name='profile-family')
profiles_router.register(r'spouse', SpouseProfileViewSet, base_name='profile-spouse')
profiles_router.register(r'children', ChildProfileViewSet, base_name='profile-child')
profiles_router.register(r'parent', ParentProfileViewSet, base_name='profile-parent')
#profiles_router.register(r'mother', ParentProfileViewSet, base_name='profile-mother')

#families_router = routers.NestedDefaultRouter(profiles_router, r'families', lookup='family')
#families_router.register(r'parents', ParentsViewSet, base_name='parents-user')
##families_router.register(r'children', ChildrenUserViewSet, base_name='family-user')


urlpatterns = [
    #url(r'^$', get_swagger_view(title='Djabbai API')),

    url(r'^api/v1/', include(router.urls)),
    #url(r'^api/v1/', include(roster_router.urls)),
    url(r'^api/v1/', include(profiles_router.urls)),
    #url(r'^api/v1/', include(families_router.urls)),
    url(r'^api/v1/auth/users/create/', MyUserCreateView.as_view(), name='user-create'),    # Override djoser registration. Make sure it comes *before* djoser
    url(r'^api/v1/auth/', include('djoser.urls')),
    url(r'^api/v1/profile/', get_current_profile, name='get_current_profile'),
    url(r'^api/v1/users/check_user/(?P<first_name>.+)/(?P<last_name>.+)/(?P<verification_code>.*)/$', check_user, name='check_user'),
    url(r'^api/v1/users/check_user/(?P<first_name>.+)/(?P<last_name>.+)/$', check_user, name='check_user'),
    url(r'^api/v1/users/check_verification_code/(?P<verification_code>.+)/$', check_verification_code, name='check_verification_code'),
    url(r'^nimda/', admin.site.urls),
    url(r'^report_builder/', include('report_builder.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', jwt_views.obtain_jwt_token, name='api-token-auth'),
    url(r'^api-token-refresh/', jwt_views.refresh_jwt_token),
    url(r'^api-token-verify/', jwt_views.verify_jwt_token),

    # other urls
    url(r"^notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
]
