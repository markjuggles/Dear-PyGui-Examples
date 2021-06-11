# Program: polling.py
# Purpose: Poll for keyboard and mouse events.
# Source:  https://discourse.dearimgui.org/t/distinguish-between-drag-click-double-click-after-mouse-release/283
#          Had to add "with window():" and change add_label_text() "value" to "default_value".

from dearpygui.core import *
from dearpygui.simple import *

doubleClickTimer = 0


def main_callback(sender, data):
    global doubleClickTimer
    
    set_value("Mouse Position", str(get_mouse_pos()))

    if is_key_down(mvKey_A):
        set_value("A key Down", "True")
    else:
        set_value("A key Down", "False")

    if is_key_pressed(mvKey_A):
        set_value("A key Pressed", "True")
    else:
        set_value("A key Pressed", "False")

    if is_key_released(mvKey_A):
        set_value("A key Released", "True")
    else:
        set_value("A key Released", "False")

    if is_mouse_button_dragging(mvMouseButton_Left, 10):
        set_value("Left Mouse Dragging", "True")
    else:
        set_value("Left Mouse Dragging", "False")

    if is_mouse_button_clicked(mvMouseButton_Left):
        set_value("Left Mouse Clicked", "True")
    
    if is_key_down(mvKey_Shift) and is_mouse_button_clicked(mvMouseButton_Left):
        set_value("Shift + Left Mouse Clicked", "True")
    
    if is_mouse_button_released(mvMouseButton_Left):
        set_value("Left Mouse Clicked", "False")
        set_value("Shift + Left Mouse Clicked", "False")
                
    if is_mouse_button_double_clicked(mvMouseButton_Left):
        set_value("Left Mouse Double Clicked", "True")
        doubleClickTimer=30
    else:
        if doubleClickTimer > 0:
            doubleClickTimer = doubleClickTimer - 1
        if doubleClickTimer == 0:
            set_value("Left Mouse Double Clicked", "False")
    



with window("main_window"):
    set_main_window_title('Polling Demo')
    set_main_window_size(800, 400)
    
    add_label_text("A key Down", default_value="False", color=[0, 200, 255])
    add_label_text("A key Pressed", default_value="False", color=[0, 200, 255])
    add_label_text("A key Released", default_value="False", color=[0, 200, 255])
    add_spacing()
    add_label_text("Mouse Position", default_value="(0,0)", color=[0, 200, 255])
    add_label_text("Left Mouse Clicked", default_value="False", color=[0, 200, 255])
    add_label_text("Left Mouse Dragging", default_value="False", color=[0, 200, 255])
    add_label_text("Left Mouse Double Clicked", default_value="False", color=[0, 200, 255])
    add_label_text("Shift + Left Mouse Clicked", default_value="False", color=[0, 200, 255])
    
    set_render_callback(main_callback)


#start_dearpygui()
start_dearpygui(primary_window="main_window")
