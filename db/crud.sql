-- 行政區資料
INSERT INTO districts (name) VALUES
('新營區'),
('鹽水區'),
('白河區'),
('柳營區'),
('後壁區'),
('東山區'),
('麻豆區'),
('下營區'),
('六甲區'),
('官田區'),
('大內區'),
('佳里區'),
('學甲區'),
('西港區'),
('七股區'),
('將軍區'),
('北門區'),
('新化區'),
('新市區'),
('善化區'),
('安定區'),
('山上區'),
('玉井區'),
('楠西區'),
('南化區'),
('左鎮區'),
('仁德區'),
('歸仁區'),
('關廟區'),
('龍崎區'),
('永康區'),
('東區'),
('南區'),
('中西區'),
('北區'),
('安南區'),
('安平區');

-- 管理機關資料
-- source: https://www.tainan.gov.tw/cp.aspx?n=13297
INSERT INTO agencies (name, note) VALUES
('民政局', '一級機關'),
('教育局', '一級機關'),
('農業局', '一級機關'),
('經濟發展局', '一級機關'),
('觀光旅遊局', '一級機關'),
('工務局', '一級機關'),
('水利局', '一級機關'),
('社會局', '一級機關'),
('勞工局', '一級機關'),
('地政局', '一級機關'),
('都市發展局', '一級機關'),
('文化局', '一級機關'),
('交通局', '一級機關'),
('衛生局', '一級機關'),
('環境保護局', '一級機關'),
('警察局', '一級機關'),
('消防局', '一級機關'),
('財政稅務局', '一級機關'),
('體育局', '一級機關');

-- source: https://www.tainan.gov.tw/News_Contacts.aspx?n=14213&sms=16578#128
-- 戶政事務所 和 地政事務所 尚未列入
INSERT INTO agencies (name, note) VALUES
('智慧發展中心', '二級機關'),
('公務人力發展中心', '二級機關'),
('殯葬管理所', '二級機關'),
('南瀛科學教育館', '二級機關'),
('家庭教育中心', '二級機關'),
('動物防疫保護處', '二級機關'),
('漁港及近海管理所', '二級機關'),
('臺南市市場處', '二級機關'),
('家庭暴力暨性侵害防治中心', '二級機關'),
('職訓就服中心', '二級機關'),
('文化資產管理處', '二級機關'),
('臺南市立圖書館', '二級機關'),
('車輛行車事故鑑定會', '二級機關'),
('臺南市公共運輸處', '二級機關'),
('臺南市捷運工程處', '二級機關'),
('職業安全健康處', '二級機關'),
('臺南市立博物館', '二級機關');

-- 區公所資料
INSERT INTO agencies (name, note) VALUES
('安定區公所', '區公所'),
('安南區公所', '區公所'),
('新化區公所', '區公所'),
('學甲區公所', '區公所'),
('北門區公所', '區公所'),
('七股區公所', '區公所'),
('大內區公所', '區公所'),
('東山區公所', '區公所'),
('關廟區公所', '區公所'),
('官田區公所', '區公所'),
('後壁區公所', '區公所'),
('佳里區公所', '區公所'),
('將軍區公所', '區公所'),
('龍崎區公所', '區公所'),
('南化區公所', '區公所'),
('楠西區公所', '區公所'),
('北區區公所', '區公所'),
('下營區公所', '區公所'),
('新營區公所', '區公所'),
('鹽水區公所', '區公所'),
('左鎮區公所', '區公所'),
('歸仁區公所', '區公所'),
('東區區公所', '區公所'),
('中西區公所', '區公所'),
('南區區公所', '區公所'),
('安平區公所', '區公所'),
('白河區公所', '區公所'),
('柳營區公所', '區公所'),
('麻豆區公所', '區公所'),
('六甲區公所', '區公所'),
('西港區公所', '區公所'),
('善化區公所', '區公所'),
('新市區公所', '區公所'),
('山上區公所', '區公所'),
('玉井區公所', '區公所'),
('仁德區公所', '區公所'),
('永康區公所', '區公所');

INSERT INTO agencies (name, note) VALUES
('安南區衛生所', '衛生所'),
('安平區衛生所', '衛生所'),
('東區衛生所', '衛生所'),
('北區衛生所', '衛生所'),
('南區衛生所', '衛生所'),
('中西區衛生所', '衛生所'),
('安定區衛生所', '衛生所'),
('將軍區衛生所', '衛生所'),
('七股區衛生所', '衛生所'),
('佳里區衛生所', '衛生所'),
('學甲區衛生所', '衛生所'),
('新化區衛生所', '衛生所'),
('西港區衛生所', '衛生所'),
('後壁區衛生所', '衛生所'),
('新市區衛生所', '衛生所'),
('下營區衛生所', '衛生所'),
('仁德區衛生所', '衛生所'),
('歸仁區衛生所', '衛生所'),
('關廟區衛生所', '衛生所'),
('官田區衛生所', '衛生所'),
('六甲區衛生所', '衛生所'),
('柳營區衛生所', '衛生所'),
('麻豆區衛生所', '衛生所'),
('楠西區衛生所', '衛生所'),
('南化區衛生所', '衛生所'),
('白河區衛生所', '衛生所'),
('北門區衛生所', '衛生所'),
('善化區衛生所', '衛生所'),
('山上區衛生所', '衛生所'),
('新營區衛生所', '衛生所'),
('左鎮區衛生所', '衛生所'),
('大內區衛生所', '衛生所'),
('東山區衛生所', '衛生所'),
('玉井區衛生所', '衛生所'),
('永康區衛生所', '衛生所'),
('鹽水區衛生所', '衛生所'),
('龍崎區衛生所', '衛生所');

-- 一級單位資料
INSERT INTO agencies (name, note) VALUES
('秘書處', '一級單位'),
('法制處', '一級單位'),
('新聞及國際關係處', '一級單位'),
('原住民族事務委員會', '一級單位'),
('研究發展考核委員會', '一級單位'),
('人事處', '一級單位'),
('主計處', '一級單位'),
('政風處', '一級單位'),
('客家事務委員會', '一級單位');

-- 國小資料, 沒有全部列出, 先只列出有用到的
INSERT INTO agencies (name, note) VALUES
('六甲國小', '國小'),
('歡雅國小', '國小'),
('大內國小', '國小'),
('白河國小', '國小');

-- 國小資料, 沒有全部列出, 先只列出有用到的
INSERT INTO agencies (name, note) VALUES
('大甲國小', '國小'),
('賀建國小', '國小');



