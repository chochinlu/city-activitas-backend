from fastapi import APIRouter
from supabase import Client

# 建立路由器
router = APIRouter(prefix="/api/v1/idle", tags=["閒置資產"])

def init_router(supabase: Client) -> APIRouter:
    
    @router.get("")  # /api/v1/idle
    async def get_idle_assets():
        response = supabase.table('test_idle_assets_view').select("*").execute()
        return response.data

    @router.get("/lands")  # /api/v1/idle/lands
    async def get_idle_land_assets():
        response = supabase.table('test_idle_land_assets_view').select("*").execute()
        return response.data

    @router.get("/buildings")  # /api/v1/idle/buildings
    async def get_idle_building_assets():
        response = supabase.table('test_idle_building_assets').select("*").execute()
        return response.data

    return router 