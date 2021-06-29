from dearpygui.core import *
from dearpygui.simple import *
import math

# cmd /K cd "$(CURRENT_DIRECTORY)" & "python.exe" "$(FULL_CURRENT_PATH)"
# Notepad++ mapped to [CTRL][SHIFT][NUM+]

doubleClickTimer = 0
radius = 50
bubbleColor = [ 255, 255, 255, 255 ]    # Bubble border color.
dragging = False                        # No drag at init.
target = None                           # Store the target tag while dragging.
fontsize = [ 6, 14 ]                    # This is a guess used to center the drawn text inside the state bubble.  (size=12)
numConnectPoints = 8                    # Number of connect points around a state.

# bubbleInfo
# BubbleX, BubbleY, BubbleTag, LabelTag, LabelXOffset, LabelYOffset
bubbleInfo = [ 
    [1*radius, radius, None, None, None, None], 
    [3*radius, radius, None, None, None, None], 
    [5*radius, radius, None, None, None, None], 
    [7*radius, radius, None, None, None, None] ]


class transitionInfo(object):
    __slots__ = [ 'state1', 'state2', 'linetag', 'arrow1tag', 'arrow2tag' ]
    def __init__(self, state1, state2, linetag, arrow1tag, arrow2tag):
        self.state1 = state1
        self.state2 = state2
        self.linetag = linetag
        self.arrow1tag = arrow1tag
        self.arrow2tag = arrow2tag
        
transitionInfoList = [ 
    transitionInfo(0, 1, None, None, None),
    transitionInfo(1, 2, None, None, None),
    transitionInfo(2, 3, None, None, None),
    transitionInfo(3, 0, None, None, None)
                     ]


# Connect point offsets about the center of a state.
connectPoints = [ [0,0] ]


def main_callback(sender, data):
    global doubleClickTimer
    global radius
    global dragging
    global bubbleColor
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
        for index, value in enumerate(bubbleInfo):
            distance = pow((mx - value[0]), 2) + pow((my - value[1]), 2)
            print(value[2] + ": " + str(distance))
            if closest > distance:
                closest = distance          # If this is closer, save the distance.
                target = index              # If this is closer, save the index.
                
        print("Target = " + str(target) + ", distance = ", str(distance) +", nameID=" + bubbleInfo[target][3])
        dragging = True
        print(bubbleInfo[index])
        
    if is_key_down(mvKey_Shift) and is_mouse_button_clicked(mvMouseButton_Left):
        set_value("Shift + Left Mouse Clicked", "True")
    
    if is_mouse_button_released(mvMouseButton_Left):
        dragging = False
        set_value("Left Mouse Clicked", "False")
        set_value("Shift + Left Mouse Clicked", "False")
        updateConnections(target)
        print("Release")
                
    if is_mouse_button_double_clicked(mvMouseButton_Left):
        set_value("Left Mouse Double Clicked", "True")
        doubleClickTimer=30
    else:
        if doubleClickTimer > 0:
            doubleClickTimer = doubleClickTimer - 1
        if doubleClickTimer == 0:
            set_value("Left Mouse Double Clicked", "False")
            
    if dragging:
        # Move the State Bubble.
        mouse = get_mouse_pos()
        modify_draw_command("drawing##widget", bubbleInfo[target][2], center=mouse)
        bubbleInfo[target][0] = mouse[0]
        bubbleInfo[target][1] = mouse[1]
        
        # Move the State Name Text.  Note that we have to apply the stored offset to center.
        position = [ (mouse[0] - bubbleInfo[target][4]), (mouse[1] - bubbleInfo[target][5]) ]
        modify_draw_command("drawing##widget", bubbleInfo[target][3], pos=position)
        
        updateConnections(target)


