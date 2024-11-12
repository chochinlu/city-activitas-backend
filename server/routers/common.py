from fastapi import APIRouter
from supabase import Client
from typing import Optional
from datetime import datetime
from fastapi import HTTPException 
from pydantic import BaseModel

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

    # 定義請求模型
    class AgencyCreate(BaseModel):
        name: str                   # 機關名稱
        note: Optional[str] = None  # 備註

    class AgencyUpdate(BaseModel):
        name: Optional[str] = None
        note: Optional[str] = None
  
    class UsageTypeCreate(BaseModel):
        name: str                   # 使用類型名稱
        note: Optional[str] = None  # 備註

    class UsageTypeUpdate(BaseModel):
        name: Optional[str] = None
        note: Optional[str] = None


    @router.post("/agencies", status_code=201)
    async def create_agency(agency: AgencyCreate):
        try:
            current_time = datetime.now().isoformat()
            agency_data = agency.dict()
            agency_data["created_at"] = current_time
            agency_data["updated_at"] = current_time
            
            response = supabase.table('test_agencies').insert(agency_data).execute()
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/agencies/{agency_id}")
    async def update_agency(agency_id: int, agency: AgencyUpdate):
        try:
            current_time = datetime.now().isoformat()
            update_data = agency.dict(exclude_unset=True)
            update_data["updated_at"] = current_time
            
            if update_data:
                response = supabase.table('test_agencies').update(update_data).eq('id', agency_id).execute()
                if not response.data:
                    raise HTTPException(status_code=404, detail="找不到指定的機關")
                return response.data[0]
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/agencies/{agency_id}")
    async def delete_agency(agency_id: int):
        try:
            # 檢查是否有相關的閒置資產
            assets = supabase.table('test_assets').select("id").eq('agency_id', agency_id).execute()
            if assets.data:
                raise HTTPException(status_code=400, detail="此機關還有相關的閒置資產，無法刪除")
            
            response = supabase.table('test_agencies').delete().eq('id', agency_id).execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="找不到指定的機關")
                
            return {"message": "機關刪除成功", "agency_id": agency_id}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

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

    @router.post("/usage-types", status_code=201)
    async def create_usage_type(usage_type: UsageTypeCreate):
        try:
            usage_type_data = usage_type.dict()
            response = supabase.table('test_usage_types').insert(usage_type_data).execute()
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/usage-types/{usage_type_id}")
    async def update_usage_type(usage_type_id: int, usage_type: UsageTypeUpdate):
        try:
            update_data = usage_type.dict(exclude_unset=True)
            if update_data:
                response = supabase.table('test_usage_types').update(update_data).eq('id', usage_type_id).execute()
                if not response.data:
                    raise HTTPException(status_code=404, detail="找不到指定的使用類型")
                return response.data[0]
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/usage-types/{usage_type_id}")
    async def delete_usage_type(usage_type_id: int):
        try:
            # 檢查是否有相關的閒置資產活化案例
            cases = supabase.table('test_asset_cases').select("id").eq('purpose_type_id', usage_type_id).execute()
            if cases.data:
                raise HTTPException(status_code=400, detail="此使用類型還有相關的活化案例，無法刪除")
            
            # 檢查是否有相關的已活化資產
            activated_assets = supabase.table('test_activated_assets').select("id").eq('usage_type_id', usage_type_id).execute()
            if activated_assets.data:
                raise HTTPException(status_code=400, detail="此使用類型還有相關的已活化資產，無法刪除")
            
            response = supabase.table('test_usage_types').delete().eq('id', usage_type_id).execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="找不到指定的使用類型")
                
            return {"message": "使用類型刪除成功", "usage_type_id": usage_type_id}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

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

    @router.get("/case-statuses")
    async def get_case_statuses():
        return [
            {"id": "核准經費中", "name": "核准經費中"},
            {"id": "進行中", "name": "進行中"},
            {"id": "完成招商", "name": "完成招商"},
            {"id": "工程中", "name": "工程中"},
            {"id": "工程期安排中", "name": "工程期安排中"},
            {"id": "尚未規劃", "name": "尚未規劃"},
            {"id": "還沒找到地", "name": "還沒找到地"},
            {"id": "評估中", "name": "評估中"},
            {"id": "評估場域", "name": "評估場域"},
            {"id": "評估招商", "name": "評估招商"},
            {"id": "已簽准", "name": "已簽准"}
        ]

    return router 