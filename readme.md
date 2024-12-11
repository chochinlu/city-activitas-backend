# CityActivitas Backend

[DB Diagram](https://dbdiagram.io/d/%E8%B2%A1%E7%A8%85%E5%B1%80%E8%B3%87%E7%94%A2-67237c4ab1b39dd858136bec)


## 專案結構

後端 REST API 伺服器的程式碼位於 `server` 資料夾中。此伺服器使用 [FastAPI](https://fastapi.tiangolo.com/) 框架開發,並透過 Docker 容器化部署。


## Run

需要先設置 `.env` 檔案, **放置到 `server` 資料夾** 下: 

```env
SUPABASE_URL=<supabase url>
SUPABASE_ANON_KEY=<supabase anon key>
SUPABASE_SERVICE_ROLE_KEY=<supabase admin key>
```

然後: 

```bash
docker compose up -d
```


API 文件: http://localhost:8000/docs

API service: http://localhost:8000