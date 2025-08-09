# 更新游戏场景脚本以处理新UI元素
import godot
from api_manager import APIManager
from shared.models.player_model import Player
from src.i_recipe_manager import IRecipeManager
from src.i_decoration_manager import IDecorationManager

class GameScene(godot.Control):
    def _ready(self):
        # 初始化API管理器和玩家数据
        self.api_manager = APIManager()
        self.current_recipe = None
        
        # 获取或创建全局游戏管理器
        self.global_game_manager = self.get_node("/root/GlobalGameManager")
        if not self.global_game_manager:
            self.global_game_manager = GlobalGameManager()
            self.get_tree().get_root().add_child(self.global_game_manager)
        
        # 获取游戏核心组件
        self.recipe_manager = self.global_game_manager.get_recipe_manager()
        self.decoration_manager = self.global_game_manager.get_decoration_manager()
        self.audio_manager = self.global_game_manager.get_audio_manager()
        self.drag_manager = self.global_game_manager.get_ingredient_drag_manager()
        
        # 加载玩家数据
        saved_data = self.api_manager.load_game("slot1")
        if saved_data:
            self.player = Player.from_dict(saved_data)
        else:
            self.player = Player(1, "Player1")
        
        # 连接食材槽位信号
        self.ingredient_slots = []
        for i in range(1, 4):
            slot = self.get_node(f"IngredientArea/Slot{i}")
            if slot:
                # 不再直接连接gui_input，由IngredientSlot脚本处理
                # slot.connect("gui_input", self, "_on_ingredient_slot_input")
                slot.connect("mouse_entered", self, "_on_ingredient_slot_hover", [i])
                self.ingredient_slots.append(slot)
        
        # 获取烹饪锅节点
        self.cooking_pot = self.get_node("CookingPot")
        if self.cooking_pot:
            # 不再直接连接pressed，由CookingPot脚本处理
            # self.cooking_pot.connect("pressed", self, "_on_cooking_pot_pressed")
            self.cooking_pot.connect("mouse_entered", self, "_on_cooking_pot_hover")
        
        # 获取设置按钮并连接信号
        settings_button = self.get_node("SettingsButton")
        if settings_button:
            settings_button.connect("pressed", self, "_on_settings_pressed")
            settings_button.connect("mouse_entered", self, "_on_button_hover")
        
        # 获取菜谱书按钮并连接信号
        recipe_book_button = self.get_node("RecipeBookButton")
        if recipe_book_button:
            recipe_book_button.connect("pressed", self, "_on_recipe_book_pressed")
            recipe_book_button.connect("mouse_entered", self, "_on_button_hover")
        
        # 获取装饰品按钮并连接信号
        decoration_button = self.get_node("DecorationButton")
        if decoration_button:
            decoration_button.connect("pressed", self, "_on_decoration_pressed")
            decoration_button.connect("mouse_entered", self, "_on_button_hover")
            
        # 获取食材商店按钮并连接信号
        ingredient_shop_button = self.get_node("IngredientShopButton")
        if ingredient_shop_button:
            ingredient_shop_button.connect("pressed", self, "_on_ingredient_shop_pressed")
            ingredient_shop_button.connect("mouse_entered", self, "_on_button_hover")

        # 获取库存按钮并连接信号
        inventory_button = self.get_node("InventoryButton")
        if inventory_button:
            inventory_button.connect("pressed", self, "_on_inventory_pressed")
            inventory_button.connect("mouse_entered", self, "_on_button_hover")

            
        # 获取NPC聊天按钮并连接信号
        npc_chat_button = self.get_node("NPCChatButton")
        if npc_chat_button:
            npc_chat_button.connect("pressed", self, "_on_npc_chat_pressed")
            npc_chat_button.connect("mouse_entered", self, "_on_button_hover")
            
        # 获取邮件按钮并连接信号
        mail_button = self.get_node("MailButton")
        if mail_button:
            mail_button.connect("pressed", self, "_on_mail_pressed")
            mail_button.connect("mouse_entered", self, "_on_button_hover")
        
        # 初始化当前选择的食材
        self.selected_ingredient = None
        
        # 初始化音频和动画
        self.init_audio_and_animation()
        
        # 初始化一些示例食材到槽位中（用于测试）
        self.init_sample_ingredients()
        
        # 更新UI显示
        self.update_ui()

    def init_audio_and_animation(self):
        # 初始化音频和动画
        if self.audio_manager:
            # 播放背景音乐
            self.audio_manager.play_music("res://assets/sounds/music/background.ogg")
            
    def update_ui(self):
        # 更新玩家信息显示
        self.get_node("ChefHat").set_tooltip_text(f"等级：{self.player.level}\n经验：{self.player.experience}/{self.player._get_required_exp()}")
        
        # 更新金币显示
        coins_label = self.get_node("CoinsLabel")
        if coins_label:
            coins_label.text = f"金币: {self.player.currency}"
        
        # 更新库存显示
        inventory_label = self.get_node("InventoryLabel")
        if inventory_label:
            inventory_summary = self.player.get_inventory_summary()
            inventory_label.text = f"库存: {inventory_summary['total_items']}种 {inventory_summary['total_quantity']}个"
            
        # 更新美丽值显示
        beauty_label = self.get_node("BeautyLabel")
        if beauty_label:
            beauty_label.text = f"美丽值: {self.player.beauty}"

    def _on_ingredient_slot_input(self, event):
        # 处理食材拖放逻辑
        if isinstance(event, godot.InputEventMouseButton) and event.pressed:
            # 开始选择食材
            self.selected_ingredient = event.target
            godot.print("Selected ingredient slot")
            if self.audio_manager:
                self.audio_manager.play_predefined_sound("ingredient_select")
        elif isinstance(event, godot.InputEventDragBegin):
            # 开始拖拽食材
            godot.print("Started dragging ingredient")
        elif isinstance(event, godot.InputEventDrop):
            # 食材放置逻辑
            if event.target == self.cooking_pot:
                # 将食材放入烹饪锅
                godot.print("Ingredient placed in cooking pot")
                self.add_ingredient_to_pot(event.target)
                if self.audio_manager:
                    self.audio_manager.play_predefined_sound("ingredient_drop")

    def _on_ingredient_slot_hover(self, slot_index):
        # 处理食材槽位悬停
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("hover", 0.5)

    def _on_cooking_pot_hover(self):
        # 处理烹饪锅悬停
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("hover", 0.5)

    def _on_button_hover(self):
        # 处理按钮悬停
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("hover", 0.5)

    def add_ingredient_to_pot(self, ingredient_slot):
        # 将食材添加到烹饪锅中
        ingredient_id = int(ingredient_slot.name.replace("Slot", "")) - 1
        godot.print(f"Adding ingredient {ingredient_id} to pot")
        
        # 这里可以添加具体的食材处理逻辑

    def _on_cooking_pot_pressed(self):
        # 处理烹饪操作
        godot.print("Started cooking")
        
        # 播放烹饪音效
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("cooking_complete")
        
        # 检查是否满足菜谱条件
        selected_ingredients = [int(slot.name.replace("Slot", "")) - 1 for slot in self.ingredient_slots]
        recipe_id = self.recipe_manager.check_recipe_complete(selected_ingredients)
        
        if recipe_id:
            # 添加经验奖励
            self.player.add_experience(50)
            godot.print(f"食谱完成！获得经验奖励 ID:{recipe_id}")
            
            # 播放成就解锁音效
            if self.audio_manager:
                self.audio_manager.play_predefined_sound("achievement_unlock")
        else:
            godot.print("食谱未完成")
            
        # 保存游戏进度
        self.api_manager.save_game("slot1", self.player.to_dict())
        
        # 更新UI
        self.update_ui()

    def check_recipe_complete(self, selected_ingredients):
        # 简单的菜谱检查逻辑（示例）
        # 实际应检查当前放入的食材是否符合某个菜谱
        return True

    def _on_settings_pressed(self):
        # 处理设置按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        settings_scene_path = "res://assets/scenes/settings_scene.tscn"
        settings_scene = godot.load(settings_scene_path)
        if settings_scene:
            self.get_tree().set_current_scene(settings_scene)

    def _on_recipe_book_pressed(self):
        # 处理菜谱书按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        recipe_book_scene_path = "res://assets/scenes/recipe_book_scene.tscn"
        recipe_book_scene = godot.load(recipe_book_scene_path)
        if recipe_book_scene:
            self.get_tree().set_current_scene(recipe_book_scene)

    def _on_custom_recipe_pressed(self):
        # 处理自创菜谱按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        custom_recipe_scene_path = "res://assets/scenes/custom_recipe_scene.tscn"
        custom_recipe_scene = godot.load(custom_recipe_scene_path)
        if custom_recipe_scene:
            self.get_tree().set_current_scene(custom_recipe_scene)
            
            
    def _on_beauty_recipe_pressed(self):
        # 处理美容菜谱按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        beauty_recipe_scene_path = "res://assets/scenes/beauty_recipe_scene.tscn"
        beauty_recipe_scene = godot.load(beauty_recipe_scene_path)
        if beauty_recipe_scene:
            self.get_tree().set_current_scene(beauty_recipe_scene)

    def _on_collection_pressed(self):
        # 处理菜谱收集按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        collection_scene_path = "res://assets/scenes/recipe_collection_scene.tscn"
        collection_scene = godot.load(collection_scene_path)
        if collection_scene:
            self.get_tree().set_current_scene(collection_scene)
                    
    def _on_rating_pressed(self):
        # 处理菜谱评分按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        rating_scene_path = "res://assets/scenes/recipe_rating_scene.tscn"
        rating_scene = godot.load(rating_scene_path)
        if rating_scene:
            self.get_tree().set_current_scene(rating_scene)
    
    def _on_npc_chat_pressed(self):
        # 处理NPC聊天按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        npc_chat_scene_path = "res://assets/scenes/npc_chat_scene.tscn"
        npc_chat_scene = godot.load(npc_chat_scene_path)
        if npc_chat_scene:
            self.get_tree().set_current_scene(npc_chat_scene)

    def _on_mail_pressed(self):
        # 处理邮件按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        mail_scene_path = "res://assets/scenes/mail_scene.tscn"
        mail_scene = godot.load(mail_scene_path)
        if mail_scene:
            self.get_tree().set_current_scene(mail_scene)

    def _on_decoration_pressed(self):
        # 处理装饰品按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        decoration_shop_scene_path = "res://assets/scenes/decoration_shop_scene.tscn"
        decoration_shop_scene = godot.load(decoration_shop_scene_path)
        if decoration_shop_scene:
            self.get_tree().set_current_scene(decoration_shop_scene)

    def _on_inventory_pressed(self):
        # 处理库存按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        inventory_scene_path = "res://assets/scenes/inventory_scene.tscn"
        inventory_scene = godot.load(inventory_scene_path)
        if inventory_scene:
            self.get_tree().set_current_scene(inventory_scene)
            
    def _on_ingredient_shop_pressed(self):
        # 处理食材商店按钮点击
        if self.audio_manager:
            self.audio_manager.play_predefined_sound("button_click")
            
        ingredient_shop_scene_path = "res://assets/scenes/ingredient_shop_scene.tscn"
        ingredient_shop_scene = godot.load(ingredient_shop_scene_path)
        if ingredient_shop_scene:
            self.get_tree().set_current_scene(ingredient_shop_scene)