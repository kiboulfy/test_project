from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        return obj.user == request.user 
    

class IsSenderOrReceiver(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            if user == obj.ad_sender.user or user == obj.ad_receiver.user:
                return True 
            raise PermissionDenied("Вы не можете просматривать это предложение обмена.")

        if request.method in ('PUT', 'PATCH'):
            if user == obj.ad_receiver.user:
                return True 
            raise PermissionDenied("Только получатель может изменить статус предложения.")

        raise PermissionDenied("Доступ запрещён.")