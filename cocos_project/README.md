# Little Gourmet - Cocos Creator Version

这是 Little Gourmet 游戏的 Cocos Creator 版本，用于替代原有的 Godot 版本。

## 项目结构

```
cocos_project/
├── index.js              # 入口点
├── package.json          # 项目配置
├── project.json          # Cocos 项目配置
├── README.md             # 本文件
├── start_cocos.bat       # 启动脚本
├── src/
│   ├── scenes/           # 游戏场景
│   │   ├── MainMenuScene.js     # 主菜单场景
│   │   ├── GameScene.js         # 游戏场景
│   │   ├── KitchenScene.js      # 厨房场景
│   │   ├── RecipeBookScene.js   # 食谱手册场景
│   │   ├── RecipeDetailScene.js # 食谱详情场景
│   │   └── InventoryScene.js    # 背包场景
│   ├── managers/         # 管理器模块
│   │   ├── DataManager.js   # 数据管理器
│   │   └── PlayerManager.js # 玩家管理器
│   └── systems/          # 系统模块
│       └── CookingSystem.js # 烹饪系统
├── assets/               # 游戏资源
│   ├── images/           # 图像资源
│   ├── sounds/           # 音频文件
│   └── ...
└── ...
```

## 如何运行

1. 安装 Cocos Creator 或 Cocos2d-JS
2. 导航到本目录
3. 运行 `cocos run` 或在 Cocos Creator 中打开项目

或者使用本地 Web 服务器:
```bash
python -m http.server 8000
```
然后在浏览器中打开 http://localhost:8000

## Cocos 的优势

- **更好的 Windows 兼容性** - 避免了 Godot 的配置问题
- **更简单的设置过程** - 安装和配置更加直观
- **良好的 2D 支持** - 非常适合烹饪模拟游戏
- **JavaScript 支持** - 使用更常见的编程语言
- **强大的移动端支持** - 更容易部署到移动平台

## 核心功能

1. **主菜单** - 游戏入口，显示玩家信息
2. **厨房系统** - 制作食物的核心功能
3. **食谱手册** - 查看已解锁的食谱
4. **背包系统** - 管理拥有的食材
5. **数据管理** - 管理游戏中的食材和食谱数据
6. **玩家系统** - 管理玩家等级、经验和金币

## 下一步计划

1. 导入原有的美术资源
2. 实现商店系统
3. 添加成就系统
4. 完善烹饪机制
5. 连接后端服务
6. 添加音效和背景音乐
7. 实现存档功能