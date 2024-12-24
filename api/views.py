from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import json

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @transaction.atomic  # Ensures both user and account creation are atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the user
            user = serializer.save()

            return Response({"message": "User and account created successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # 確保用戶需要帶有有效的 Token 才能訪問

    @transaction.atomic  # 確保更新操作為原子性
    def put(self, request, *args, **kwargs):
        try:
            # 從 Token 中獲取當前用戶
            user = request.user

            # 驗證是否提供了原始數據
            if not request.body:
                return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

            # 將原始 JSON 數據轉換為字典
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON data."}, status=status.HTTP_400_BAD_REQUEST)

            # 更新用戶資料
            username = data.get('username', user.username)  # 如果未提供，保留現有值
            password = data.get('password')

            if username:
                user.username = username
            if password:
                user.set_password(password)  # 將密碼哈希化

            user.save()  # 保存更新

            return Response({"message": "User account updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

