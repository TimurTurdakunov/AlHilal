from rest_framework import permissions
from processes.servisses.other_functions import get_user_id_from_token
from processes.models import CustomUser
from django.contrib.auth.models import Group


class IsActive(permissions.BasePermission):

    message = 'Пользователь не активен в системе'

    def has_permission(self, request, view):
        user = CustomUser.objects.get(pk=get_user_id_from_token(request))
        if user.is_active:
            return True
        return False


class IsMethodPost(permissions.BasePermission):
    message = 'у пользователя нет прав'

    def has_permission(self, request, view):
        return request.method == "POST"


class IsMaker(permissions.BasePermission):

    message = 'у пользователя нет прав'

    def has_permission(self, request, view):
        groups = CustomUser.objects.get(pk=get_user_id_from_token(request)).groups.all()
        if 'makr' in [group.name for group in groups]:
            return True
        return False


class IsAuthorizer(permissions.BasePermission):
    message = 'у пользователя нет прав'

    def has_permission(self, request, view):
        groups = CustomUser.objects.get(pk=get_user_id_from_token(request)).groups.all()
        if 'authorizer' in [group.name for group in groups]:
            return True
        return False


class IsOperationist(permissions.BasePermission):
    message = 'у пользователя нет прав'

    def has_permission(self, request, view):
        groups = CustomUser.objects.get(pk=get_user_id_from_token(request)).groups.all()
        if 'operationist' in [group.name for group in groups]:
            return True
        return False

class IsAdmin(permissions.BasePermission):
    message = 'у пользователя нет прав'

    def has_permission(self, request, view):
        groups = CustomUser.objects.get(pk=get_user_id_from_token(request)).groups.all()
        if 'admin' in [group.name for group in groups]:
            return True
        return False