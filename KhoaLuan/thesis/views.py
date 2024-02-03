from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser, Thesis, DefenseCouncil, ThesisScore
from .serializers import CustomUserSerializer, DefenseCouncilSerializer, ThesisScoreSerializer, ThesisSerializer, UserChangePasswordSerializer
from .perms import IsSinhVien, IsGiaoVuKhoa


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='user/(?P<role>\w+)', url_name='user/(?P<role>\w+)', detail=False)
    def current_user(self, request, role):
        if role == 'sinhvien':
            response_data = {'role': 'sinhvien'}

        elif role == 'giangvien':
            response_data = {'role': 'giangvien'}

        elif role == 'giaovukhoa':
            response_data = {'role': 'giaovukhoa'}

        elif role == 'admin':
            response_data = {'role': 'admin'}

        else:
            response_data = {'error': 'Vai trò không hợp lệ'}

        return JsonResponse(response_data)

    @action(methods=['put'], detail=True)
    def chang_password(self, request):
        user = self.get_object()
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():  # Kiểm tra mật khẩu cũ
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Mật khẩu không đúng.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({'message': 'Mật khẩu đã được thay đổi.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DefenseCouncilViewSet(viewsets.ModelViewSet):
    queryset = DefenseCouncil.objects.filter(active=True)
    serializer_class = DefenseCouncilSerializer
    permission_classes = [permissions.IsAuthenticated]


class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.filter(active=True)
    serializer_class = ThesisSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods='post', url_path='post_info', url_name='post_info', detail=True)
    def post_info(self, request, pk=None):
        thesis = self.get_object()
        info = ['id', 'name', 'students', 'advisors', 'date_defend', 'is_defend']
        thesis.info = request.data.get(info)
        thesis.save()
        return Response({'message': 'Thông tin đã được cập nhật thành công.'}, status=status.HTTP_200_OK)

    @action(methods='post', url_path='upload_file', url_name='upload_file', detail=True)
    def upload_file(self, request, pk=None):
        thesis = self.get_object()
        upload_file = request.FILES.get('file')
        if upload_file:
            thesis.file_thesis.save(upload_file.name, upload_file)
        return Response({'message': 'File đã được tải lên thành công.'}, status=status.HTTP_200_OK)


class ThesisScoreViewSet(viewsets.ModelViewSet):
    queryset = ThesisScore.objects.filter(active=True)
    serializer_class = ThesisScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

