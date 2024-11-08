COMMENT ON TABLE districts IS '行政區資料表';
COMMENT ON TABLE agencies IS '管理機關資料表';
COMMENT ON TABLE assets IS '資產資料表';
COMMENT ON TABLE land_details IS '土地資料表';
COMMENT ON TABLE building_details IS '建物資料表';
COMMENT ON TABLE building_land_details IS '建物土地關聯表';
COMMENT ON TABLE usage_types IS '資產使用類型資料表';
COMMENT ON TABLE activated_asset_demand_agencies IS '已活化資產與需求機關關聯表';
COMMENT ON TABLE activated_assets IS '已活化資產資料表';
COMMENT ON TABLE activation_history IS '資產活化歷史紀錄表';
COMMENT ON TABLE asset_cases IS '資產處理案件表';
COMMENT ON TABLE case_meeting_conclusions IS '案件會議結論表';
COMMENT ON TABLE case_tasks IS '案件任務表';


COMMENT ON VIEW idle_assets_view IS '閒置資產視圖';
COMMENT ON VIEW idle_land_assets_view IS '閒置土地資產視圖';
COMMENT ON VIEW idle_building_assets IS '閒置建物資產視圖';
COMMENT ON VIEW activated_assets_view IS '已活化資產視圖';
COMMENT ON VIEW asset_cases_view IS '資產活化案件與統計視圖';
COMMENT ON VIEW case_tasks_view IS '資產活化案件任務視圖';
