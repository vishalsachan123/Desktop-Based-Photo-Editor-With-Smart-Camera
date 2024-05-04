import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import btnhover
import Edit
import Collage
import Text_Recognization
import my_smart_camera

def recognizeText():
    home.destroy()
    Text_Recognization.TextRecognitionApp()
    

def startCam():
    my_smart_camera.myCam()


def editImage():
    home.destroy()
    a1=Edit.Image()
    
def createCollage():
    home.destroy()
    a2=Collage.collage()

home = tk.Tk()
home.title("SmartPhotoEditor")
home.iconbitmap('res/icon.ico')
home.option_add("*tearOff", False)
#home.geometry("1920x1080")#"1200x700"
home.attributes('-fullscreen', True)
home.config(bg='#383838')
home.columnconfigure(index=0, weight=1)
home.columnconfigure(index=1, weight=1)
home.rowconfigure(index=0, weight=1)
home.rowconfigure(index=1, weight=1)
home.rowconfigure(index=2, weight=1)
home.resizable(True,True)

menu = tk.Menu(home,bg='black',fg="white")
filemenu = tk.Menu(menu, tearoff='false',bg='#383838',fg='white')
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda:home.destroy())
menu.add_cascade(label="File", menu=filemenu)
home.config(menu=menu)

photo1 = tk.PhotoImage(file = r"res/edit.png")
photo1= photo1.subsample(2, 2)
photo2 = tk.PhotoImage(file = r"res/collage.png")
photo2= photo2.subsample(2, 2)

photo3 = tk.PhotoImage(file = r"res/smart_cam.png")
photo3 = photo3.subsample(2, 2)

photo4 = tk.PhotoImage(file = r"res/text_icon.png")
photo4 = photo4.subsample(2, 2)




# Label
welcometext = ttk.Label(home, text="Welcome  to  PhotoEditor",font=font.Font(family="Fonarto",size=45) ,justify="center",background='#383838',foreground="white")
welcometext.grid(row=0, column=0, pady=20, columnspan=3)
c1 = tk.Button(home, text="Edit",background='#383838',font=font.Font(family="Fonarto",size=25),foreground="white",image=photo1,compound = 'center',relief='ridge',command=lambda:editImage())
c1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
btnhover.changeOnHover(c1, "#4A4A4A", "#383838",'Edit pictures',1000)

c2 = tk.Button(home, text="Collage",background='#383838',font=font.Font(family="Fonarto",size=25),foreground="white",image=photo2,compound = 'center',relief='ridge',command=lambda:createCollage())
c2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
btnhover.changeOnHover(c2, "#4A4A4A", "#383838",'Create Collages',1000)


c3 = tk.Button(home, text="Smart Camera",background='#383838',font=font.Font(family="Fonarto",size=25),foreground="white",image=photo3,compound = 'center',relief='ridge',command=lambda:startCam())
c3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
btnhover.changeOnHover(c3, "#006CFF", "#383838",'Edit picture',1000)


c4 = tk.Button(home, text="Intelligent Text Recognition",background='#383838',font=font.Font(family="Fonarto",size=25),image=photo4,foreground="white",compound = 'center',relief='ridge',command=lambda:recognizeText())
c4.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
btnhover.changeOnHover(c4, "#FF9300", "#383838",'Edit pictures',1000)

home.mainloop()

