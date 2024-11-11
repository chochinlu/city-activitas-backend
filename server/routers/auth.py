from fastapi import APIRouter, HTTPException
from supabase import Client

# 建立路由器
router = APIRouter(tags=["認證"])

def init_router(supabase: Client) -> APIRouter:

    @router.post("/signup")
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

    @router.post("/login")
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

    return router 