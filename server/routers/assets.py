from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from supabase import Client
from dependencies.auth import get_auth_dependency

# 定義請求模型
class AssetUpdate(BaseModel):
    type: Optional[str] = None                # 資產種類：土地或建物
    agency_id: Optional[int] = None           # 管理機關ID
    district_id: Optional[int] = None         # 行政區ID
    section: Optional[str] = None             # 地段
    address: Optional[str] = None             # 地址
    coordinates: Optional[tuple[float, float]] = None          # 定位座標
    area_coordinates: Optional[list[tuple[float, float]]] = None  # 區域座標組
    target_name: Optional[str] = None         # 標的名稱
    status: Optional[str] = None              # 狀態

class LandDetailUpdate(BaseModel):
    lot_number: Optional[str] = None          # 地號，例如：80-8、81-1
    land_type: Optional[str] = None           # 土地種類，例如：市有土地、國有土地
    area: Optional[float] = None              # 面積(平方公尺)，例如：7826
    zone_type: Optional[str] = None           # 使用分區，例如：學校用地、保護區
    land_use: Optional[str] = None            # 土地用途，例如：特定目的事業用地
    current_status: Optional[str] = None      # 現況，例如：空置
    vacancy_rate: Optional[int] = None        # 空置比例，例如：100
    note: Optional[str] = None                # 備註，例如：六甲國小大丘分班(已裁併校)

class BuildingDetailUpdate(BaseModel):
    building_number: Optional[str] = None      # 建號，例如：歸仁北段6932建號
    building_type: Optional[str] = None        # 建物種類，例如：市有建物
    floor_area: Optional[str] = None           # 樓地板面積，例如：2樓:3729.7 3樓:3426.2
    zone_type: Optional[str] = None            # 使用分區，例如：住宅區、商業區
    land_use: Optional[str] = None             # 土地用途，例如：乙種建築用地
    current_status: Optional[str] = None       # 現況，例如：空置、部分空置
    vacancy_rate: Optional[int] = None         # 空置比例，例如：100
    note: Optional[str] = None                 # 備註，例如：2樓空置、3樓部分空間約400坪提供給使用

router = APIRouter(prefix="/api/v1/assets", tags=["資產"])

def init_router(supabase: Client) -> APIRouter:
    verify_token = get_auth_dependency(supabase)

    @router.patch("/{asset_id}", dependencies=[Depends(verify_token)])
    async def update_asset(asset_id: int, asset: AssetUpdate):
        """
        更新資產主要資料
        
        範例:
        ```json
        {
            "address": "新地址",
            "status": "已活化",
            "coordinates": [120.123, 23.456]
        }
        ```
        """
        try:
            # 1. 檢查資產是否存在
            existing_asset = supabase.table('test_assets').select("*").eq('id', asset_id).execute()
            if not existing_asset.data:
                raise HTTPException(status_code=404, detail="找不到指定的資產")
            
            # 2. 準備更新資料
            update_data = {}
            
            # 只更新有提供的欄位
            if asset.type is not None:
                update_data["type"] = asset.type
            if asset.agency_id is not None:
                update_data["agency_id"] = asset.agency_id
            if asset.district_id is not None:
                update_data["district_id"] = asset.district_id
            if asset.section is not None:
                update_data["section"] = asset.section
            if asset.address is not None:
                update_data["address"] = asset.address
            if asset.target_name is not None:
                update_data["target_name"] = asset.target_name
            if asset.status is not None:
                update_data["status"] = asset.status
                
            # 處理座標資料
            if asset.coordinates is not None:
                update_data["coordinates"] = f"({asset.coordinates[0]},{asset.coordinates[1]})"
            
            if asset.area_coordinates is not None:
                points = [f"({x},{y})" for x, y in asset.area_coordinates]
                if points[0] != points[-1]:
                    points.append(points[0])
                update_data["area_coordinates"] = f"({','.join(points)})"
            
            # 加入更新時間
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 3. 更新資產資料
            if update_data:
                response = supabase.table('test_assets').update(update_data).eq('id', asset_id).execute()
                return {"message": "資產更新成功", "asset_id": asset_id}
            else:
                return {"message": "沒有資料需要更新", "asset_id": asset_id}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/lands/{land_id}", dependencies=[Depends(verify_token)])
    async def update_land_detail(land_id: int, land: LandDetailUpdate):
        """
        更新土地明細資料
        
        範例:
        ```json
        {
            "area": 8000,
            "current_status": "部分空置",
            "vacancy_rate": 50
        }
        ```
        """
        try:
            # 1. 檢查土地明細是否存在
            existing_land = supabase.table('test_land_details').select("*").eq('id', land_id).execute()
            if not existing_land.data:
                raise HTTPException(status_code=404, detail="找不到指定的土地明細")
            
            # 2. 準備更新資料
            update_data = land.dict(exclude_unset=True)  # 只包含有設定值的欄位
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 3. 更新土地明細資料
            response = supabase.table('test_land_details').update(update_data).eq('id', land_id).execute()
            
            return {"message": "土地明細更新成功", "land_id": land_id}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/buildings/{building_id}", dependencies=[Depends(verify_token)])
    async def update_building_detail(building_id: int, building: BuildingDetailUpdate):
        """
        更新建物明細資料
        
        範例:
        ```json
        {
            "current_status": "部分空置",
            "vacancy_rate": 50,
            "note": "2樓空置、3樓部分空間約400坪提供給使用"
        }
        ```
        """
        try:
            # 1. 檢查建物明細是否存在
            existing_building = supabase.table('test_building_details').select("*").eq('id', building_id).execute()
            if not existing_building.data:
                raise HTTPException(status_code=404, detail="找不到指定的建物明細")
            
            # 2. 準備更新資料
            update_data = building.dict(exclude_unset=True)  # 只包含有設定值的欄位
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 3. 更新建物明細資料
            response = supabase.table('test_building_details').update(update_data).eq('id', building_id).execute()
            
            return {"message": "建物明細更新成功", "building_id": building_id}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    return router 