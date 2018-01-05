-- 数据库链接
-- mongo 172.17.33.176:30001/feed -u liquid -p n3tw0rk

-- 创建 Collection
db.createCollection("capture_mysite_video", {size: 20, capped: 5, max: 100})
