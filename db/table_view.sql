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