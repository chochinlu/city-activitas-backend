from fastapi import APIRouter, HTTPException
from supabase import Client
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/cases", tags=["進行中案件"])

# 定義請求模型
class CaseCreate(BaseModel):
    asset_id: Optional[int] = None          # 關聯資產 ID（選擇性）
    name: str                               # 案件名稱
    purpose: Optional[str] = None           # 活化目標說明
    purpose_type_id: Optional[int] = None   # 活化目標類型 ID
    status: str                             # 案件狀態

def init_router(supabase: Client) -> APIRouter:

    @router.get("")  # /api/v1/cases
    async def get_cases():
        response = supabase.table('test_asset_cases_view').select("*").execute()
        return response.data

    @router.get("/{case_id}/tasks")  # /api/v1/cases/{case_id}/tasks
    async def get_case_tasks(case_id: int):
        response = supabase.table('test_case_tasks_view').select("*").eq("案件ID", case_id).execute()
        return response.data

    @router.get("/{case_id}/meetings")  # /api/v1/cases/{case_id}/meetings
    async def get_case_meetings(case_id: int):
        response = supabase.table('test_case_meeting_conclusions') \
            .select("*") \
            .eq("case_id", case_id) \
            .order('meeting_date', desc=True) \
            .execute()
        return response.data

    @router.get("/{case_id}/meetings/{meeting_id}")  # /api/v1/cases/{case_id}/meetings/{meeting_id}
    async def get_case_meeting(case_id: int, meeting_id: int):
        response = supabase.table('test_case_meeting_conclusions') \
            .select("*") \
            .eq("case_id", case_id) \
            .eq("id", meeting_id) \
            .single() \
            .execute()
        return response.data

    @router.post("/{case_id}/meetings")  # /api/v1/cases/{case_id}/meetings
    async def create_case_meeting(case_id: int, meeting_date: str, content: str):
        response = supabase.table('test_case_meeting_conclusions') \
            .insert({
                "case_id": case_id,
                "meeting_date": meeting_date,
                "content": content
            }).execute()
        return response.data


    @router.post("")  # /api/v1/cases
    async def create_case(case: CaseCreate):
        try:
            current_time = datetime.now().isoformat()
            case_data = case.dict()
            case_data["created_at"] = current_time
            case_data["updated_at"] = current_time
            
            # 如果有提供 asset_id，檢查資產是否存在並更新其狀態
            if case.asset_id:
                # 檢查資產是否存在
                asset = supabase.table('test_assets').select("id").eq('id', case.asset_id).single().execute()
                if not asset.data:
                    raise HTTPException(status_code=404, detail="找不到指定的資產")
                
                # 更新資產狀態為「活化中」
                supabase.table('test_assets').update({
                    "status": "活化中",
                    "updated_at": current_time
                }).eq('id', case.asset_id).execute()
            
            # 檢查活化目標類型是否存在（如果有提供）
            if case.purpose_type_id:
                usage_type = supabase.table('test_usage_types').select("id").eq('id', case.purpose_type_id).single().execute()
                if not usage_type.data:
                    raise HTTPException(status_code=404, detail="找不到指定的使用類型")
            
            # 新增案件
            response = supabase.table('test_asset_cases').insert(case_data).execute()
            
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router 


