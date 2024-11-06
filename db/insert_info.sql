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

-- 戶政事務所資料
INSERT INTO agencies (name, note) VALUES
('府前戶政事務所', '戶政事務所'),
('中西戶政事務所', '戶政事務所'), 
('河南戶政事務所', '戶政事務所'),
('南化戶政事務所', '戶政事務所'),
('安南戶政事務所', '戶政事務所'),
('安平戶政事務所', '戶政事務所'),
('東區戶政事務所', '戶政事務所'),
('白河戶政事務所', '戶政事務所'),
('鹽行戶政事務所', '戶政事務所'),
('善化戶政事務所', '戶政事務所'),
('新營戶政事務所', '戶政事務所'),
('歸仁戶政事務所', '戶政事務所'),
('關廟戶政事務所', '戶政事務所'),
('永康戶政事務所', '戶政事務所'),
('玉井戶政事務所', '戶政事務所'),
('仁德戶政事務所', '戶政事務所'),
('北區戶政事務所', '戶政事務所'),
('下營戶政事務所', '戶政事務所'),
('大內戶政事務所', '戶政事務所'),
('山上戶政事務所', '戶政事務所');

-- 地政事務所資料
INSERT INTO agencies (name, note) VALUES
('臺南地政事務所', '地政事務所'),
('東南地政事務所', '地政事務所'),
('安南地政事務所', '地政事務所'),
('歸仁地政事務所', '地政事務所'),
('白河地政事務所', '地政事務所'),
('鹽水地政事務所', '地政事務所'),
('新營地政事務所', '地政事務所'),
('玉井地政事務所', '地政事務所'),
('新化地政事務所', '地政事務所'),
('佳里地政事務所', '地政事務所');

INSERT INTO agencies (name, note) VALUES
('佳里戶政事務所', '戶政事務所');

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

-- source: https://data.tainan.gov.tw/dataset/school-codes/resource/feb1f1f5-eebc-41e1-b3d8-d8a5acbe2e2a
INSERT INTO agencies (name, note) VALUES
('仁德國小', '國小'),
('文賢國小', '國小'),
('長興國小', '國小'),
('依仁國小', '國小'),
('仁和國小', '國小'),
('德南國小', '國小'),
('虎山國小', '國小'),
('歸仁國小', '國小'),
('歸南國小', '國小'),
('保西國小', '國小'),
('大潭國小', '國小'),
('關廟國小', '國小'),
('五甲國小', '國小'),
('保東國小', '國小'),
('崇和國小', '國小'),
('文和國小', '國小'),
('深坑國小', '國小'),
('新光國小', '國小'),
('永康國小', '國小'),
('大灣國小', '國小'),
('三村國小', '國小'),
('西勢國小', '國小'),
('永康復興國小', '國小'),
('龍潭國小', '國小'),
('大橋國小', '國小'),
('新化國小', '國小'),
('那拔國小', '國小'),
('口碑國小', '國小'),
('大新國小', '國小'),
('山上國小', '國小'),
('玉井國小', '國小'),
('層林國小', '國小'),
('楠西國小', '國小'),
('南化國小', '國小'),
('北寮國小', '國小'),
('西埔國小', '國小'),
('玉山國小', '國小'),
('瑞峰國小', '國小'),
('左鎮國小', '國小'),
('光榮國小', '國小'),
('善化國小', '國小'),
('茄拔國小', '國小'),
('善化大同國小', '國小'),
('大成國小', '國小'),
('陽明國小', '國小'),
('善糖國小', '國小'),
('小新國小', '國小'),
('新市國小', '國小'),
('大社國小', '國小'),
('安定國小', '國小'),
('南安國小', '國小'),
('安定南興國小', '國小'),
('麻豆國小', '國小'),
('培文國小', '國小'),
('文正國小', '國小'),
('大山國小', '國小'),
('安業國小', '國小'),
('北勢國小', '國小'),
('港尾國小', '國小'),
('紀安國小', '國小'),
('佳里國小', '國小'),
('佳興國小', '國小'),
('延平國小', '國小'),
('塭內國小', '國小'),
('子龍國小', '國小'),
('仁愛國小', '國小'),
('通興國小', '國小'),
('西港國小', '國小'),
('港東國小', '國小'),
('西港成功國小', '國小'),
('後營國小', '國小'),
('松林國小', '國小'),
('三慈國小', '國小'),
('學甲國小', '國小'),
('中洲國小', '國小'),
('宅港國小', '國小'),
('頂洲國小', '國小'),
('東陽國小', '國小'),
('下營國小', '國小'),
('中營國小', '國小'),
('甲中國小', '國小'),
('東興國小', '國小'),
('林鳳國小', '國小'),
('官田國小', '國小'),
('隆田國小', '國小'),
('嘉南國小', '國小'),
('渡拔國小', '國小'),
('二溪國小', '國小'),
('新營國小', '國小'),
('新民國小', '國小'),
('新橋國小', '國小'),
('新營新興國小', '國小'),
('新進國小', '國小'),
('南梓國小', '國小'),
('新生國小', '國小'),
('土庫國小', '國小'),
('公誠國小', '國小'),
('鹽水國小', '國小'),
('坔頭港國小', '國小'),
('月津國小', '國小'),
('竹埔國小', '國小'),
('仁光國小', '國小'),
('岸內國小', '國小'),
('文昌國小', '國小'),
('玉豐國小', '國小'),
('竹門國小', '國小'),
('內角國小', '國小'),
('仙草國小', '國小'),
('河東國小', '國小'),
('大竹國小', '國小'),
('柳營國小', '國小'),
('果毅國小', '國小'),
('重溪國小', '國小'),
('太康國小', '國小'),
('新山國小', '國小'),
('後壁國小', '國小'),
('菁寮國小', '國小'),
('安溪國小', '國小'),
('新東國小', '國小'),
('永安國小', '國小'),
('新嘉國小', '國小'),
('樹人國小', '國小'),
('東山國小', '國小'),
('聖賢國小', '國小'),
('東原國小', '國小'),
('青山國小', '國小'),
('吉貝耍國小', '國小'),
('崑山國小', '國小'),
('五王國小', '國小'),
('文化國小', '國小'),
('正新國小', '國小'),
('信義國小', '國小'),
('新泰國小', '國小'),
('永信國小', '國小'),
('永康勝利國小', '國小'),
('紅瓦厝國小', '國小'),
('南科實小', '國小'),
('寶仁國小', '國小'),
('慈濟小學', '國小'),
('勝利國小', '國小'),
('博愛國小', '國小'),
('大同國小', '國小'),
('東光國小', '國小'),
('德高國小', '國小'),
('崇學國小', '國小'),
('志開國小', '國小'),
('新興國小', '國小'),
('省躬國小', '國小'),
('喜樹國小', '國小'),
('龍崗國小', '國小'),
('日新國小', '國小'),
('永華國小', '國小'),
('新南國小', '國小'),
('立人國小', '國小'),
('公園國小', '國小'),
('開元國小', '國小'),
('大光國小', '國小'),
('石門國小', '國小'),
('西門國小', '國小'),
('安順國小', '國小'),
('和順國小', '國小'),
('海東國小', '國小'),
('安慶國小', '國小'),
('土城國小', '國小'),
('青草國小', '國小'),
('鎮海國小', '國小'),
('顯宮國小', '國小'),
('長安國小', '國小'),
('南興國小', '國小'),
('安佃國小', '國小'),
('大港國小', '國小'),
('海佃國小', '國小'),
('復興國小', '國小'),
('崇明國小', '國小'),
('安平國小', '國小'),
('文元國小', '國小'),
('學東國小', '國小'),
('億載國小', '國小'),
('賢北國小', '國小'),
('裕文國小', '國小');


