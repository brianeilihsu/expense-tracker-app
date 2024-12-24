from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Account, Category, Transaction, Report
from .serializers import UserSerializer, AccountSerializer, CategorySerializer, TransactionSerializer, ReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date, timedelta
import openai

# User View
class UserListView(mixins.ListModelMixin,
                   generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UserDetailView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Account View
class AccountListView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 僅返回當前用戶的 Account
        return Account.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AccountDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Category View
class CategoryListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 僅返回當前用戶的 Category
        return Category.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CategoryDetailView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 僅返回當前用戶的 Category
        return Category.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        category = self.get_object()  # 獲取要刪除的 Category
        # 使用 serializer 的 delete 方法刪除
        serializer = self.get_serializer()
        serializer.delete(category)
        return Response({"message": "Category and related transactions deleted successfully."}, status=204)


# Transaction View
class TransactionListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter transactions to only include those of the authenticated user
        queryset = Transaction.objects.filter(user=self.request.user)
        year_month = self.request.query_params.get('date')  # 假設參數名為 `date`
        if year_month:
            try:
                # 將 `yyyy-mm` 解析為年份和月份
                year, month = map(int, year_month.split('-'))
                queryset = queryset.filter(date__year=year, date__month=month)
            except ValueError:
                # 如果解析失敗，返回空的查詢集
                queryset = queryset.none()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TransactionDetailView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GenerateMonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 獲取請求數據
        date_str = request.data.get("date")  # 格式：YYYY-MM
        if not date_str:
            return Response({"error": "Month is required in the format YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)

        # 驗證月份格式並轉換為 date 類型
        try:
            target_date = datetime.strptime(date_str, "%Y-%m").date()
        except ValueError:
            return Response({"error": "Invalid month format. Use YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 獲取當前日期
        today = date.today()
        first_day_of_next_month = (today.replace(day=1) + timedelta(days=31)).replace(day=1)

        # 如果目標月份大於當前月份或當前日期未超過目標月份的最後一天，返回錯誤
        if target_date >= first_day_of_next_month:
            return Response({"error": "Cannot generate report for future months."}, status=status.HTTP_400_BAD_REQUEST)

        if target_date.year == today.year and target_date.month == today.month:
            return Response({"error": "Cannot generate report for the current month until it ends."}, status=status.HTTP_400_BAD_REQUEST)

        # 獲取當前用戶
        user = request.user

        # 檢查該月份的報告是否已存在
        if Report.objects.filter(user=user, month=target_date).exists():
           return Response({"error": "Report for the specified month already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # 查詢指定月份的交易數據
        transactions = Transaction.objects.filter(
            user=user,
            date__year=target_date.year,
            date__month=target_date.month
        )

        if not transactions.exists():
            return Response({"error": "No transactions found for the specified month."}, status=status.HTTP_404_NOT_FOUND)

        # 格式化交易數據
        transaction_data = [
            {
                "date": txn.date.strftime("%Y-%m-%d"),
                "amount": txn.amount,
                "type": txn.transaction_type,
                "category": txn.category.name,
                "description": txn.description,
            }
            for txn in transactions
        ]

        openai.api_key = "openai api key##"  # 替換為你的 OpenAI API Key
        messages = [
            {"role": "system", "content": "你是一個繁體中文財務分析助手，負責生成用戶的財務報告且沒有錯字與沒意義的字符。"},
            {"role": "user", "content": f"請分析用戶記帳數據，以台幣作為單位，並生成200字的財務報告，如果他有很多非必要的支出例如娛樂或花費高昂的餐費，請以嘲諷的口吻生成文字報告，相反的如果他有良好的金錢使用觀念請誇獎他：{transaction_data}"}
        ]

        # 發送到 ChatGPT 進行分析
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages
            )
            # 提取生成的内容
            report_content = response['choices'][0]['message']['content']
            print("生成的財務報告：", report_content)
        except Exception as e:
            print(f"分析失敗: {str(e)}")
        
        # 將分析結果存入 Report 模型
        report, created = Report.objects.update_or_create(
            user=user,
            month=target_date,
            defaults={"content": report_content}
        )

        # 使用序列化器返回生成的報告
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetMonthlyReportView(APIView):
    permission_classes=[IsAuthenticated]
        
    def get(self, request, *args, **kwargs):
        # 獲取請求數據
        date_str = request.query_params.get("date")  # 格式：YYYY-MM
        if not date_str:
            return Response({"error": "Month is required in the format YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)

        # 驗證月份格式並轉換為 date 類型
        try:
            target_date = datetime.strptime(date_str, "%Y-%m").date()
            print(target_date)
        except ValueError:
            return Response({"error": "Invalid month format. Use YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)

        # 獲取當前用戶
        user = request.user

        # 查詢該月份是否存在報告
        try:
            report = Report.objects.get(user=user, month=target_date)
            
        except Report.DoesNotExist:
            return Response({"error": "No report found for the specified month."}, status=status.HTTP_404_NOT_FOUND)

        # 使用序列化器返回報告數據
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)