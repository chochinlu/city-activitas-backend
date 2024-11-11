from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from supabase import Client

router = APIRouter(prefix="/api/v1/idle", tags=["閒置資產"])

# 定義請求模型
class LandDetailCreate(BaseModel):
    lot_number: str                         # 地號，例如：80-8、81-1
    land_type: Optional[str] = None         # 土地種類，例如：市有土地、國有土地
    area: Optional[float] = None            # 面積(平方公尺)，例如：7826
    zone_type: Optional[str] = None         # 使用分區，例如：學校用地、保護區
    land_use: Optional[str] = None          # 土地用途，例如：特定目的事業用地
    current_status: Optional[str] = None    # 現況，例如：空置
    vacancy_rate: Optional[int] = None      # 空置比例，例如：100
    note: Optional[str] = None              # 備註，例如：六甲國小大丘分班(已裁併校)

class BuildingDetailCreate(BaseModel):
    building_number: str                    # 建號，例如：歸仁北段6932建號
    building_type: Optional[str] = None     # 建物種類，例如：市有建物
    floor_area: Optional[str] = None        # 樓地板面積，例如：2樓:3729.7 3樓:3426.2
    zone_type: Optional[str] = None         # 使用分區，例如：住宅區、商業區
    land_use: Optional[str] = None          # 土地用途，例如：乙種建築用地
    current_status: Optional[str] = None    # 現況，例如：空置、部分空置
    vacancy_rate: Optional[int] = None      # 空置比例，例如：100
    note: Optional[str] = None              # 備註，例如：2樓空置、3樓部分空間約400坪提供給使用

class AssetCreate(BaseModel):
    type: str                               # 資產種類：土地或建物
    agency_id: int                          # 管理機關ID
    district_id: int                        # 行政區ID
    section: str                            # 地段，例如：大丘園段、田寮段
    address: Optional[str] = None           # 地址，例如：錦仁區和平南街9號
    coordinates: Optional[tuple[float, float]] = None          # 定位座標
    area_coordinates: Optional[list[tuple[float, float]]] = None  # 區域座標組
    target_name: Optional[str] = None       # 標的名稱，例如：歸仁市場2, 3樓
    status: str = "未活化"                  # 狀態：已經活化、活化中、未活化
    land_details: Optional[list[LandDetailCreate]] = None      # 土地明細列表
    building_details: Optional[list[BuildingDetailCreate]] = None  # 建物明細列表

def init_router(supabase: Client) -> APIRouter:
    
    @router.get("")  # /api/v1/idle
    async def get_idle_assets():
        response = supabase.table('test_idle_assets_view').select("*").execute()
        return response.data

    @router.get("/lands")  # /api/v1/idle/lands
    async def get_idle_land_assets():
        response = supabase.table('test_idle_land_assets_view').select("*").execute()
        return response.data
      
    @router.get("/lands/{asset_id}")  # /api/v1/idle/lands/{asset_id}
    async def get_idle_land_asset_by_id(asset_id: int):
        try:
            response = supabase.table('test_idle_land_assets_view').select("*").eq('資產ID', asset_id).execute()
            
            if not response.data:
                raise HTTPException(status_code=404, detail="找不到指定的閒置土地資產")
                
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/buildings")  # /api/v1/idle/buildings
    async def get_idle_building_assets():
        response = supabase.table('test_idle_building_assets').select("*").execute()
        return response.data

    @router.get("/buildings/{asset_id}")  # /api/v1/idle/buildings/{asset_id}
    async def get_idle_building_asset_by_id(asset_id: int):
        try:
            response = supabase.table('test_idle_building_assets').select("*").eq('id', asset_id).execute()
            
            if not response.data:
                raise HTTPException(status_code=404, detail="找不到指定的閒置建物資產")
                
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/assets", status_code=201)
    async def create_idle_asset(asset: AssetCreate):
        try:
            # 1. 新增主要資產
            current_time = datetime.now().isoformat()
            
            # 處理座標格式 - point 格式應為: (x,y)
            coordinates = f"({asset.coordinates[0]},{asset.coordinates[1]})" if asset.coordinates else None
            
            # 處理多邊形座標格式 - polygon 格式應為: ((x1,y1),(x2,y2),(x3,y3),...)
            area_coordinates = None
            if asset.area_coordinates:
                # 將座標點轉換為 PostgreSQL 的 polygon 格式
                points = [f"({x},{y})" for x, y in asset.area_coordinates]
                # 確保多邊形封閉（首尾相接）
                if points[0] != points[-1]:
                    points.append(points[0])
                area_coordinates = f"({','.join(points)})"

            asset_data = {
                "type": asset.type,
                "agency_id": asset.agency_id,
                "district_id": asset.district_id,
                "section": asset.section,
                "address": asset.address,
                "coordinates": coordinates,
                "area_coordinates": area_coordinates,
                "target_name": asset.target_name,
                "status": asset.status,
                "created_at": current_time,
                "updated_at": current_time
            }
            
            asset_response = supabase.table('test_assets').insert(asset_data).execute()
            asset_id = asset_response.data[0]['id']
            
            # 2. 根據資產類型新增詳細資料
            if asset.type == "土地" and asset.land_details:
                for land_detail in asset.land_details:
                    land_data = land_detail.dict()
                    land_data["asset_id"] = asset_id
                    land_data["created_at"] = current_time
                    land_data["updated_at"] = current_time
                    supabase.table('test_land_details').insert(land_data).execute()
                    
            elif asset.type == "建物" and asset.building_details:
                for building_detail in asset.building_details:
                    building_data = building_detail.dict()
                    building_data["asset_id"] = asset_id
                    building_data["created_at"] = current_time
                    building_data["updated_at"] = current_time
                    supabase.table('test_building_details').insert(building_data).execute()
            
            return {"message": "閒置資產新增成功", "asset_id": asset_id}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router 
  
  
  