INSERT INTO agencies (name, note) VALUES
('城光國中', '國中'),
('昭明國中', '國中'),
('仁德國中', '國中'),
('仁德文賢國中', '國中'),
('歸仁國中', '國中'),
('關廟國中', '國中'),
('永康國中', '國中'),
('龍崎國中', '國中'),
('新化國中', '國中'),
('善化國中', '國中'),
('玉井國中', '國中'),
('山上國中', '國中'),
('安定國中', '國中'),
('楠西國中', '國中'),
('新市國中', '國中'),
('南化國中', '國中'),
('左鎮國中', '國中'),
('麻豆國中', '國中'),
('下營國中', '國中'),
('六甲國中', '國中'),
('官田國中', '國中'),
('大內國中', '國中'),
('佳里國中', '國中'),
('佳興國中', '國中'),
('學甲國中', '國中'),
('西港國中', '國中'),
('將軍國中', '國中'),
('後港國中', '國中'),
('竹橋國中', '國中'),
('北門國中', '國中'),
('南新國中', '國中'),
('太子國中', '國中'),
('新東國中', '國中'),
('鹽水國中', '國中'),
('白河國中', '國中'),
('柳營國中', '國中'),
('東山國中', '國中'),
('東原國中', '國中'),
('後壁國中', '國中'),
('菁寮國中', '國中'),
('大橋國中', '國中'),
('沙崙國中', '國中'),
('成功國中', '國中'),
('延平國中', '國中'),
('建興國中', '國中'),
('中山國中', '國中'),
('安平國中', '國中'),
('安南國中', '國中'),
('安順國中', '國中'),
('復興國中', '國中'),
('新興國中', '國中'),
('文賢國中', '國中'),
('崇明國中', '國中'),
('和順國中', '國中'),
('海佃國中', '國中');

INSERT INTO agencies (name, note) VALUES
-- 高中
('新豐高中', '高中'),
('臺南大學附中', '高中'),
('北門高中', '高中'),
('新營高中', '高中'),
('後壁高中', '高中'),
('善化高中', '高中'),
('新化高中', '高中'),
('南科實中', '高中'),
('南光高中', '高中'),
('鳳和高中', '高中'),
('港明高中', '高中'),
('興國高中', '高中'),
('明達高中', '高中'),
('黎明高中', '高中'),
('華濟永安高中', '高中'),
('新榮高中', '高中'),
('大灣高中', '高中'),
('永仁高中', '高中'),
('土城高中', '高中'),
('建業中學', '高中'),
('瀛海中學', '高中'),
('崑山中學', '高中'),
('德光高中', '高中'),
('慈濟高中', '高中'),

-- 職業學校
('北門農工', '職業學校');


-- 資產使用類型資料
INSERT INTO usage_types (name) VALUES
('辦公廳舍/行政空間'),
('社會福利設施'),
('檔案室/倉儲'),
('文教設施'),
('停車場'),
('活動中心'),
('觀光遊憩設施'),
('交通設施'),
('其他'),
('環保設施'),
('動物福利設施'),
('親子育兒設施'),
('創業育成空間'),
('休閒遊憩設施'),
('醫療衛生'),
('交通運輸設施'),
('辦理標租作業'),
('商業市集'),
('商業服務設施'),
('緊急救援設施'),
('郵政服務設施'),
('教育訓練設施'),
('環境綠化設施'),
('產業支援設施');