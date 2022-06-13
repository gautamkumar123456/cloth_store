from rest_framework import permissions

""""
Using IsOwner class to implement in our class to access only by authorized user.
"""


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id