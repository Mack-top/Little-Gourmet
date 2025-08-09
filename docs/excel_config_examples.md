# Excel配置示例

## 奖励配置表

### 菜谱周排名奖励表 (recipe_weekly_rewards)

| 排名范围 | 排名范围 | 金币奖励 | 美丽值奖励 | 经验奖励 |
|---------|---------|---------|----------|---------|
| rank_range | rank_range | gold | beauty | exp |
| string | string | int | int | int |
| 1 | 1 | 1000 | 50 | 500 |
| 2 | 2 | 800 | 40 | 400 |
| 3 | 3 | 600 | 30 | 300 |
| 4-10 | 4-10 | 400 | 20 | 200 |
| 11-50 | 11-50 | 200 | 10 | 100 |

## 付费加分限制配置表

### 每日额外加分限制表 (daily_extra_points_limit)

| 配置项 | 配置项 | 数值 |
|-------|-------|-----|
| config_key | config_key | config_value |
| string | string | float/int |
| daily_limit_per_recipe | 每个菜谱每日最多可购买的额外加分 | 10.0 |
| cost_per_point | 每点额外加分所需金币 | 100 |

## 菜谱商店配置表

### 商店排行榜配置表 (recipe_store_config)

| 配置项 | 配置项 | 数值 |
|-------|-------|-----|
| config_key | config_key | config_value |
| string | string | float/int |
| top_ranked_recipe_count | 前几名菜谱可被收集到商店 | 3 |
| royalty_rate | 菜谱拥有者分成比例 | 0.05 |
| update_cycle_days | 商店排行榜更新周期（天） | 30 |

## 数据库导出表示例

### 菜谱表 (recipes)

| 菜谱ID | 菜谱名称 | 菜系分类 | 难度等级 | 制作时间 |
|-------|---------|---------|---------|---------|
| recipe_id | name | category | difficulty | time_required |
| int | string | string | int | int |
| 1001 | 麻婆豆腐 | 川菜 | 5 | 30 |
| 1002 | 红烧肉 | 家常菜 | 6 | 60 |

### 菜谱评分表 (recipe_ratings)

| 评分ID | 菜谱ID | 玩家ID | 评分 | 评分时间 |
|-------|-------|-------|-----|---------|
| rating_id | recipe_id | player_id | score | rating_time |
| int | int | int | float | datetime |
| 1 | 1001 | 101 | 9.5 | 2023-01-01 10:30:00 |
| 2 | 1002 | 102 | 8.0 | 2023-01-01 11:15:00 |

### 菜谱额外加分表 (recipe_extra_points)

| 记录ID | 菜谱ID | 额外加分 | 购买时间 |
|-------|-------|---------|---------|
| record_id | recipe_id | extra_points | purchase_time |
| int | int | float | datetime |
| 1 | 1001 | 5.0 | 2023-01-01 12:00:00 |
| 2 | 1002 | 3.5 | 2023-01-01 13:30:00 |

### 商店排行榜表 (store_rankings)

| 记录ID | 菜谱ID | 玩家ID | 排名 | 上架时间 | 销售数量 | 总收入 |
|-------|-------|-------|-----|---------|---------|-------|
| record_id | recipe_id | player_id | rank | listing_time | sales_count | total_revenue |
| int | int | int | int | datetime | int | float |
| 1 | 1001 | 101 | 1 | 2023-01-01 12:00:00 | 10 | 100.0 |
| 2 | 1002 | 102 | 2 | 2023-01-01 12:00:00 | 5 | 50.0 |

## Excel文件格式说明

1. 表名应为数据库表的中文名称
2. 第一行为字段的中文名
3. 第二行为字段的英文名
4. 第三行为字段的数据类型
5. 从第四行开始为实际数据

## 支持的数据类型

- int: 整数
- float: 浮点数
- string: 字符串
- datetime: 日期时间

## 配置文件使用说明

1. 奖励配置表用于定义不同排名范围的奖励内容
2. 付费加分限制表用于定义每日额外加分的限制和价格
3. 菜谱商店配置表用于定义商店排行榜的相关配置
4. 数据库导出功能可将游戏内数据导出为Excel格式，便于分析和备份