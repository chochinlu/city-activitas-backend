from fastapi import APIRouter
from supabase import Client

router = APIRouter(prefix="/api/v1/cases", tags=["進行中案件"])

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

    return router 