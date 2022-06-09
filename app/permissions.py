from rest_framework.permissions import BasePermission



class IsPhotographerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_photographer)


class IsBuyerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_buyer)