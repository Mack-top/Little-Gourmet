Kitchen Story API 文档
=====================

欢迎阅读 Kitchen Story 游戏的 API 文档。本文档详细描述了游戏各个模块的接口和使用方法。

.. toctree::
   :maxdepth: 2
   :caption: 客户端模块:

   client_core
   client_managers
   client_utils
   client_network

.. toctree::
   :maxdepth: 2
   :caption: 共享模块:

   shared_models

.. toctree::
   :maxdepth: 2
   :caption: 服务端模块:

   server_api
   server_dao
   server_services

介绍
----

Kitchen Story 是一个面向女性玩家的烹饪模拟游戏，包含丰富的食材管理、菜谱制作、厨房装饰和模拟经营等玩法。

核心功能模块
-----------

1. **玩家系统** - 管理玩家信息、等级、经验和货币
2. **食材系统** - 管理食材的新鲜度、质量和库存
3. **菜谱系统** - 管理菜谱的解锁、制作和奖励
4. **装饰系统** - 管理厨房装饰品的购买、放置和展示
5. **成就系统** - 管理游戏成就的解锁和奖励
6. **经营系统** - 管理餐厅经营和收入
7. **网络系统** - 处理客户端与服务器的通信

开发指南
--------

请参考 `开发指南 <../development_guide.md>`_ 获取更多开发相关信息。

索引和表格
----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`