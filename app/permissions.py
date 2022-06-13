from rest_framework.permissions import BasePermission

class IsPhotographerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_photographer)
class IsClientUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_client)
