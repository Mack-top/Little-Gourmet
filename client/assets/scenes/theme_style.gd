# 统一主题样式文件
# 定义清新田园风格的颜色和样式

# 背景颜色
const BACKGROUND_COLOR = Color(0.88, 0.96, 0.85, 1)

# 面板颜色
const PANEL_COLOR = Color(0.9, 0.95, 0.85, 0.9)
const PANEL_BORDER_COLOR = Color(0.6, 0.8, 0.5, 1)

# 文本颜色
const TEXT_COLOR = Color(0.3, 0.6, 0.2, 1)
const TEXT_HOVER_COLOR = Color(0.4, 0.7, 0.3, 1)
const TEXT_PRESSED_COLOR = Color(0.2, 0.5, 0.1, 1)

# 面板样式
static func create_panel_style():
	var style = StyleBoxFlat.new()
	style.bg_color = PANEL_COLOR
	style.border_color = PANEL_BORDER_COLOR
	style.border_width_left = 2
	style.border_width_top = 2
	style.border_width_right = 2
	style.border_width_bottom = 2
	style.corner_radius_top_left = 15
	style.corner_radius_top_right = 15
	style.corner_radius_bottom_right = 15
	style.corner_radius_bottom_left = 15
	return style

# 按钮样式
static func apply_button_style(button):
	button.add_color_override("font_color", TEXT_COLOR)
	button.add_color_override("font_color_hover", TEXT_HOVER_COLOR)
	button.add_color_override("font_color_pressed", TEXT_PRESSED_COLOR)