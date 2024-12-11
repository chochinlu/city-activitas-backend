from fastapi import APIRouter, HTTPException, Depends
from supabase import Client
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from dependencies.auth import get_auth_dependency

router = APIRouter(prefix="/api/v1/proposals", tags=["資產提報與需求"])

# 資產提報請求模型
class AssetProposalCreate(BaseModel):
    agency_id: str                
    target_name: Optional[str] = None
    district_id: str               
    section: str
    lot_number: str
    address: Optional[str] = None
    coordinates: Optional[str] = None
    
    # 執照相關
    has_usage_license: str              # 有、無
    has_building_license: str           # 有、無、部分
    
    # 土地相關資訊
    land_type: Optional[str] = None
    zone_type: Optional[str] = None
    land_use: Optional[str] = None
    area: Optional[float] = None
    floor_area: Optional[str] = None
    
    # 使用狀況
    usage_status: str                   # 閒置、低度利用
    usage_description: Optional[str] = None
    
    # 活化相關
    activation_status: Optional[str] = None
    estimated_activation_date: Optional[datetime] = None
    is_requesting_delisting: bool = False
    delisting_reason: Optional[str] = None
    
    # 提案相關
    note: Optional[str] = None
    reporter_email: str

class AssetProposalUpdate(BaseModel):
    target_name: Optional[str] = None
    district_id: Optional[int] = None
    section: Optional[str] = None
    lot_number: Optional[str] = None
    address: Optional[str] = None
    coordinates: Optional[str] = None
    has_usage_license: Optional[str] = None
    has_building_license: Optional[str] = None
    land_type: Optional[str] = None
    zone_type: Optional[str] = None
    land_use: Optional[str] = None
    area: Optional[float] = None
    floor_area: Optional[str] = None
    usage_status: Optional[str] = None
    usage_description: Optional[str] = None
    activation_status: Optional[str] = None
    estimated_activation_date: Optional[datetime] = None
    is_requesting_delisting: Optional[bool] = None
    delisting_reason: Optional[str] = None
    note: Optional[str] = None
    proposal_status: Optional[str] = None
    reviewer_note: Optional[str] = None

# 需求資產請求模型
class AssetRequirementCreate(BaseModel):
    agency_id: str
    purpose: str                        # 需求用途
    asset_type: str                     # 資產種類：土地/建物
    preferred_floor: Optional[str] = None
    area: Optional[float] = None
    district_id: Optional[str] = None
    urgency_note: Optional[str] = None
    funding_source: Optional[str] = None
    reporter_email: str

class AssetRequirementUpdate(BaseModel):
    purpose: Optional[str] = None
    asset_type: Optional[str] = None
    preferred_floor: Optional[str] = None
    area: Optional[float] = None
    district_id: Optional[int] = None
    urgency_note: Optional[str] = None
    funding_source: Optional[str] = None
    requirement_status: Optional[str] = None
    reviewer_note: Optional[str] = None

def init_router(supabase: Client) -> APIRouter:
    verify_token = get_auth_dependency(supabase)

    @router.get("/asset-proposals")
    async def get_asset_proposals():
        """取得所有資產提報"""
        try:
            response = supabase.table('test_asset_proposals').select("*").execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/asset-proposals/{proposal_id}")
    async def get_asset_proposal(proposal_id: int):
        """取得特定資產提報"""
        try:
            response = supabase.table('test_asset_proposals') \
                .select("*") \
                .eq('id', proposal_id) \
                .single() \
                .execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=404, detail="找不到指定的資產提報")

    @router.post("/asset-proposals", dependencies=[Depends(verify_token)])
    async def create_asset_proposal(proposal: AssetProposalCreate):
        """建立新的資產提報"""
        try:
            # 檢查 district_id 是否存在
            if proposal.district_id:
                district = supabase.table('districts').select("*").eq('id', proposal.district_id).execute()
                if not district.data:
                    raise HTTPException(status_code=404, detail="找不到指定的行政區")

            # 檢查 agency_id 是否存在
            if proposal.agency_id:
                agency = supabase.table('agencies').select("*").eq('id', proposal.agency_id).execute()
                if not agency.data:
                    raise HTTPException(status_code=404, detail="找不到指定的管理機關")

            # 準備插入資料
            insert_data = proposal.model_dump()
            insert_data["created_at"] = datetime.now().isoformat()
            insert_data["updated_at"] = datetime.now().isoformat()
            insert_data['proposal_status'] = '提案中'

            print("要插入的資料：", insert_data)
            
            response = supabase.table('test_asset_proposals').insert(insert_data).execute()
            return response.data[0]
        except Exception as e:
            print("錯誤：", str(e))
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/asset-proposals/{proposal_id}", dependencies=[Depends(verify_token)])
    async def update_asset_proposal(proposal_id: int, proposal: AssetProposalUpdate):
        """更新資產提報"""
        try:
            # 檢查提報是否存在
            existing = supabase.table('test_asset_proposals') \
                .select("*") \
                .eq('id', proposal_id) \
                .single() \
                .execute()
            if not existing.data:
                raise HTTPException(status_code=404, detail="找不到指定的資產提報")

            # 直接使用字串格式的座標
            update_data = proposal.dict(exclude_unset=True)
            update_data['updated_at'] = datetime.now().isoformat()

            response = supabase.table('test_asset_proposals') \
                .update(update_data) \
                .eq('id', proposal_id) \
                .execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/asset-requirements")
    async def get_asset_requirements():
        """取得所有需求資產"""
        try:
            response = supabase.table('test_asset_requirements').select("*").execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/asset-requirements/{requirement_id}")
    async def get_asset_requirement(requirement_id: int):
        """取得特定需求資產"""
        try:
            response = supabase.table('test_asset_requirements') \
                .select("*") \
                .eq('id', requirement_id) \
                .single() \
                .execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=404, detail="找不到指定的需求資產")

    @router.post("/asset-requirements", dependencies=[Depends(verify_token)])
    async def create_asset_requirement(requirement: AssetRequirementCreate):
        """建立新的需求資產"""
        try:
            insert_data = requirement.dict()
            insert_data['created_at'] = datetime.now().isoformat()
            insert_data['updated_at'] = datetime.now().isoformat()
            insert_data['requirement_status'] = '提案中'

            response = supabase.table('test_asset_requirements').insert(insert_data).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/asset-requirements/{requirement_id}", dependencies=[Depends(verify_token)])
    async def update_asset_requirement(requirement_id: int, requirement: AssetRequirementUpdate):
        """更新需求資產"""
        try:
            # 檢查需求是否存在
            existing = supabase.table('test_asset_requirements') \
                .select("*") \
                .eq('id', requirement_id) \
                .single() \
                .execute()
            if not existing.data:
                raise HTTPException(status_code=404, detail="找不到指定的需求資產")

            update_data = requirement.dict(exclude_unset=True)
            update_data['updated_at'] = datetime.now().isoformat()

            response = supabase.table('test_asset_requirements') \
                .update(update_data) \
                .eq('id', requirement_id) \
                .execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router 