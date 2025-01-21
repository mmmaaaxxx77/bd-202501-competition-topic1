# 專案說明

此專案主要提供一個 **文章管理 API**，採用 **Django REST Framework** 並整合 **JWT** 驗證機制，以及以 **drf-yasg** 產生的 **Swagger** UI 供測試 API 之用。搭配 **Django Admin** 則可在後台檢視及管理資料。

---

## 1. 專案任務

- 提供 **CRUD** 文章管理功能（含標題、內文、發文時間等欄位）。
- 透過 **JWT** 驗證確保 API 安全。
- 提供 **Swagger UI** 幫助開發者以圖形化介面測試 API。
- 提供 **Django Admin** 作為後台管理介面，可檢視並操作資料庫內容。

---

## 2. 啟動專案 & 建立超級使用者

1. **使用 Docker Compose 啟動服務**
   - 在專案根目錄執行：
     ```bash
     docker-compose up --build
     ```
   - 預設會先啟動 **db** 服務並等待 **10 秒**（確保資料庫就緒），才會啟動 **web** 服務。

2. **建立超級使用者**  
   - 待容器完成啟動後，另開一個終端機，進入 **web** 容器：
     ```bash
     docker-compose exec web bash
     ```
   - 在容器裡執行：
     ```bash
     python src/manage.py createsuperuser
     ```
   - 輸入帳號與密碼 (可使用 `admin / admin` 測試)。  
   - 完成後即可使用此帳密登入後台。

> **注意：** 若資料庫啟動較慢，需要的等待時間長於 10 秒，可自行在 Dockerfile 或 Docker Compose 中調整等待機制（healthcheck 或 wait-for-it.sh）。

---

## 3. 後台 Admin 與 Swagger 連線方式

- **Admin 後台**  
  瀏覽器進入 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
  使用先前建立的超級使用者帳密 (如 `admin / admin`) 登入。

- **Swagger UI**  
  瀏覽器進入 [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)  
  即可檢視並測試所有公開（或需要 JWT）的 API 端點。

---

## 4. Swagger 測試流程

1. **取得 JWT Token**  
   - 在 Swagger UI 找到 `POST /api/token/` 端點，輸入您在 **createsuperuser** 步驟中設定的使用者帳密，即可取得 `access` 與 `refresh` token。

2. **帶入 Token**  
   - 在 Swagger UI 點擊 **Authorize** 按鈕，輸入 `Bearer <access_token>` 完成授權。  

3. **測試 CRUD API**  
   - `/api/articles/`（GET/POST）或 `/api/articles/{id}/`（GET/POST/PATCH/DELETE）等端點均可帶著 Token 呼叫。

---

## 5. Admin 後台檢視資料

1. 進入 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
2. 使用 `admin / admin` 登入後，即可看到 **Articles** 等模組，點擊即可檢視與編輯資料。

---

### 結語

- 本專案使用 **Django** + **DRF** + **JWT** + **Swagger**（drf-yasg）  
- 建議在 **Docker Compose** 環境中使用時，要注意 **資料庫啟動時間**，本範例中設定了 **等待 10 秒** 才啟動 Web，確保 DB 就緒；若環境或設定不同，請自行調整。  
- 驗證請透過 **JWT** Token 方式完成，並在 **Swagger** UI 上測試各項文章管理功能。  
- 進階管理可透過 **Django Admin** 後台進行。  