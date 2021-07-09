#
# Program:      fsm.py
# Purpose:      Finite State Machine plotter
# Dependencies: Dear PyGui 0.8

import dearpygui.dearpygui as dpg
import dearpygui
import math

# Notepad Run code:
# cmd /K cd "$(CURRENT_DIRECTORY)" & "python.exe" "$(FULL_CURRENT_PATH)"
# Notepad++ mapped to [CTRL][SHIFT][NUM+]

radius = 50
bubbleColor = [ 255, 255, 255, 255 ]    # Bubble border color.
dragging = False                        # No drag at init.
target = None                           # Store the target tag while dragging.
fontsize = [ 6, 14 ]                    # This is a guess used to center the drawn text inside the state bubble.  (size=12)
numConnectPoints = 8                    # Number of connect points around a state.
myCircle = None

# bubbleInfo
# BubbleX, BubbleY, BubbleTag, LabelTag, LabelXOffset, LabelYOffset
bubbleInfo = [ 
    [1*radius, radius, None, None, None, None], 
    [3*radius, radius, None, None, None, None], 
    [5*radius, radius, None, None, None, None], 
    [7*radius, radius, None, None, None, None] ]


# class transitionInfo()
#
# Describe the line transitioning from one state to another.
#
class transitionInfo(object):
    __slots__ = [ 'state1', 'state2', 'item', 'arrow1tag', 'arrow2tag' ]
    def __init__(self, state1, state2, item, arrow1tag, arrow2tag):
        self.state1 = state1
        self.state2 = state2
        self.item = item
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



def mouse_down(sender, app_data, user_data):
    global target
    
    if app_data == 0:                                   # 0=left, 1=right, 2=center
        mouse = dpg.get_drawing_mouse_pos()
        mx = mouse[0]
        my = mouse[1]
        print("Left Mouse Clicked at " + str(mouse))
        
        # Find the closest state position to the mouse click using (mx - px)^2 + (my - py)^2.
        closest = float("inf")
        for index, value in enumerate(bubbleInfo):
            distance = pow((mx - value[0]), 2) + pow((my - value[1]), 2)
            
            if closest > distance:
                closest = distance          # If this is closer, save the distance.
                target = index              # If this is closer, save the index.
                
        print("Target = " + str(target) + ", distance = ", str(distance))
        dragging = True
        print(bubbleInfo[index])


def mouse_drag():
    global target
    global bubbleInfo
    global myCircle
    
    # Move the State Bubble.
    mouse = mouse = dpg.get_drawing_mouse_pos()
    
    dpg.configure_item(bubbleInfo[target][2], center=mouse)
    bubbleInfo[target][0] = mouse[0]
    bubbleInfo[target][1] = mouse[1]

    # Move the State Name Text.  Note that we have to apply the stored offset to center.
    position = [ (mouse[0] - bubbleInfo[target][4]), (mouse[1] - bubbleInfo[target][5]) ]
    #modify_draw_command("drawing##widget", bubbleInfo[target][3], pos=position)
    dpg.configure_item(bubbleInfo[target][3], pos=position)
    
    updateConnections(target)
    

def mouse_up():
    global target
    
    print("mouse_up()")
    updateConnections(target)
    print("Release")
    updateConnections(target, True)
    

# updateConnections()
# 
# Draw each connecting line between states.
# Find the closest connect points on each state to the center of the other.
# Draw the line between the two points.
#
def updateConnections(target, arrow=False):
    for transition in transitionInfoList:
        orig = transition.state1
        dest = transition.state2
            
        if (orig == target) or (dest == target):
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
                    optimum1 = index            # If this is closer, save the index.
                
            # find the closet edge point on the destination state.
            closest = float("inf")
            pe = [ 0, 0 ]
            for index, value in enumerate(connectPoints):
                pe[0] = connectPoints[index][0] + pc2[0]
                pe[1] = connectPoints[index][1] + pc2[1]
                distance = pow((pe[0] - pc1[0]), 2) + pow((pe[1] - pc1[1]), 2)
                
                if closest > distance:
                    closest = distance          # If this is closer, save the distance.
                    optimum2 = index            # If this is closer, save the index.
                
            p1 = [pc1[0] + connectPoints[optimum1][0], pc1[1] + connectPoints[optimum1][1]]
            p2 = [pc2[0] + connectPoints[optimum2][0], pc2[1] + connectPoints[optimum2][1]]
            
            dpg.configure_item(transition.item,  p1=p1, p2=p2)
     
    if arrow:
        print("Arrow")
            
            
  
dpg.setup_registries()

#
# Initialize the states and connections.
#
with dpg.window(label="Main Window"):
    
    # Create the drawing area.
    #winSize = dpg.get_main_window_size()
    winSize = [1024, 512]
    #dpg.add_drawing("drawing##widget", width=winSize[0], height=winSize[1])
    dpg.add_drawlist(width=winSize[0], height=winSize[1])
    #dpg.draw_rectangle("drawing##widget", [0, winSize[1]], [winSize[0], 0], [255, 0, 0, 255], fill=[0, 0, 25, 255], rounding=12, thickness=1.0)
    dpg.draw_rectangle([0, winSize[1]], [winSize[0], 0], color=[255, 0, 0, 255], fill=[0, 0, 25, 255], rounding=12, thickness=1.0)
    
    #with dpg.drawlist(width=300, height=300): # or you could use dpg.add_drawlist and set parents manually
    
    # Initialize the visual objects.
    id = 0
    for state in bubbleInfo:
        #print(state)
        id = id + 1
        #stateTag = "StateTag" + str(id)
        nameTag = "NameTag" + str(id)
        
        center = state[0:2]
        #draw_circle("drawing##widget", center, radius, bubbleColor, tag=stateTag, thickness=2.0)
        item = dpg.draw_circle(center, radius, color=bubbleColor, thickness=2.0)
        
        state[2] = item
        state[3] = None
        state[4] = (fontsize[0] * len(nameTag)) / 2
        state[5] = fontsize[1] / 2
        
        position = center
        position[0] = position[0] - state[4]
        position[1] = position[1] - state[5]

        item = dpg.draw_text(position, nameTag, color=bubbleColor, label=nameTag, size=12)
        state[3] = item
        
    # Initialize a list with the connect point offset about the center of a state.
    del connectPoints[0]
    for n in range(numConnectPoints):
        theta = 2.0 * math.pi * n / numConnectPoints
        connectPoints.append([math.cos(theta)*radius, math.sin(theta)*radius])
    
    # Create a line for each entry in connectionInfo[].
    for index, transition in enumerate(transitionInfoList):
        p1 = [ (bubbleInfo[transition.state1][4]), (bubbleInfo[transition.state2][5]) ]
        p2 = [ (bubbleInfo[transition.state2][4]), (bubbleInfo[transition.state2][5]) ]
        transition.item = dpg.draw_line(p1, p2, color=bubbleColor)
        
    # Set the graphic renderer callback to support moving the visual objects.
    #set_render_callback(main_callback)
    #dpg.add_mouse_drag_handler(callback=foo_callback)
    dpg.add_mouse_drag_handler(callback=mouse_drag, user_data=None)
    dpg.add_mouse_click_handler(callback=mouse_down, user_data=None)
    dpg.add_mouse_release_handler(callback=mouse_up, user_data=None)
    
    
# Start the framework.
dpg.start_dearpygui()

