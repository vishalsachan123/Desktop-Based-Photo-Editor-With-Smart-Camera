from tkinter import *
from idlelib.tooltip import Hovertip
  
# function to change properties of button on hover
def changeOnHover(button, colorOnHover, colorOnLeave, hoverinfo , delay):
  
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover,foreground="#8BF3FF"))
    #Hovertip(button,hoverinfo, hover_delay=delay)
    # background color on leaving widget
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave,foreground="white"))