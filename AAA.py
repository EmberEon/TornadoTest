from forum.utils import file_log

items = [{"goods_id": 2104, "count": 1, "name": "1元话费×1", "img_url": "/ddz_goods_items/2104.png", "time_limit": 0},
         {"goods_id": 2103, "count": 1, "name": "30元话费×1", "img_url": "/ddz_goods_items/2103.png", "time_limit": 0},
         {"goods_id": 2115, "count": 1, "name": "50元话费×1", "img_url": "/ddz_goods_items/2115.png", "time_limit": 0},
         {"goods_id": 2102, "count": 1, "name": "20元话费×1", "img_url": "/ddz_goods_items/2102.png", "time_limit": 0},
         {"goods_id": 2101, "count": 1, "name": "10元话费×1", "img_url": "/ddz_goods_items/2101.png", "time_limit": 0},
         {"goods_id": 2100, "count": 1, "name": "5元话费×1", "img_url": "/ddz_goods_items/2100.png", "time_limit": 0},
         {"goods_id": 2114, "count": 1, "name": "100元话费×1", "img_url": "/ddz_goods_items/2114.png", "time_limit": 0},
         {"goods_id": 2002, "count": 6718800000, "name": "金币×67.188亿", "img_url": "/ddz_goods_items/2002.png",
          "time_limit": 0}]


# 自定义排序规则函数
def custom_sort(item):
    # 如果是金币项，将其排在最后
    if "金币" in item["name"]:
        return (float("inf"), item["name"])

    # 提取话费金额（假设话费金额在名称中的数字部分）
    amount = int(item["name"].split("元")[0])
    return (-amount, item["name"])


# 使用自定义排序规则对物品进行排序
sorted_items = sorted(items, key=custom_sort)

# 打印排序后的物品列表
for item in sorted_items:
    file_log.fail_log
    print(item)