# updateConnections()
# 
# Draw each connecting line between states.
# Find the closest connect points on each state to the center of the other.
# Draw the line between the two points.
#
def updateConnections(target):
    for transition in transitionInfoList:
        orig = transition.state1
        dest = transition.state2
            
        if (orig == target) or (dest == target):
            #print(line)
            
            # The center of the state of the line origin.
            pc1 = bubbleInfo[orig][0:2]
            
            # The center of the state of the line destination.
            pc2 = bubbleInfo[dest][0:2]
            
            # find the closet edge point on the origin state.
            closest = float("inf")
            pe = [ 0, 0 ]
            for index, value in enumerate(connectPoints):
                pe[0] = connectPoints[index][0] + pc1[0]
                pe[1] = connectPoints[index][1] + pc1[1]
                distance = pow((pe[0] - pc2[0]), 2) + pow((pe[1] - pc2[1]), 2)
                
                if closest > distance:
                    closest = distance          # If this is closer, save the distance.
                    opt1 = index                # If this is closer, save the index.
                
            # find the closet edge point on the destination state.
            closest = float("inf")
            pe = [ 0, 0 ]
            for index, value in enumerate(connectPoints):
                pe[0] = connectPoints[index][0] + pc2[0]
                pe[1] = connectPoints[index][1] + pc2[1]
                distance = pow((pe[0] - pc1[0]), 2) + pow((pe[1] - pc1[1]), 2)
                
                if closest > distance:
                    closest = distance          # If this is closer, save the distance.
                    opt2 = index                # If this is closer, save the index.
                
            #print(opt2)
            
            p1 = [pc1[0] + connectPoints[opt1][0], pc1[1] + connectPoints[opt1][1]]
            p2 = [pc2[0] + connectPoints[opt2][0], pc2[1] + connectPoints[opt2][1]]
            
            modify_draw_command("drawing##widget", transition.linetag, p1=p1, p2=p2)
            
            
  
#
# Initialize the states and connections.
#
with window("Main Window"):
    
    # Create the drawing area.
    winSize = get_main_window_size()
    add_drawing("drawing##widget", width=winSize[0], height=winSize[1])
    draw_rectangle("drawing##widget", [0, winSize[1]], [winSize[0], 0], [255, 0, 0, 255], fill=[0, 0, 25, 255], rounding=12, thickness=1.0)
    
    # Initialize the visual objects.
    id = 0
    for state in bubbleInfo:
        #print(state)
        id = id + 1
        stateTag = "StateTag" + str(id)
        nameTag = "NameTag" + str(id)
        
        state[2] = stateTag
        state[3] = nameTag
        state[4] = (fontsize[0] * len(nameTag)) / 2
        state[5] = fontsize[1] / 2
        
        center = state[0:2]
        draw_circle("drawing##widget", center, radius, bubbleColor, tag=stateTag, thickness=2.0)
        
        position = center
        position[0] = position[0] - state[4]
        position[1] = position[1] - state[5]
        draw_text("drawing##widget", position, nameTag, color=bubbleColor, tag=nameTag, size=12)
    
    # Initialize a list with the connect point offset about the center of a state.
    del connectPoints[0]
    for n in range(numConnectPoints):
        theta = 2.0 * math.pi * n / numConnectPoints
        connectPoints.append([math.cos(theta)*radius, math.sin(theta)*radius])
    
    # Create a line for each entry in connectionInfo[].
    for index, transition in enumerate(transitionInfoList):
        lineTag = "Line" + str(index)
        p1 = [ (bubbleInfo[transition.state1][4]), (bubbleInfo[transition.state2][5]) ]
        p2 = [ (bubbleInfo[transition.state2][4]), (bubbleInfo[transition.state2][5]) ]
        
        draw_line("drawing##widget", p1, p2, bubbleColor, 2, tag=lineTag)
        #print(lineTag)
        transition.linetag = lineTag
        
    # Set the graphic renderer callback to support moving the visual objects.
    set_render_callback(main_callback)
    
# Start the framework.
start_dearpygui(primary_window="Main Window")

