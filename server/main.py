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


@app.get("/assets")
async def get_assets():
    response = supabase.table('test_assets').select("*").execute()
    return response.data