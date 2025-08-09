// Inventory Scene for Little Gourmet Game

var InventoryScene = cc.Scene.extend({
    onEnter: function () {
        this._super();
        
        var size = cc.winSize;
        
        // 添加背景
        var background = new cc.LayerColor(cc.color(240, 248, 255, 255)); // 爱丽丝蓝背景
        this.addChild(background);
        
        // 添加标题
        var titleLabel = new cc.LabelTTF("背包", "Arial", 36);
        titleLabel.setPosition(size.width / 2, size.height - 50);
        titleLabel.setColor(cc.color(70, 130, 180));
        this.addChild(titleLabel);
        
        // 添加返回按钮
        var backButton = new cc.MenuItemFont("返回", this.onBack, this);
        backButton.setFontSize(20);
        backButton.setPosition(100, size.height - 30);
        
        var menu = new cc.Menu(backButton);
        menu.setPosition(0, 0);
        this.addChild(menu);
        
        // 显示背包内容
        this.showInventory(size);
    },
    
    // 显示背包内容
    showInventory: function(size) {
        var inventory = playerManager.getInventory();
        
        if (inventory.length === 0) {
            // 背包为空
            var emptyLabel = new cc.LabelTTF("背包是空的", "Arial", 24);
            emptyLabel.setPosition(size.width / 2, size.height / 2);
            emptyLabel.setColor(cc.color(100, 100, 100));
            this.addChild(emptyLabel);
            return;
        }
        
        // 显示背包物品
        var yPos = size.height - 150;
        for (var i = 0; i < inventory.length; i++) {
            var itemInfo = inventory[i];
            var item = dataManager.getIngredientById(itemInfo.id);
            var itemName = item ? item.name : "未知物品";
            
            // 物品名称和数量
            var itemLabel = new cc.LabelTTF(
                itemName + " x " + itemInfo.quantity,
                "Arial",
                20
            );
            itemLabel.setPosition(size.width / 2, yPos);
            itemLabel.setColor(cc.color(0, 0, 0));
            this.addChild(itemLabel);
            
            yPos -= 50;
            
            // 如果位置太低，停止添加更多项目
            if (yPos < 100) {
                // 显示还有更多物品的提示
                var moreLabel = new cc.LabelTTF("还有更多物品...", "Arial", 18);
                moreLabel.setPosition(size.width / 2, yPos);
                moreLabel.setColor(cc.color(100, 100, 100));
                this.addChild(moreLabel);
                break;
            }
        }
    },
    
    // 返回按钮回调
    onBack: function() {
        cc.director.runScene(new MainMenuScene());
    }
});