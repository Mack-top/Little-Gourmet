// Little Gourmet Game Entry Point
// Using Cocos2d-JS

// 导入所有场景
var MainMenuScene = require('src/scenes/MainMenuScene.js');
var GameScene = require('src/scenes/GameScene.js');
var KitchenScene = require('src/scenes/KitchenScene.js');
var RecipeBookScene = require('src/scenes/RecipeBookScene.js');
var RecipeDetailScene = require('src/scenes/RecipeDetailScene.js');
var InventoryScene = require('src/scenes/InventoryScene.js');

// 导入管理器
var DataManager = require('src/managers/DataManager.js');
var PlayerManager = require('src/managers/PlayerManager.js');

// 导入系统
var CookingSystem = require('src/systems/CookingSystem.js');

cc.game.onStart = function(){
    cc.view.setDesignResolutionSize(800, 600, cc.ResolutionPolicy.SHOW_ALL);
    cc.view.resizeWithBrowserSize(true);
    
    // 加载所有数据
    dataManager.loadAllData();
    
    // 初始化玩家
    playerManager.initializePlayer();
    
    // Load main scene
    cc.director.runScene(new MainMenuScene());
};
cc.game.run();