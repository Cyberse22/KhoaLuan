from rest_framework.permissions import BasePermission, IsAuthenticated


class OwnerAuthenticated(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_object_permission(request, view) and request.user == obj.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT']:
            return True
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsSinhVien(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'sinhvien'


class IsGiangVien(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'giangvien'


class IsGiaoVuKhoa(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'giaovukhoa'
