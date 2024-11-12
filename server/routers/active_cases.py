from fastapi import APIRouter, HTTPException
from supabase import Client
from datetime import datetime, date
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

class TaskCreate(BaseModel):
    agency_id: int                      # 負責單位(執行機關)
    task_content: str                   # 任務內容
    status: str                         # 進度狀態
    start_date: Optional[date] = None   # 開始執行時間
    complete_date: Optional[date] = None # 實際完成時間
    due_date: Optional[date] = None     # 預期完成時間
    note: Optional[str] = None          # 備註

def init_router(supabase: Client) -> APIRouter:

    @router.get("")  # /api/v1/cases
    async def get_cases():
        response = supabase.table('test_asset_cases_view').select("*").execute()
        return response.data

    @router.get("/{case_id}")  # /api/v1/cases/{case_id}
    async def get_case(case_id: int):
        try:
            # 取得案件基本資料，包含關聯的資產和使用類型資訊
            response = supabase.table('test_asset_cases_view') \
                .select("*") \
                .eq("案件ID", case_id) \
                .single() \
                .execute()
                
            if not response.data:
                raise HTTPException(status_code=404, detail="找不到指定的案件")
                
            case_data = response.data
            
            # 取得案件相關的任務
            tasks = supabase.table('test_case_tasks_view') \
                .select("*") \
                .eq("案件ID", case_id) \
                .execute()
                
            # 取得案件相關的會議結論
            meetings = supabase.table('test_case_meeting_conclusions') \
                .select("*") \
                .eq("case_id", case_id) \
                .order('meeting_date', desc=True) \
                .execute()
                
            # 組合所有資料
            return {
                "case": case_data,
                "tasks": tasks.data,
                "meetings": meetings.data
            }
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))
            
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

    @router.post("/{case_id}/tasks")  # /api/v1/cases/{case_id}/tasks
    async def create_case_task(case_id: int, task: TaskCreate):
        try:
            # 檢查案件是否存在
            case = supabase.table('test_asset_cases').select("id").eq('id', case_id).single().execute()
            if not case.data:
                raise HTTPException(status_code=404, detail="找不到指定的案件")
                
            # 檢查機關是否存在
            agency = supabase.table('test_agencies').select("id").eq('id', task.agency_id).single().execute()
            if not agency.data:
                raise HTTPException(status_code=404, detail="找不到指定的機關")
            
            # 準備任務資料
            current_time = datetime.now().isoformat()
            task_data = task.dict()
            task_data["case_id"] = case_id
            task_data["created_at"] = current_time
            task_data["updated_at"] = current_time
            
            # 新增任務
            response = supabase.table('test_case_tasks').insert(task_data).execute()
            
            return response.data[0]
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

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


