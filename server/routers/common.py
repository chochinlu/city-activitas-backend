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

    return router 