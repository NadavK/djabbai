from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Duty, Shabbat, Assignment, Roster
from .serializers import ShabbatSerializer, AssignmentSerializer, DutySerializer, RosterSerializer, \
    RosterUpdateSerializer, AssignmentUpdateSerializer, ShabbatUpdateSerializer


class UpdateSerializerMixin(object):
    """
    specify a different serializer to use for PUT requests
    http://www.adamwester.me/blog/django-rest-framework-change-update-serializer/
    """

    def get_serializer_class(self):
        """
        return a different serializer if performing an update
        """
        serializer_class = self.serializer_class

        if self.request.method in ['PUT', 'POST'] and self.update_serializer_class:
            serializer_class = self.update_serializer_class

        return serializer_class


class DutyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Manage Duties
    """
    queryset = Duty.objects.all() #.order_by('dayt')
    serializer_class = DutySerializer


class ShabbatViewSet(UpdateSerializerMixin, viewsets.ModelViewSet):
    """
    Manage Shabbatot
    """
    queryset = Shabbat.objects.all().order_by('dayt')
    serializer_class = ShabbatSerializer
    update_serializer_class = ShabbatUpdateSerializer


class AssignmentUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:               # Superuser is g-d
            return True

        if not request.user.is_authenticated:       # Anon cannot do anything
            return False

        """we need to do all permission checking here, since has_object_permission() is not guaranteed to be called"""
        if 'pk' in view.kwargs and view.kwargs['pk']:
            try:
                assignment = view.get_queryset().get(pk=view.kwargs['pk'])
            except ObjectDoesNotExist:
                return False                                # caller does not have 'permission' to access non-existent objects

            if not request.user.profile.can_edit(assignment.profile.pk):   # The user is allowed to update their own object or child-owned objects
                return False

            if 'profile' in request.data and request.data['profile']:
                return request.user.profile.can_edit(request.data['profile'])   # The user is allowed to update the assignment to themselves or their children

            return True

        else:
            # check model permissions
            return False

    def has_object_permission(self, request, view, obj):
        """ nothing to do here, we already checked everything, so ignore """
        return True


class AssignmentViewSet(UpdateSerializerMixin, viewsets.ModelViewSet):
    """
    retrieve:
    Returns the requested roster/assignment.

    list:
    Returns all assignments in this roster.

    create:
    Create a new assignment in this roster.

    update:
    Update an assignment in this roster.

    delete:
    Delete an assignment in this roster.
    """
    queryset = Assignment.objects.all() #.order_by('dayt')
    serializer_class = AssignmentSerializer
    update_serializer_class = AssignmentUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = [AssignmentUpdatePermission, ]
        return super(AssignmentViewSet, self).get_permissions()

    def list(self, request, roster_pk=None):
        queryset = self.queryset.filter(roster_id=roster_pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, roster_pk=None):
        try:
            assignment = self.queryset.get(pk=pk, roster_id=roster_pk)
            serializer = self.serializer_class(assignment, many=False)
            return Response(serializer.data)
        except Assignment.DoesNotExist:
            raise Http404

    def create(self, request, pk=None, roster_pk=None):
        request.data["roster"] = roster_pk
        return super(AssignmentViewSet, self).create(request)

    def update(self, request, pk=None, roster_pk=None):
        try:
            self.queryset.get(pk=pk, roster_id=roster_pk)      # Ensure Assignment matches Roster
        except Assignment.DoesNotExist:
            raise Http404

        request.data["roster"] = roster_pk
        return super(AssignmentViewSet, self).update(request)


class RosterViewSet(UpdateSerializerMixin, viewsets.ModelViewSet):
    """
    Manage roster (list of assignments)
    """
    queryset = Roster.objects.all() #.order_by('dayt')
    serializer_class = RosterSerializer
    update_serializer_class = RosterUpdateSerializer
