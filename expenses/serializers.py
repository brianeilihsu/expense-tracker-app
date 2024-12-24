from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Account, Category, Transaction, Report

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'password': {'write_only': True}  # 密碼僅允許寫入
        }
        
# Account Serializer
class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 嵌套 User 序列化器，僅允許讀取

    class Meta:
        model = Account
        fields = ['id', 'user', 'balance']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'user']  # 包含 user 字段
        read_only_fields = ['user']  # 確保 user 不可直接通過請求設置

    def create(self, validated_data):
        request = self.context['request']  # 從上下文獲取請求對象
        user = request.user
        name = validated_data.get('name')

        # 檢查當前用戶的 Category 是否已存在相同名稱
        if Category.objects.filter(user=user, name=name).exists():
            raise ValidationError({'name': 'Category with this name already exists for the current user.'})

        # 自動將 user 設置為當前請求用戶
        validated_data['user'] = user
        return super().create(validated_data)
    
    def delete(self, instance):
        # 刪除與該 Category 綁定的所有 Transaction
        instance.transactions.all().delete()
        # 刪除該 Category
        instance.delete()
    


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # 僅允許讀取的使用者字段
    category = serializers.CharField()  # 接收 category 名稱（string）

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type', 'amount', 'date', 'description']

    def validate(self, data):
        """
        確認 category 名稱並將其轉換為 Category 實例，如果不存在則創建一個新的。
        """
        category_name = data.get("category")
        if isinstance(category_name, str):
            user = self.context['request'].user  # 獲取當前用戶
            # 嘗試找到對應的 category，若不存在則創建
            category_instance, created = Category.objects.get_or_create(name=category_name, user=user)
            data["category"] = category_instance  # 將 category 替換為實例
        return data

    def create(self, validated_data):
        """
        確保 transaction 是針對登錄的使用者，並創建交易記錄
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)




class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'month', 'content']
        read_only_fields = ['id']  # id 只讀

    def create(self, validated_data):
        # 自動將當前用戶設置為 user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)