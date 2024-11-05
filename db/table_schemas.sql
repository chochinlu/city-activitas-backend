-- // 行政區資料表
-- Table districts {
--   id integer [pk, increment]
--   name varchar [not null, unique] // 例如：六甲區、鹽水區
--   note text

--   indexes {
--     name
--   }
-- }

CREATE TABLE districts (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    note TEXT
);

COMMENT ON COLUMN districts.name IS '例如：六甲區、鹽水區';


-- // 管理機關資料表
-- Table agencies {
--   id integer [pk, increment]
--   name varchar [not null, unique] // 例如：六甲國小、財政稅務局
--   note text

--   indexes {
--     name
--   }
-- }

CREATE TABLE agencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    note TEXT
);

COMMENT ON COLUMN agencies.name IS '例如：六甲國小、財政稅務局';

-- // 主要資產資料表
-- Table assets {
--   id integer [pk, increment]
--   type varchar [not null]          // `資產種類`例如：土地、建物
--   agency_id integer [ref: > agencies.id]
--   district_id integer [ref: > districts.id]
--   section varchar [not null]       // `地段` 例如：大丘園段、田寮段
--   address text                     // 例如：錦仁區和平南街9號
--   coordinates point                 // 定位座標, 使用 PostgreSQL 的 PostGIS 擴充功能
--   area_coordinates polygon            // 區域座標組, 使用 PostgreSQL 的 PostGIS 擴充功能
--   target_name varchar             // 標的名稱(原本只有建物資產有, 挪來這裡), 例如：歸仁市場2, 3樓
--   status varchar                  // 例如：已經活化、活化中、未活化
--   created_at timestamp [default: `CURRENT_TIMESTAMP`]
--   updated_at timestamp

--   indexes {
--     type
--     agency_id
--     district_id
--     status
--   }
-- }

-- 使用 PostGIS 擴充功能
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    type VARCHAR NOT NULL,
    agency_id INTEGER NOT NULL REFERENCES agencies(id),
    district_id INTEGER NOT NULL REFERENCES districts(id),
    section VARCHAR NOT NULL,
    address TEXT,
    coordinates POINT,
    area_coordinates POLYGON,
    target_name VARCHAR,
    status VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- 建立索引
CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_assets_agency_id ON assets(agency_id);
CREATE INDEX idx_assets_district_id ON assets(district_id);
CREATE INDEX idx_assets_status ON assets(status);

-- 添加欄位註釋
COMMENT ON COLUMN assets.type IS '資產種類，例如：土地、建物';
COMMENT ON COLUMN assets.section IS '地段，例如：大丘園段、田寮段';
COMMENT ON COLUMN assets.address IS '例如：錦仁區和平南街9號';
COMMENT ON COLUMN assets.coordinates IS '定位座標，使用 PostgreSQL 的 PostGIS 擴充功能';
COMMENT ON COLUMN assets.area_coordinates IS '區域座標組，使用 PostgreSQL 的 PostGIS 擴充功能';
COMMENT ON COLUMN assets.target_name IS '標的名稱(原本只有建物資產有，挪來這裡)，例如：歸仁市場2, 3樓';
COMMENT ON COLUMN assets.status IS '例如：已經活化、活化中、未活化';

-- // 土地資料表
-- Table land_details {
--   id integer [pk, increment]
--   asset_id integer [ref: > assets.id]
--   lot_number varchar [not null]    // 地號, 例如：80-8、81-1
--   land_type varchar               // 土地種類, 例如：市有土地、國有土地
--   area decimal                    // 面積(平方公尺), 例如：7826
--   zone_type varchar               // 使用分區, 例如：學校用地、保護區
--   land_use varchar                // 土地用途(市區的不會有), 例如：特定目的事業用地
--   current_status varchar          // 現況, 例如：空置
--   vacancy_rate integer            // 空置比例, 例如：100
--   note text                       // 例如：六甲國小大丘分班(已裁併校)
--   created_at timestamp [default: `CURRENT_TIMESTAMP`]
--   updated_at timestamp
--   deleted_at timestamp

--   indexes {
--     asset_id
--     lot_number
--     zone_type
--     current_status
--   }
-- }

