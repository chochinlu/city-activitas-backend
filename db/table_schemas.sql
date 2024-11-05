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