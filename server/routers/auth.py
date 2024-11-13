from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

security = HTTPBearer()

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


    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            # 驗證 JWT token
            user = supabase.auth.get_user(credentials.credentials)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail="無效的認證憑證"
            )

    @router.get("/protected")
    async def protected(user = Depends(verify_token)):
        return {
            "message": "成功訪問受保護的路由",
            "user": user
        }

    return router 