CREATE TABLE land_details (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    lot_number VARCHAR NOT NULL,
    land_type VARCHAR,
    area DECIMAL,
    zone_type VARCHAR,
    land_use VARCHAR,
    current_status VARCHAR,
    vacancy_rate INTEGER,
    note TEXT
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 建立索引
CREATE INDEX idx_land_details_asset_id ON land_details(asset_id);
CREATE INDEX idx_land_details_lot_number ON land_details(lot_number);
CREATE INDEX idx_land_details_zone_type ON land_details(zone_type);
CREATE INDEX idx_land_details_current_status ON land_details(current_status);

-- 添加欄位註釋
COMMENT ON COLUMN land_details.lot_number IS '地號，例如：80-8、81-1';
COMMENT ON COLUMN land_details.land_type IS '土地種類，例如：市有土地、國有土地';
COMMENT ON COLUMN land_details.area IS '面積(平方公尺)，例如：7826';
COMMENT ON COLUMN land_details.zone_type IS '使用分區，例如：學校用地、保護區';
COMMENT ON COLUMN land_details.land_use IS '土地用途(市區的不會有)，例如：特定目的事業用地';
COMMENT ON COLUMN land_details.current_status IS '現況，例如：空置';
COMMENT ON COLUMN land_details.vacancy_rate IS '空置比例，例如：100';
COMMENT ON COLUMN land_details.note IS '例如：六甲國小大丘分班(已裁併校)';


-- // 建物資料表
-- Table building_details {
--   id integer [pk, increment]
--   asset_id integer [ref: > assets.id]
--   building_number varchar         // 建號, 例如：歸仁北段6932建號
--   building_type varchar          // 建物種類, 例如：市有建物
--   floor_area text               // 樓地板面積(平方公尺), 例如：2樓:3729.7 3樓:3426.2
--   zone_type varchar               // 使用分區, 例如：學校用地、保護區
--   land_use varchar                // 土地用途(市區的不會有), 例如：特定目的事業用地
--   current_status varchar         // 現況, 例如：空置、部分空置
--   vacancy_rate varchar          // 空置比例, 例如：100
--   note text                     // 例如：2樓空置、3樓部分空間約400坪提供給使用

--   indexes {
--     asset_id
--     building_number
--     current_status
--     zone_type
--     land_use
--   }
-- }

CREATE TABLE building_details (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    building_number VARCHAR(100),
    building_type VARCHAR(50),
    floor_area TEXT,
    zone_type VARCHAR(100),
    land_use VARCHAR(100),
    current_status VARCHAR(50),
    vacancy_rate INTEGER,
    note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 建立索引
CREATE INDEX idx_building_details_asset_id ON building_details(asset_id);
CREATE INDEX idx_building_details_building_number ON building_details(building_number);
CREATE INDEX idx_building_details_current_status ON building_details(current_status);
CREATE INDEX idx_building_details_zone_type ON building_details(zone_type);
CREATE INDEX idx_building_details_land_use ON building_details(land_use);

-- 添加欄位註釋
COMMENT ON COLUMN building_details.building_number IS '建號，例如：歸仁北段6932建號';
COMMENT ON COLUMN building_details.building_type IS '建物種類，例如：市有建物';
COMMENT ON COLUMN building_details.floor_area IS '樓地板面積(平方公尺)，例如：2樓:3729.7 3樓:3426.2';
COMMENT ON COLUMN building_details.zone_type IS '使用分區，例如：住宅區、商業區、工業區';
COMMENT ON COLUMN building_details.land_use IS '土地用途，例如：乙種建築用地、特定目的事業用地';
COMMENT ON COLUMN building_details.current_status IS '現況，例如：空置、部分空置';
COMMENT ON COLUMN building_details.vacancy_rate IS '空置比例，例如：100';
COMMENT ON COLUMN building_details.note IS '例如：2樓空置、3樓部分空間約400坪提供給使用';


// 建物土地關聯表
-- Table building_land_details {
--   id SERIAL [pk]
--   asset_id INTEGER [ref: > assets.id]
--   lot_number VARCHAR(20) [note: '地號']
--   land_type VARCHAR(50) [note: '土地種類']
--   land_manager VARCHAR(50) [note: '土地管理者']
--   created_at TIMESTAMP [note: '建立時間']
--   updated_at TIMESTAMP [note: '更新時間']
-- }


CREATE TABLE building_land_details (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    lot_number VARCHAR(20) NOT NULL,  -- 地號
    land_type VARCHAR(50),            -- 土地種類 (市有土地/國有土地/私有土地)
    land_manager VARCHAR(50),         -- 土地管理者
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

COMMENT ON TABLE building_land_details IS '建物土地關聯表';
COMMENT ON COLUMN building_land_details.id IS '主鍵 ID';
COMMENT ON COLUMN building_land_details.asset_id IS '資產 ID';
COMMENT ON COLUMN building_land_details.lot_number IS '地號';
COMMENT ON COLUMN building_land_details.land_type IS '土地種類 (市有土地/國有土地/私有土地)';
COMMENT ON COLUMN building_land_details.land_manager IS '土地管理者';