from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from datetime import datetime

from routers import idle_assets, active_cases, activated_assets, auth, common

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

app = FastAPI()

# health check
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",  # 可從環境變數或配置檔讀取
        "database": "connected" if supabase else "disconnected"
    }

# include routers
app.include_router(idle_assets.init_router(supabase))
app.include_router(active_cases.init_router(supabase))
app.include_router(activated_assets.init_router(supabase))
app.include_router(auth.init_router(supabase))
app.include_router(common.init_router(supabase))
