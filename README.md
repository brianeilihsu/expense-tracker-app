# Expense Tracker App - TrackSmart

**TrackSmart** 是一個簡單直觀的記帳應用程式，旨在幫助使用者輕鬆追蹤收入與支出，並結合數據分析工具，快速了解個人財務狀況。

## 功能特色

1. **記錄收入與支出**  
   - 使用者可以輸入每筆交易的日期、金額，並加上分類標籤（例如餐飲、交通等）。
   - 支援新增和刪除記錄。

2. **消費分析**  
   - 提供直觀的消費圓餅圖，展示各分類的花費情況。
   - 顯示總資產餘額，幫助快速掌握財務狀況。

3. **AI 驅動的財務建議**  
   - 結合 OpenAI，為使用者提供期間收入與支出的智能分析與建議。

---

## 系統架構

- **前端**: React
- **後端**: Django + REST API
- **資料庫**: PostgreSQL
- **雲端服務**: AWS 部署
- **分析工具**: OpenAI API

---

## 安裝與啟動

### 環境需求

- Python 3.10 或以上版本
- Node.js 16 或以上版本
- PostgreSQL 14 或以上版本

### 本地運行步驟

1. **克隆專案**
   ```bash
   git clone https://github.com/brianeilihsu/expense-tracker-app.git
   cd expense-tracker-app
   ```

2. **後端設定**
   - 建立虛擬環境：
     ```bash
     python -m venv django-venv
     source django-venv/bin/activate    # Mac/Linux
     django-venv\Scripts\activate       # Windows
     ```
   - 安裝依賴：
     ```bash
     pip install -r requirements.txt
     ```
   - 運行伺服器：
     ```bash
     python manage.py migrate
     python manage.py runserver
     ```

3. **前端設定**
   - 安裝依賴：
     ```bash
     cd frontend
     npm install
     ```
   - 啟動開發伺服器：
     ```bash
     npm start
     ```

4. **訪問應用**
   - 後端 API: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
   - 前端 UI: [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

---

## 使用方式

1. 註冊並登入帳戶。
2. 在首頁新增收入或支出的記錄。
3. 查看即時更新的消費圓餅圖和總資產餘額。
4. 點擊 AI 分析，獲取專業建議。

---

## 未來改進方向

- 增加多語言支援。
- 提供匯出報表功能。
- 改善 AI 建議的準確性，增加個性化分析。

---
