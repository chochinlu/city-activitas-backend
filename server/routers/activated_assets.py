from fastapi import APIRouter
from supabase import Client

# 建立路由器
router = APIRouter(prefix="/api/v1/activated", tags=["已活化資產"])

def init_router(supabase: Client) -> APIRouter:

    @router.get("")  # /api/v1/activated
    async def get_activated_assets():
        response = supabase.table('test_activated_assets_view').select("*").execute()
        return response.data

    return router 