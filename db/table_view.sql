-- 使用測試用table view
create view
  public.test_idle_assets_view as
select
  a.id,
  a.type as "資產類型",
  a.target_name as "標的名稱",
  d.name as "行政區",
  a.section as "地段",
  a.address as "地址",
  ag.name as "管理機關",
  a.status as "狀態",
  a.coordinates as "定位座標",
  a.area_coordinates as "區域座標組",
  a.created_at as "建立時間"
from
  test_assets a
  left join test_districts d on a.district_id = d.id
  left join test_agencies ag on a.agency_id = ag.id
where
  a.status::text = '未活化'::text
order by
  d.name,
  a.created_at desc;


create view
  public.test_idle_land_assets_view as
select
  a.id as "資產ID",
  ld.id as "土地明細ID",
  d.name as "行政區",
  a.target_name as "標的名稱",
  a.section as "地段",
  a.address as "地址",
  ag.name as "管理機關",
  ld.lot_number as "地號",
  ld.land_type as "土地類型",
  ld.area as "面積(平方公尺)",
  ld.zone_type as "使用分區",
  ld.land_use as "土地用途",
  ld.current_status as "現況",
  ld.vacancy_rate as "空置比例(%)",
  ld.note as "備註",
  a.status as "狀態",
  a.created_at as "建立時間"
from
  test_assets a
  left join test_districts d on a.district_id = d.id
  left join test_agencies ag on a.agency_id = ag.id
  left join test_land_details ld on a.id = ld.asset_id
where
  a.status::text = '未活化'::text
  and a.type::text = '土地'::text
  and ld.deleted_at is null
order by
  a.id,
  d.name,
  a.section,
  ld.lot_number;