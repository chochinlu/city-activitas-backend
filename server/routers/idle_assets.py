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

class BuildingLandDetailCreate(BaseModel):
    lot_number: str                         # 地號，例如：80-8、81-1
    land_type: Optional[str] = None         # 土地種類，例如：市有土地、國有土地
    land_manager: Optional[str] = None     # 土地管理者，例如：臺南市政府

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
    building_land_details: Optional[list[BuildingLandDetailCreate]] = None  # 建物土地明細列表

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
    land_details: Optional[list[LandDetailCreate]] = None      # 土地明細列表
    building_details: Optional[list[BuildingDetailCreate]] = None  # 建物明細列表
    building_land_details: Optional[list[BuildingLandDetailCreate]] = None  # 建物土地明細列表

def init_router(supabase: Client) -> APIRouter:
    
    @router.get("")  # /api/v1/idle
    async def get_idle_assets():
        response = supabase.table('test_idle_assets_view').select("*").execute()
        return response.data

    @router.get("/assets/{asset_id}")  # /api/v1/idle/assets/{asset_id}
    async def get_idle_asset_by_id(asset_id: int):
        try:
            response = supabase.table('test_idle_assets_view').select("*").eq('id', asset_id).execute()
        
            if not response.data:
                raise HTTPException(status_code=404, detail="找不到指定的閒置資產")
                
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

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
            response = supabase.table('test_idle_building_assets').select("*").eq('資產ID', asset_id).execute()
            
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
                    
            elif asset.type == "建物":
                # 新增建物詳細資料
                if asset.building_details:
                    for building_detail in asset.building_details:
                        building_data = building_detail.dict()
                        building_data["asset_id"] = asset_id
                        building_data["created_at"] = current_time
                        building_data["updated_at"] = current_time
                        supabase.table('test_building_details').insert(building_data).execute()
                
                # 新增建物土地詳細資料
                if asset.building_land_details:
                    for land_detail in asset.building_land_details:
                        land_data = land_detail.dict()
                        land_data["asset_id"] = asset_id
                        land_data["created_at"] = current_time
                        land_data["updated_at"] = current_time
                        supabase.table('test_building_land_details').insert(land_data).execute()
            
            return {"message": "閒置資產新增成功", "asset_id": asset_id}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/assets/{asset_id}")
    async def update_idle_asset(asset_id: int, asset: AssetUpdate):
        try:
            current_time = datetime.now().isoformat()
            
            # 1. 更新主要資產資料
            update_data = {}
            for field, value in asset.dict(exclude_unset=True).items():
                if field not in ['land_details', 'building_details', 'building_land_details']:
                    if field == 'coordinates' and value:
                        update_data[field] = f"({value[0]},{value[1]})"
                    elif field == 'area_coordinates' and value:
                        points = [f"({x},{y})" for x, y in value]
                        if points[0] != points[-1]:
                            points.append(points[0])
                        update_data[field] = f"({','.join(points)})"
                    else:
                        update_data[field] = value
            
            update_data["updated_at"] = current_time
            
            if update_data:
                supabase.table('test_assets').update(update_data).eq('id', asset_id).execute()
            
            # 2. 更新土地明細
            if asset.land_details:
                # 獲取現有的土地明細
                existing_lands = supabase.table('test_land_details').select("*").eq('asset_id', asset_id).execute()
                existing_lands_dict = {land['lot_number']: land for land in existing_lands.data}
                
                # 處理每個土地明細
                for land_detail in asset.land_details:
                    land_data = land_detail.dict()
                    land_data["updated_at"] = current_time
                    
                    if land_detail.lot_number in existing_lands_dict:
                        # 更新現有記錄
                        land_id = existing_lands_dict[land_detail.lot_number]['id']
                        supabase.table('test_land_details').update(land_data).eq('id', land_id).execute()
                        # 從字典中移除已處理的記錄
                        del existing_lands_dict[land_detail.lot_number]
                    else:
                        # 新增新記錄
                        land_data["asset_id"] = asset_id
                        land_data["created_at"] = current_time
                        supabase.table('test_land_details').insert(land_data).execute()
                
                # 刪除不再需要的記錄
                if existing_lands_dict:
                    old_ids = [land['id'] for land in existing_lands_dict.values()]
                    supabase.table('test_land_details').delete().in_('id', old_ids).execute()
            
            # 3. 更新建物明細
            if asset.building_details:
                existing_buildings = supabase.table('test_building_details').select("*").eq('asset_id', asset_id).execute()
                existing_buildings_dict = {building['building_number']: building for building in existing_buildings.data}
                
                for building_detail in asset.building_details:
                    building_data = building_detail.dict()
                    building_data["updated_at"] = current_time
                    
                    if building_detail.building_number in existing_buildings_dict:
                        building_id = existing_buildings_dict[building_detail.building_number]['id']
                        supabase.table('test_building_details').update(building_data).eq('id', building_id).execute()
                        del existing_buildings_dict[building_detail.building_number]
                    else:
                        building_data["asset_id"] = asset_id
                        building_data["created_at"] = current_time
                        supabase.table('test_building_details').insert(building_data).execute()
                
                if existing_buildings_dict:
                    old_ids = [building['id'] for building in existing_buildings_dict.values()]
                    supabase.table('test_building_details').delete().in_('id', old_ids).execute()
            
            # 4. 更新建物土地明細
            if asset.building_land_details:
                existing_lands = supabase.table('test_building_land_details').select("*").eq('asset_id', asset_id).execute()
                existing_lands_dict = {land['lot_number']: land for land in existing_lands.data}
                
                for land_detail in asset.building_land_details:
                    land_data = land_detail.dict()
                    land_data["updated_at"] = current_time
                    
                    if land_detail.lot_number in existing_lands_dict:
                        land_id = existing_lands_dict[land_detail.lot_number]['id']
                        supabase.table('test_building_land_details').update(land_data).eq('id', land_id).execute()
                        del existing_lands_dict[land_detail.lot_number]
                    else:
                        land_data["asset_id"] = asset_id
                        land_data["created_at"] = current_time
                        supabase.table('test_building_land_details').insert(land_data).execute()
                
                if existing_lands_dict:
                    old_ids = [land['id'] for land in existing_lands_dict.values()]
                    supabase.table('test_building_land_details').delete().in_('id', old_ids).execute()
            
            return {"message": "閒置資產更新成功", "asset_id": asset_id}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/assets/{asset_id}")
    async def delete_idle_asset(asset_id: int):
        try:
            # 1. 檢查資產是否存在
            asset = supabase.table('test_assets').select("type").eq('id', asset_id).execute()
            if not asset.data:
                raise HTTPException(status_code=404, detail="找不到指定的��置資產")
            
            # 2. 檢查是否有相關引用
            # 檢查已活化資產表
            activated = supabase.table('test_activated_assets') \
                .select("id") \
                .eq('asset_id', asset_id) \
                .execute()
            if activated.data:
                raise HTTPException(
                    status_code=400, 
                    detail="此資產已有活化紀錄，無法刪除"
                )
            
            # 檢查案件表
            cases = supabase.table('test_asset_cases') \
                .select("id") \
                .eq('asset_id', asset_id) \
                .execute()
            if cases.data:
                raise HTTPException(
                    status_code=400, 
                    detail="此資產已有相關案件，無法刪除"
                )
            
            # 檢查活化歷史紀錄表
            history = supabase.table('test_activation_history') \
                .select("id") \
                .eq('asset_id', asset_id) \
                .execute()
            if history.data:
                raise HTTPException(
                    status_code=400, 
                    detail="此資產已有活化歷史紀錄，無法刪除"
                )
                
            # 3. 根據資產類型刪除相關的明細資料
            if asset.data[0]['type'] == "土地":
                # 刪除土地明細
                supabase.table('test_land_details').delete().eq('asset_id', asset_id).execute()
                
            elif asset.data[0]['type'] == "建物":
                # 刪除建物土地關聯
                supabase.table('test_building_land_details').delete().eq('asset_id', asset_id).execute()
                
                # 刪除建物明細
                supabase.table('test_building_details').delete().eq('asset_id', asset_id).execute()
                
            # 4. 刪除主要資產記錄
            supabase.table('test_assets').delete().eq('id', asset_id).execute()
            
            return {"message": "閒置資產刪除成功", "asset_id": asset_id}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    return router 
  
  
  