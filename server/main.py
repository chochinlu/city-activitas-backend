from fastapi import FastAPI, HTTPException, APIRouter
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

app = FastAPI()

# routers
idle_assets_router = APIRouter(prefix="/api/v1/idle", tags=["閒置資產"])
active_cases_router = APIRouter(prefix="/api/v1/cases", tags=["進行中案件"])
activated_assets_router = APIRouter(prefix="/api/v1/activated", tags=["已活化資產"])

# 閒置資產相關路由
@idle_assets_router.get("")  # /api/v1/idle
async def get_idle_assets():
    response = supabase.table('test_idle_assets_view').select("*").execute()
    return response.data

@idle_assets_router.get("/lands")  # /api/v1/idle/lands
async def get_idle_land_assets():
    response = supabase.table('test_idle_land_assets_view').select("*").execute()
    return response.data

@idle_assets_router.get("/buildings")  # /api/v1/idle/buildings
async def get_idle_building_assets():
    response = supabase.table('test_idle_building_assets').select("*").execute()
    return response.data

# 進行中案件相關路由
@active_cases_router.get("")  # /api/v1/cases
async def get_cases():
    response = supabase.table('test_asset_cases_view').select("*").execute()
    return response.data

@active_cases_router.get("/{case_id}/tasks")  # /api/v1/cases/{case_id}/tasks
async def get_case_tasks(case_id: int):
    response = supabase.table('test_case_tasks_view').select("*").eq("案件ID", case_id).execute()
    return response.data

@active_cases_router.get("/{case_id}/meetings")  # /api/v1/cases/{case_id}/meetings
async def get_case_meetings(case_id: int):
    response = supabase.table('test_case_meeting_conclusions') \
        .select("*") \
        .eq("case_id", case_id) \
        .order('meeting_date', desc=True) \
        .execute()
    return response.data

@active_cases_router.get("/{case_id}/meetings/{meeting_id}")  # /api/v1/cases/{case_id}/meetings/{meeting_id}
async def get_case_meeting(case_id: int, meeting_id: int):
    response = supabase.table('test_case_meeting_conclusions') \
        .select("*") \
        .eq("case_id", case_id) \
        .eq("id", meeting_id) \
        .single() \
        .execute()
    return response.data

@active_cases_router.post("/{case_id}/meetings")  # /api/v1/cases/{case_id}/meetings
async def create_case_meeting(case_id: int, meeting_date: str, content: str):
    response = supabase.table('test_case_meeting_conclusions') \
        .insert({
            "case_id": case_id,
            "meeting_date": meeting_date,
            "content": content
        }).execute()
    return response.data

# 已活化資產相關路由
@activated_assets_router.get("")  # /api/v1/activated
async def get_activated_assets():
    response = supabase.table('test_activated_assets_view').select("*").execute()
    return response.data

# include routers
app.include_router(idle_assets_router)
app.include_router(active_cases_router)
app.include_router(activated_assets_router)

# root
@app.get("/")
def read_root():
    return {"message": "Hello CityActivitas!"}

# signup
@app.post("/signup")
async def signup(email: str, password: str):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if response.user:
            return {
                "message": "Registration successful",
                "user": response.user
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Registration failed"
            )
            
    except Exception as e:
        print(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Signup failed: {str(e)}"
        )

# login and get token
@app.post("/login")
async def login(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            return {
                "access_token": response.session.access_token,
                "user": response.user
            }
        else:
            raise HTTPException(
                status_code=400, 
                detail="Invalid credentials"
            )
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Login failed: {str(e)}"
        )