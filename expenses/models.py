from django.contrib.auth.models import User
from django.db import models

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True)  # 建立一對多關係

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(null=False)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 更新 Account balance 的邏輯
        account = Account.objects.get(user=self.user)
        if self.transaction_type == 'income':
            account.balance += self.amount
        else:  # expense
            account.balance -= self.amount
        account.save()
        super().save(*args, **kwargs)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')  # 用戶外鍵關聯
    month = models.DateField()  # 用來表示這份報告屬於哪個月份
    content = models.TextField()  # GPT 生成的文字報告

    def __str__(self):
        return f"{self.content}"

