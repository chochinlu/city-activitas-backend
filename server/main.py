from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello CityActivitas!"}

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

# Assets 相關端點
@app.get("/api/v1/assets")  # 取得所有資產
async def get_assets():
    response = supabase.table('test_assets').select("*").execute()
    return response.data

@app.get("/api/v1/assets/{asset_id}")  # 取得特定資產
async def get_asset(asset_id: int):
    response = supabase.table('test_assets').select("*").eq("id", asset_id).execute()
    return response.data

@app.get("/api/v1/assets/idle")  # 取得所有閒置資產
async def get_idle_assets():
    response = supabase.table('test_idle_assets_view').select("*").execute()
    return response.data

@app.get("/api/v1/assets/idle/lands")  # 取得閒置土地資產
async def get_idle_land_assets():
    response = supabase.table('test_idle_land_assets_view').select("*").execute()
    return response.data

@app.get("/api/v1/assets/idle/buildings")  # 取得閒置建物資產
async def get_idle_building_assets():
    response = supabase.table('test_idle_building_assets').select("*").execute()
    return response.data

@app.get("/api/v1/assets/activated")  # 取得已活化資產
async def get_activated_assets():
    response = supabase.table('test_activated_assets_view').select("*").execute()
    return response.data

# Cases 相關端點
@app.get("/api/v1/cases")  # 取得所有案件
async def get_cases():
    response = supabase.table('test_asset_cases_view').select("*").execute()
    return response.data

@app.get("/api/v1/cases/{case_id}/tasks")  # 取得特定案件的任務
async def get_case_tasks(case_id: int):
    response = supabase.table('test_case_tasks_view').select("*").eq("案件ID", case_id).execute()
    return response.data

# 會議記錄相關端點
@app.get("/api/v1/cases/{case_id}/meetings")  # 取得特定案件的所有會議記錄
async def get_case_meetings(case_id: int):
    response = supabase.table('test_case_meeting_conclusions') \
        .select("*") \
        .eq("case_id", case_id) \
        .order('meeting_date', desc=True) \
        .execute()
    return response.data

@app.get("/api/v1/cases/{case_id}/meetings/{meeting_id}")  # 取得特定會議記錄
async def get_case_meeting(case_id: int, meeting_id: int):
    response = supabase.table('test_case_meeting_conclusions') \
        .select("*") \
        .eq("case_id", case_id) \
        .eq("id", meeting_id) \
        .single() \
        .execute()
    return response.data


@app.post("/api/v1/cases/{case_id}/meetings")  # 新增會議記錄
async def create_case_meeting(
    case_id: int,   # 案件ID
    meeting_date: str,  # 會議日期 像是 2024-01-01
    content: str  # 會議內容
):
    response = supabase.table('test_case_meeting_conclusions') \
        .insert({
            "case_id": case_id,
            "meeting_date": meeting_date,
            "content": content
        }).execute()
    return response.data