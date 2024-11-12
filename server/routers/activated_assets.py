from fastapi import APIRouter, HTTPException
from supabase import Client
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/activated", tags=["已活化資產"])

class ActivatedAssetUpdate(BaseModel):
    year: Optional[int] = None                  # 年度
    location: Optional[str] = None              # 地點說明
    is_supplementary: Optional[bool] = None     # 是否為補列
    supplementary_year: Optional[int] = None    # 補列年度
    usage_plan: Optional[str] = None            # 計畫用途
    usage_type_id: Optional[int] = None         # 計畫用途類別
    land_value: Optional[float] = None          # 土地公告現值
    building_value: Optional[float] = None      # 房屋課稅現值
    benefit_value: Optional[float] = None       # 節流效益
    is_counted: Optional[bool] = None           # 列入計算
    note: Optional[str] = None                  # 備註
    status: Optional[str] = None                # 狀態
    start_date: Optional[date] = None           # 活化開始日期
    end_date: Optional[date] = None             # 活化結束日期

def init_router(supabase: Client) -> APIRouter:

    @router.get("")  # /api/v1/activated
    async def get_activated_assets():
        response = supabase.table('test_activated_assets_view').select("*").execute()
        return response.data

    @router.put("/{activated_id}")  # /api/v1/activated/{activated_id}
    async def update_activated_asset(activated_id: int, asset: ActivatedAssetUpdate):
        try:
            # 檢查已活化資產是否存在
            existing_asset = supabase.table('test_activated_assets') \
                .select("*") \
                .eq('id', activated_id) \
                .single() \
                .execute()
                
            if not existing_asset.data:
                raise HTTPException(status_code=404, detail="找不到指定的已活化資產")
            
            # 準備更新資料
            update_data = {k: v for k, v in asset.dict(exclude_unset=True).items() if v is not None}
            if not update_data:
                raise HTTPException(status_code=400, detail="沒有提供要更新的資料")
            
            # 如果有提供 usage_type_id，檢查使用類型是否存在
            if asset.usage_type_id:
                usage_type = supabase.table('test_usage_types') \
                    .select("id") \
                    .eq('id', asset.usage_type_id) \
                    .single() \
                    .execute()
                if not usage_type.data:
                    raise HTTPException(status_code=404, detail="找不到指定的使用類型")
            
            # 更新時間戳記
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 更新已活化資產
            response = supabase.table('test_activated_assets') \
                .update(update_data) \
                .eq('id', activated_id) \
                .execute()
                
            return response.data[0]
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    return router 