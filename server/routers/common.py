from fastapi import APIRouter
from supabase import Client

router = APIRouter(prefix="/api/v1/common", tags=["共用資料"])

def init_router(supabase: Client) -> APIRouter:

    @router.get("/agencies")
    async def get_agencies():
        response = supabase.table('test_agencies').select("*").execute()
        return response.data

    @router.get("/agencies/{id}")
    async def get_agency(id: int):
        response = supabase.table('test_agencies').select("*").eq('id', id).single().execute()
        return response.data

    @router.get("/districts")
    async def get_districts():
        response = supabase.table('test_districts').select("*").execute()
        return response.data

    @router.get("/districts/{id}")
    async def get_district(id: int):
        response = supabase.table('test_districts').select("*").eq('id', id).single().execute()
        return response.data

    @router.get("/usage-types")
    async def get_usage_types():
        response = supabase.table('test_usage_types').select("*").execute()
        return response.data

    @router.get("/usage-types/{id}")
    async def get_usage_type(id: int):
        response = supabase.table('test_usage_types').select("*").eq('id', id).single().execute()
        return response.data

    @router.get("/asset-statuses")
    async def get_asset_statuses():
        return [
            {"id": "未活化", "name": "未活化"},
            {"id": "活化中", "name": "活化中"},
            {"id": "已活化", "name": "已活化"}
        ]

    @router.get("/asset-types")
    async def get_asset_types():
        return [
            {"id": "土地", "name": "土地"},
            {"id": "建物", "name": "建物"}
        ]

    return router 