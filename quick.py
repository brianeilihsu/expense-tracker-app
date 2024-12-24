import csv
import os
import django
from datetime import datetime
from decimal import Decimal  # 用於處理金額數字

# 設置 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')  # 替換為你的專案名稱
django.setup()

from expenses.models import Transaction, Category  # 替換為你的應用名稱和模型名稱
from django.contrib.auth.models import User

# 讀取 CSV 並導入數據
def import_csv_to_database(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            user = User.objects.get(username='dilen')  # 替換為正確的使用者名稱

            # 嘗試找到對應的 category，若不存在則創建
            category, created = Category.objects.get_or_create(name=row['Category'], user=user)

            # 解析日期
            try:
                parsed_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()  # 將字符串轉換為日期
            except ValueError as e:
                print(f"Error parsing date {row['Date']}: {e}")
                continue
            # 解析金額
            try:
                amount = Decimal(row['Amount'])  # 將金額轉換為 Decimal
            except ValueError as e:
                print(f"Error parsing amount {row['Amount']}: {e}")
                continue

            # 創建 Transaction
            transaction = Transaction.objects.create(
                user=user,
                category=category,
                transaction_type=row['Transaction_type'],
                amount=amount,  # 傳入轉換後的 Decimal 金額
                date=parsed_date,
                description=row['Description']
            )
            print(f"Imported Transaction: {transaction.id}")
# 呼叫函數
import_csv_to_database('expense_data.csv')
