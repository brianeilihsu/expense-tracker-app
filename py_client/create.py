import requests
#from getpass import getpass
import csv

auth_endpoint = "http://localhost:8000/api/login/" 
username = "chuenna"
password = "123456"

auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password}) 
#print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['access']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://localhost:8000/api/expenses/transactions/" 

    # 讀取 CSV 文件
    csv_file_path = "expense_data.csv"  # 替換為你的 CSV 文件路徑
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        # 遍歷每一行，並發送 POST 請求
        for row in csv_reader:
            # 建構資料結構，根據後端的需求映射字段
            # data = {
            #     "date": row['Date'],  # 替換為 CSV 中的欄位名稱
            #     "category": row['Category'],  # 替換為 CSV 中的欄位名稱
            #     "transaction_type": row['Transaction_type'],  # 假設為固定值
            #     "amount": float(row['Amount']),  # 確保金額為數值
            #     "description": row['Description'],
            # }
            data = {
                "date": row.get('Date'),  # Default if missing
                "category": row.get('Category'),  # Default if missing
                "transaction_type": row.get('Transaction_type'),  # Default if missing
                "amount": float(row.get('Amount')),  # Default to 0 if missing or invalid
                "description": row.get('Description'),
            }
            # 發送請求
            response = requests.post(endpoint, json=data, headers=headers)
            
            # 印出回應（可選）
            if response.status_code == 201:  # 假設成功狀態碼為 201
                print(f"成功新增交易：{response.json()}")
            else:
                print(f"新增失敗，狀態碼：{response.status_code}，內容：{response.json()}")
else:
    print(f"登入失敗，狀態碼：{auth_response.status_code}")