import csv
import os
import django

# 設置 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '..\home.settings')  # 替換為你的專案名稱
django.setup()

from expenses.models import Transaction, Category  # 替換為你的應用名稱和模型名稱
from django.contrib.auth.models import User

# 讀取 CSV 並導入數據
def import_csv_to_database(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            user = User.objects.get(username='xiaofei')  # 替換為正確的使用者名稱

            # 嘗試找到對應的 category，若不存在則創建
            category, created = Category.objects.get_or_create(name=row['category'], user=user)

            # 創建 Transaction
            transaction = Transaction.objects.create(
                user=user,
                category=category,
                transaction_type=row['transaction_type'],
                amount=row['amount'],
                date=row['date'],
                description=row['description']
            )
            print(f"Imported Transaction: {transaction.id}")

# 呼叫函數
import_csv_to_database('黃曉菲.csv')
