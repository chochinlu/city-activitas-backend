from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from pydantic import BaseModel
from typing import Optional, Tuple, List
from datetime import datetime
from supabase import Client
from dependencies.auth import get_auth_dependency

# 定義請求模型
class AssetUpdate(BaseModel):
    type: Optional[str] = None                # 資產種類：土地或建物
    agency_id: Optional[str] = None           # 管理機關ID
    district_id: Optional[str] = None         # 行政區ID
    section: Optional[str] = None             # 地段
    address: Optional[str] = None             # 地址
    coordinates: Optional[str] = None          # 接收 "(120.123, 23.456)" 格式的字串
    area_coordinates: Optional[str] = None     # 接收多邊形座標字串
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

class BuildingLandDetailUpdate(BaseModel):
    lot_number: Optional[str] = None      # 地號
    land_type: Optional[str] = None       # 土地種類 (市有土地/國有土地/私有土地)
    land_manager: Optional[str] = None    # 土地管理者

class AssetImageCreate(BaseModel):
    title: str
    description: Optional[str] = None

class AssetImageUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

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
            "coordinates": "(120.123, 23.456)",
            "area_coordinates": "((120.123, 23.456),(120.123, 23.456),(120.123, 23.456))"
        }
        ```
        """
        try:
            # 1. 檢查資產是否存在
            existing_asset = supabase.table('test_assets').select("*").eq('id', asset_id).execute()
            if not existing_asset.data:
                raise HTTPException(status_code=404, detail="找不到指定的資產")
            
            # 2. 準備更新資料
            update_data = asset.dict(exclude_unset=True)
            
            # 3. 處理座標資料
            if 'coordinates' in update_data:
                # 將 "(120.123, 23.456)" 轉換為 PostgreSQL POINT 格式
                coordinates_str = update_data['coordinates'].strip('()')
                x, y = map(float, coordinates_str.split(','))
                update_data['coordinates'] = f"({x},{y})"  # PostgreSQL POINT 格式
            
            if 'area_coordinates' in update_data:
                # 這裡需要根據你的多邊形座標格式進行相應的轉換
                # 假設接收的是 "((x1,y1),(x2,y2),(x3,y3))" 格式
                update_data['area_coordinates'] = update_data['area_coordinates']
            
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 4. 更新資產資料
            response = supabase.table('test_assets').update(update_data).eq('id', asset_id).execute()
            
            return {"message": "資產更新成功", "asset_id": asset_id}
            
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

    @router.patch("/building-lands/{detail_id}", dependencies=[Depends(verify_token)])
    async def update_building_land_detail(detail_id: int, detail: BuildingLandDetailUpdate):
        """
        更新建物土地關聯資料
        
        範例:
        ```json
        {
            "lot_number": "80-8",
            "land_type": "市有土地",
            "land_manager": "財政部國有財產署"
        }
        ```
        """
        try:
            # 1. 檢查建物土地關聯是否存在
            existing_detail = supabase.table('test_building_land_details').select("*").eq('id', detail_id).execute()
            if not existing_detail.data:
                raise HTTPException(status_code=404, detail="找不到指定的建物土地關聯資料")
            
            # 2. 準備更新資料
            update_data = detail.dict(exclude_unset=True)  # 只包含有設定值的欄位
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 3. 更新建物土地關聯資料
            response = supabase.table('test_building_land_details').update(update_data).eq('id', detail_id).execute()
            
            return {"message": "建物土地關聯更新成功", "detail_id": detail_id}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/{asset_id}/images", dependencies=[Depends(verify_token)])
    async def upload_asset_image(
        asset_id: int,
        file: UploadFile = File(...),
        image_data: AssetImageCreate = Depends()
    ):
        """
        上傳資產圖片
        
        - **file**: 圖片檔案
        - **title**: 圖片標題
        - **description**: 圖片說明（選填）
        """
        print(file)
        print(image_data)
        print(asset_id)
        try:
            # 1. 檢查資產是否存在
            existing_asset = supabase.table('test_assets').select("*").eq('id', asset_id).execute()
            if not existing_asset.data:
                raise HTTPException(status_code=404, detail="找不到指定的資產")
            
            # 2. 上傳圖片到 Supabase Storage
            file_path = f"assets/{asset_id}/{file.filename}"
            storage_response = supabase.storage.from_('assets').upload(
                file_path,
                file.file.read(),
                file_options={"content-type": file.content_type}
            )
            
            # 3. 取得圖片 URL
            storage_url = supabase.storage.from_('assets').get_public_url(file_path)
            
            # 4. 儲存圖片資訊到資料庫
            image_info = {
                "asset_id": asset_id,
                "storage_url": storage_url,
                "file_name": file.filename,
                "file_size": file.size,
                "mime_type": file.content_type,
                "title": image_data.title,
                "description": image_data.description,
                "editor_email": "user@example.com"  # 應從 token 中取得
            }
            
            response = supabase.table('asset_images').insert(image_info).execute()
            
            return {"message": "圖片上傳成功", "image": response.data[0]}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/{asset_id}/images", dependencies=[Depends(verify_token)])
    async def list_asset_images(asset_id: int):
        """
        取得資產的所有圖片
        """
        try:
            response = supabase.table('asset_images').select("*").eq('asset_id', asset_id).execute()
            return response.data
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/images/{image_id}", dependencies=[Depends(verify_token)])
    async def update_asset_image(image_id: int, image: AssetImageUpdate):
        """
        更新圖片資訊
        
        範例:
        ```json
        {
            "title": "新標題",
            "description": "新說明"
        }
        ```
        """
        try:
            # 1. 檢查圖片是否存在
            existing_image = supabase.table('asset_images').select("*").eq('id', image_id).execute()
            if not existing_image.data:
                raise HTTPException(status_code=404, detail="找不到指定的圖片")
            
            # 2. 準備更新資料
            update_data = image.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.now().isoformat()
            
            # 3. 更新圖片資訊
            response = supabase.table('asset_images').update(update_data).eq('id', image_id).execute()
            
            return {"message": "圖片資訊更新成功", "image": response.data[0]}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/images/{image_id}", dependencies=[Depends(verify_token)])
    async def delete_asset_image(image_id: int):
        """
        刪除資產圖片
        """
        try:
            # 1. 取得圖片資訊
            image = supabase.table('asset_images').select("*").eq('id', image_id).execute()
            if not image.data:
                raise HTTPException(status_code=404, detail="找不到指定的圖片")
            
            # 2. 從 Storage 刪除圖片
            file_path = image.data[0]["storage_url"].split("/")[-1]
            supabase.storage.from_('assets').remove([file_path])
            
            # 3. 從資料庫刪除記錄
            response = supabase.table('asset_images').delete().eq('id', image_id).execute()
            
            return {"message": "圖片刪除成功"}
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=str(e))
          
  

    return router 