from dearpygui.core import *
from dearpygui.simple import *

doubleClickTimer = 0
radius = 50
#circles = [ [1*radius, radius], [3*radius, radius], [5*radius, radius], [7*radius, radius] ]
#circles = [ [1*radius, radius, None], [3*radius, radius, None], [5*radius, radius, None], [7*radius, radius, None] ]
circles = [ [1*radius, radius, None, None], [3*radius, radius, None, None], [5*radius, radius, None, None], [7*radius, radius, None, None] ]

white = [ 255, 255, 255, 255 ]

dragging = False 
target = ""


def main_callback(sender, data):
    global doubleClickTimer
    global radius
    global dragging
    global white
    global target
    
    if is_mouse_button_dragging(mvMouseButton_Left, 10):
        set_value("Left Mouse Dragging", "True")
    else:
        set_value("Left Mouse Dragging", "False")

    if is_mouse_button_clicked(mvMouseButton_Left):
        set_value("Left Mouse Clicked", "True")
        mouse = get_mouse_pos()
        mx = mouse[0]
        my = mouse[1]
        print("Left Mouse Clicked at " + str(mouse[0]) + ", " + str(mouse[1]))
        
        # Find the closest state position to the mouse click using (mx - px)^2 + (my - py)^2.
        closest = float("inf")
        for index, value in enumerate(circles):
            distance = pow((mx - value[0]), 2) + pow((my - value[1]), 2)
            print(value[2] + ": " + str(distance))
            if closest > distance:
                closest = distance          # If this is closer, save the distance.
                target = index              # If this is closer, save the index.
                
        print("Target = " + str(target) + ", distance = ", str(distance) +", nameID=" + circles[target][3])
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
        mouse = get_mouse_pos()
        modify_draw_command("drawing##widget", circles[target][2], center=mouse)
        modify_draw_command("drawing##widget", circles[target][3], pos=mouse)
        circles[target][0] = mouse[0]
        circles[target][1] = mouse[1]
        


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
        #print(state)
        id = id + 1
        stateTag = "StateTag" + str(id)
        nameTag = "NameTag" + str(id)
        center = state[0:2]
        #print(stateTag)
        #print(center)
        draw_circle("drawing##widget", center, radius, white, tag=stateTag, thickness=2.0)
        draw_text("drawing##widget", center, str(id), color=white, tag=nameTag, size=12)
        state[2] = stateTag
        state[3] = nameTag
        
    set_render_callback(main_callback)
    
    
start_dearpygui(primary_window="Main Window")

