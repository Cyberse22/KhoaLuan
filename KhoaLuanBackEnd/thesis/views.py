from django.http import JsonResponse
from django.shortcuts import render
from djoser.serializers import TokenCreateSerializer
from rest_framework import viewsets, permissions, generics, parsers, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomUser, Thesis, DefenseCouncil, ThesisScore
from .serializers import CustomUserSerializer, DefenseCouncilSerializer, ThesisScoreSerializer, ThesisSerializer, UserChangePasswordSerializer
from .perms import IsSinhVien, IsGiaoVuKhoa, IsGiangVien, IsAdmin


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

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
    permission_classes = [permissions.IsAuthenticated, IsGiangVien, IsGiaoVuKhoa]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated(), IsGiaoVuKhoa(), IsGiangVien()]

        return [permissions.AllowAny()]

    @action(methods='post', url_path='create_council', url_name='create_council', detail=False)
    def create_council(self, request):
        data = request.data

        serializer = DefenseCouncilSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.filter(active=True)
    serializer_class = ThesisSerializer
    permission_classes = [permissions.IsAuthenticated, IsSinhVien, IsGiaoVuKhoa]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods='post', url_path='post_info', url_name='post_info', detail=True)
    def post_info(self, request, pk=None):
        thesis = self.get_object()

        if not IsGiaoVuKhoa().has_permission(request, self):
            return Response({'error': 'Không có quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        info = ['id', 'name', 'students', 'advisors', 'date_defend', 'is_defend']
        for field in info:
            setattr(thesis, field, request.data.get(field))

        thesis.save()
        return Response({'message': 'Thông tin đã được cập nhật thành công.'}, status=status.HTTP_200_OK)

    @action(methods='post', url_path='upload_file', url_name='upload_file', detail=True)
    def upload_file(self, request, pk=None):
        thesis = self.get_object()
        upload_file = request.FILES.get('file')
        if upload_file:
            thesis.file_thesis.save(upload_file.name, upload_file)
            return Response({'message': 'File đã được tải lên thành công.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Không có file được tải lên.'}, status=status.HTTP_400_BAD_REQUEST)


class ThesisScoreViewSet(viewsets.ModelViewSet):
    queryset = ThesisScore.objects.filter(active=True)
    serializer_class = ThesisScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated(), IsSinhVien(), IsGiangVien(), IsGiaoVuKhoa]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True)
    def score_thesis(self, request, pk=None):
        thesis_score = self.get_object()

        if IsGiangVien().has_permission():
            score = request.data.get('score')
            criteria = request.data.get('criteria')

            thesis_score.score = score
            thesis_score.criteria = criteria
            thesis_score.save()

            return Response({'message': 'Điểm đã được cập nhật thành công.'}, status=status.HTTP_200_OK)

        elif IsSinhVien().has_permission(request, self):
            score = thesis_score.score
            criteria = thesis_score.criteria
            return Response({'message': f'Điểm của bạn là {score}', 'criteria': criteria}, status=status.HTTP_200_OK)

        elif IsGiaoVuKhoa().has_permission(request, self):
            score = thesis_score.score
            criteria = thesis_score.criteria
            return Response({'message': f'Điểm là {score}', 'criteria': criteria}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Người dùng không có quyền thực hiện hành động này'}, status=status.HTTP_403_FORBIDDEN)
