from dearpygui.core import *
from dearpygui.simple import *

doubleClickTimer = 0
radius = 50
circles = [ [1*radius, radius], [3*radius, radius], [5*radius, radius], [7*radius, radius] ]
white = [ 255, 255, 255, 255 ]
dragging = False 


def main_callback(sender, data):
    global doubleClickTimer
    global radius
    global dragging
    global white
    
    if is_mouse_button_dragging(mvMouseButton_Left, 10):
        set_value("Left Mouse Dragging", "True")
    else:
        set_value("Left Mouse Dragging", "False")

    if is_mouse_button_clicked(mvMouseButton_Left):
        set_value("Left Mouse Clicked", "True")
        print("Left Mouse Clicked at " + str(get_mouse_pos()))
        dragging = True
    
    if is_key_down(mvKey_Shift) and is_mouse_button_clicked(mvMouseButton_Left):
        set_value("Shift + Left Mouse Clicked", "True")
    
    if is_mouse_button_released(mvMouseButton_Left):
        dragging = False
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
            
    if dragging:
        #modify_draw_command("drawing##widget","movingCircle", center=get_mouse_pos(), radius=radius, color=white, thickness=2.0)
        modify_draw_command("drawing##widget","StateTag1", center=get_mouse_pos(), radius=radius, color=white, thickness=2.0)


with window("Main Window"):

    winSize = get_main_window_size()
    #winSize = [800, 600]
    #add_drawing("drawing##widget", width=800, height=500)
    #draw_rectangle("drawing##widget", [0, 500], [800, 0], [255, 0, 0, 255], fill=[0, 0, 25, 255], rounding=12, thickness=1.0)
    print(str(winSize[0]) + ", " + str(winSize[1]))
    add_drawing("drawing##widget", width=winSize[0], height=winSize[1])
    
    draw_rectangle("drawing##widget", [0, winSize[1]], [winSize[0], 0], [255, 0, 0, 255], fill=[0, 0, 25, 255], rounding=12, thickness=1.0)
    #draw_circle("drawing##widget", circles[0], radius, white, tag="movingCircle", thickness=2.0)
    
    id = 0
    for state in circles:
        print(state)
        id = id + 1
        stateTag = "StateTag" + str(id)
        print(stateTag)
        draw_circle("drawing##widget", state, radius, white, tag=stateTag, thickness=2.0)
    
    set_render_callback(main_callback)
    
    
start_dearpygui(primary_window="Main Window")

