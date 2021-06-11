from dearpygui.core import *
from dearpygui.simple import *

PressMax = 20
count = 0

def press_callback(sender, data):
    global count
    count = count + 1
    configure_item("string", label=str(count))
    configure_item("Slider", default_value=count)
    configure_item("label1", label=count)
    # ProgressBar
    value = get_value("ProgressBar")
    value = value + (1/PressMax)
    if value >= 1.0:
        value = 1.0
    set_value("ProgressBar", value)
    
    if(count >= PressMax):
        configure_item("Press Me", enabled=False)
        configure_item("ImageButton", enabled=False)


def press_exit(sender, data):
    stop_dearpygui()
    
    
    
with window("PressCounter"): 
    set_main_window_title('Press Counter')                                          # Sets the main window title text.
    set_main_window_size(300, 540)
    
    add_button("Press Me", callback=press_callback)                                 # Button with callback function.
    
    add_text("Max Value is " + str(PressMax))                                       # This text cannot be modified.
    add_label_text(name='label1', default_value="Show Count: ", label=str(count))   # This is a label and a display value.
    add_input_text("string", default_value="Press Count: ", label=str(count))       # This prompts and receives input.
    add_progress_bar("ProgressBar")                                                 # This is a progress indication widget.
    
    add_text('')
    add_slider_int("Slider", default_value=count, max_value=20)                     # This is an input widget.
    add_text('')
    add_image_button('ImageButton', value='python.png', callback=press_callback)
    add_text('')
    add_button("Exit", callback=press_exit)                                         # Add exit button.
    

start_dearpygui(primary_window="PressCounter")

