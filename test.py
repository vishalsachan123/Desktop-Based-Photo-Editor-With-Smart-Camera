import tkinter
import btnhover
from PIL import ImageTk,Image,ImageOps,ImageEnhance,ImageGrab,ImageFilter
import PIL
from tkinter import filedialog,colorchooser
from tkinter.filedialog import askopenfilename,asksaveasfilename
import tkinter.font as font
import os
import numpy
import runpy
from idlelib.tooltip import Hovertip

class Image:
    #global imageprogress,prgcount
    #Opening Image
    def doOpenImg(self):
        global selectedImage,imgsrc
        self.ImageEdit.delete('all')
        selectedImage = filedialog.askopenfilename(filetypes=[("Image File","*.jpg"),("Image File","*.png")]) 
        imgsrc = PIL.Image.open(selectedImage)
        self.w,self.h = imgsrc.size
        self.img=imgsrc.copy()
        self.img.thumbnail((800,800))
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
    
    #Save as
    def doSaveAsImg(self):
        file=asksaveasfilename(filetypes=[("All Files","*.*"),("PNG file","*.png"),("jpg file","*.jpg")])
        tempimg=self.img.resize((self.w,self.h))
        img1 = ImageTk.PhotoImage(tempimg)
        tempimg.save(file)

    #Drawing on image
    def choose_color(self):
        global color
        color= colorchooser.askcolor(title ="Choose color")
        colorbox.configure(bg=color[1])
    def pensize(self,scalevalue):
        global colw
        colw=scalevalue
    def get_x_and_y(self,event):
        global lasx, lasy
        lasx, lasy = event.x, event.y
    def draw_smth(self,event):
        global lasx, lasy
        try:
            self.ImageEdit.create_polygon((lasx, lasy, event.x, event.y),fill=color[1],outline=color[1],width=colw)
            lasx, lasy = event.x, event.y
        except NameError:
            try:
                self.ImageEdit.create_polygon((lasx, lasy, event.x, event.y),fill=color[1],outline=color[1],width='1')
                lasx, lasy = event.x, event.y
            except NameError:
                self.ImageEdit.create_polygon((lasx, lasy, event.x, event.y),fill='black',outline='black',width='1')
                lasx, lasy = event.x, event.y
        x=self.root.winfo_rootx()+self.ImageEdit.winfo_x()
        y=self.root.winfo_rooty()+self.ImageEdit.winfo_y()
        x1=x+self.ImageEdit.winfo_width()
        y1=y+self.ImageEdit.winfo_height()
        self.img=ImageGrab.grab().crop((x,y,x1,y1))
    
    def DrawOnImg(self,canvas,widget):
        global colorbox
        for items in widget.winfo_children():
            items.destroy()
        canvas.bind("<Button-1>", self.get_x_and_y)
        canvas.bind("<B1-Motion>",self.draw_smth)
        drawLabel = tkinter.Label(widget,bg='#383838',text = "Draw",fg='white', font=font.Font(size=15, weight='bold'))
        drawLabel.grid(row=0,column=0,padx=10,pady=20,columnspan=3)
        colorbtn = tkinter.Button(widget, text = "Select color",command = self.choose_color)
        colorbtn.grid(row=1,column=0)
        try:
            colorbox = tkinter.Canvas(widget, width="20", height="20",relief='groove',bg=color[1])
            colorbox.grid(row=1,column=1,padx=10)
        except:
            colorbox = tkinter.Canvas(widget, width="20", height="20",relief='groove',bg='#383838')
            colorbox.grid(row=1,column=1,padx=10)
        try:
            colorsize = tkinter.Scale(widget, from_=1, to=60,label=' set size ',length=170, orient='horizontal',
                              bg='#383838',fg='white',command=self.pensize)
            colorsize.set(colw)
            colorsize.grid(row=2,column=0,pady=15,padx=10,columnspan=3)
        except:
            colorsize = tkinter.Scale(widget, from_=1, to=60,label=' set size ',length=170, orient='horizontal',
                              bg='#383838',fg='white',command=self.pensize)
            colorsize.grid(row=2,column=0,pady=15,padx=10,columnspan=3)
        
    def doTransform(self,canvas,widget):
        for items in widget.winfo_children():
            items.destroy()
        canvas.unbind("<Button 1>");canvas.unbind("<B1-Motion>")
        resizeLabel = tkinter.Label(widget,bg='#383838',text = "Resize",fg='white', font=font.Font(size=15, weight='bold'))
        resizeLabel.grid(row=0,column=0,padx=10,pady=20,columnspan=2)
        wLabel = tkinter.Label(widget, bg='#383838',text = "Width",fg='white')
        wLabel.grid(row=1,column=0,padx=10)
        wText = tkinter.Entry(widget,width=7)
        wText.insert(0, self.w)
        wText.grid(row=1,column=1,padx=10)
        hLabel = tkinter.Label(widget, bg='#383838',text = "Height",fg='white')
        hLabel.grid(row=2,column=0,padx=10)
        hText = tkinter.Entry(widget,width=7)
        hText.insert(0, self.h)
        hText.grid(row=2,column=1,padx=10)
        tkinter.Label(widget,bg='#383838',text = "-------------------------------",fg='white').grid(row=3,column=0,columnspan=2,pady=10)
        rotateLabel = tkinter.Label(widget,bg='#383838',text = "Rotate",fg='white', font=font.Font(size=15, weight='bold'))
        rotateLabel.grid(row=4,column=0,padx=10,pady=20,columnspan=2)
        lr = tkinter.Button(widget, bg='#383838',text = "⤺",fg='white',font=font.Font(size=15, weight='bold'),command=lambda:self.doRotate(90))
        lr.grid(row=5,column=0,padx=10,pady=5)
        rr = tkinter.Button(widget, bg='#383838',text = "⤼",fg='white',font=font.Font(size=15, weight='bold'),command=lambda:self.doRotate(-90))
        rr.grid(row=5,column=1,padx=10,pady=5)
        tkinter.Label(widget,bg='#383838',text = "-------------------------------",fg='white').grid(row=6,column=0,columnspan=2,pady=10)
        flipLabel = tkinter.Label(widget,bg='#383838',text = "Flip",fg='white', font=font.Font(size=15, weight='bold'))
        flipLabel.grid(row=7,column=0,padx=10,pady=20,columnspan=2)
        hflip = tkinter.Button(widget, bg='#383838',text = "⬄",fg='white',font=font.Font(size=15, weight='bold'),command=lambda:self.doFlip("h"))
        hflip.grid(row=8,column=0,padx=10,pady=5)
        vflip = tkinter.Button(widget, bg='#383838',text = "⇳",fg='white',font=font.Font(size=15, weight='bold'),command=lambda:self.doFlip("v"))
        vflip.grid(row=8,column=1,padx=10,pady=5)

    def doRotate(self,angle):
        temp=self.w
        self.w=self.h
        self.h=temp
        self.img = self.img.rotate(angle, PIL.Image.NEAREST, expand = 1)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
        
    def doFlip(self,val):
        if(val=="h"):
            self.img = ImageOps.mirror(self.img)
        elif(val=="v"):
            self.img = ImageOps.flip(self.img)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
    
    def doAdjust(self,canvas,widget):
        for items in widget.winfo_children():
            items.destroy()
        canvas.unbind("<Button 1>");canvas.unbind("<B1-Motion>")
        global adjustimage
        adjustimage=self.img.copy()
        brightbutton= tkinter.Button(widget,text="Brightness",background='#383838',foreground="white",width=10, command=lambda:showSlider(1,widget))
        brightbutton.grid(row=0,column=0,padx=10,pady=20,columnspan=2)
        self.hover.changeOnHover(brightbutton, "#4A4A4A", "#383838",'change brightness',1000)
        
        contrastbutton= tkinter.Button(widget,text="Contrast",background='#383838',foreground="white",width=10, command=lambda:showSlider(2,widget))
        contrastbutton.grid(row=2,column=0,padx=10,pady=20,columnspan=2)
        self.hover.changeOnHover(contrastbutton, "#4A4A4A", "#383838",'change contrast',1000)
        
        huebutton= tkinter.Button(widget,text="Hue",background='#383838',foreground="white",width=10, command=lambda:showSlider(3,widget))
        huebutton.grid(row=4,column=0,padx=10,pady=20,columnspan=2)
        self.hover.changeOnHover(huebutton, "#4A4A4A", "#383838",'change hue',1000)
        
        saturatebutton= tkinter.Button(widget,text="Saturation",background='#383838',foreground="white",width=10, command=lambda:showSlider(4,widget))
        saturatebutton.grid(row=6,column=0,padx=10,pady=20,columnspan=2)
        self.hover.changeOnHover(saturatebutton, "#4A4A4A", "#383838",'change saturation',1000)
        
        sharpbutton= tkinter.Button(widget,text="Sharpness",background='#383838',foreground="white",width=10, command=lambda:showSlider(5,widget))
        sharpbutton.grid(row=8,column=0,padx=10,pady=20,columnspan=2)
        self.hover.changeOnHover(sharpbutton, "#4A4A4A", "#383838",'change sharpness',1000)
        
        applybutton=tkinter.Button(widget,text="Apply",background='white',foreground="#383838",font=font.Font(family="Fonarto",size=15), command=lambda:applyadjust())
        applybutton.grid(row=10,column=0,padx=10,pady=80,columnspan=2)
        self.hover.changeOnHover(applybutton, "Red", "#383838",'Apply Changes',1000)
        
    
        def showSlider(value,widget):
            for items in widget.winfo_children():
                if isinstance(items,tkinter.Scale):
                    items.destroy()
            if value==1:
                brightscale = tkinter.Scale(widget, from_=0.1, to=2.0,resolution=0.1,length=200, orient='horizontal',
                              bg='#383838',fg='white',command=self.doBrightness)
                brightscale.set(1)
                brightscale.grid(row=1,column=0,padx=10,pady=20,columnspan=2)
            elif value==2:
                contrastscale = tkinter.Scale(widget, from_=0.1, to=2.0,resolution=0.1,length=200, orient='horizontal',
                              bg='#383838',fg='white',command=self.doContrast)
                contrastscale.set(1)
                contrastscale.grid(row=3,column=0,padx=10,pady=20,columnspan=2)
            elif value==3:
                huescale = tkinter.Scale(widget, from_=0.1, to=2.0,resolution=0.1,length=200, orient='horizontal',
                              bg='#383838',fg='white',command=self.doHue)
                huescale.set(1)
                huescale.grid(row=5,column=0,padx=10,pady=20,columnspan=2)
            elif value==4:
                saturationscale = tkinter.Scale(widget, from_=0.1, to=2.0,resolution=0.1,length=200, orient='horizontal',
                                  bg='#383838',fg='white',command=self.doSaturation)
                saturationscale.set(1)
                saturationscale.grid(row=7,column=0,padx=10,pady=20,columnspan=2)
            elif value==5:
                sharpnessscale = tkinter.Scale(widget, from_=-1.0, to=3.0,resolution=0.1,length=200, orient='horizontal',
                              bg='#383838',fg='white',command=self.doSharpness)
                sharpnessscale.set(1)
                sharpnessscale.grid(row=9,column=0,padx=10,pady=20,columnspan=2)
            
        def applyadjust():
            self.doAdjust(self.ImageEdit,self.toolwidget)
            
        
    
    def doBrightness(self,value):
        value1=float(value)
        tempimg1 = ImageEnhance.Brightness(adjustimage)    
        self.img = tempimg1.enhance(value1)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
    
    
    def doContrast(self,value):
        value1=float(value)
        tempimg1 = ImageEnhance.Contrast(adjustimage)    
        self.img = tempimg1.enhance(value1)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
    
    def doSharpness(self,value):
        value1=float(value)
        tempimg1 = ImageEnhance.Sharpness(adjustimage)    
        self.img = tempimg1.enhance(value1)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
        
    def doSaturation(self,value):
        value1=float(value)
        tempimg1 = ImageEnhance.Color(adjustimage)    
        self.img = tempimg1.enhance(value1)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
        
    def doHue(self,value):
        value1=float(value)
        tempimg1 = ImageEnhance.Color(adjustimage)    
        self.img = tempimg1.enhance(value1)
        img1 = ImageTk.PhotoImage(self.img)
        w1,h1=self.img.size
        self.ImageEdit.configure(width=w1,height=h1)
        self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
        self.ImageEdit.image=img1
    
    def doFilters(self,canvas,widget):
        for items in widget.winfo_children():
            items.destroy()
        canvas.unbind("<Button 1>");canvas.unbind("<B1-Motion>")
        global filteredimage
        filteredimage=self.img.copy()
        f0=tkinter.Button(widget,width=15,height=2,text="None",command=lambda:nofilter())
        f0.grid(row=0,column=0,padx=10,pady=10)
        f1=tkinter.Button(widget,width=15,height=2,text="Black & White", command=lambda:bwfilter())
        f1.grid(row=1,column=0,padx=10,pady=10)
        f2=tkinter.Button(widget,width=15,height=2,text="Blur",command=lambda:blurfilter())
        f2.grid(row=2,column=0,padx=10,pady=10)
        f3=tkinter.Button(widget,width=15,height=2,text="Pixelise",command=lambda:pixelfilter())
        f3.grid(row=3,column=0,padx=10,pady=10)
        f4=tkinter.Button(widget,width=15,height=2,text="Invert",command=lambda:invertfilter())
        f4.grid(row=4,column=0,padx=10,pady=10)
        f5=tkinter.Button(widget,width=15,height=2,text="Sepia",command=lambda:sepiafilter())
        f5.grid(row=5,column=0,padx=10,pady=10)
        f6=tkinter.Button(widget,width=15,height=2,text="Red",command=lambda:redfilter())
        f6.grid(row=6,column=0,padx=10,pady=10)
        f7=tkinter.Button(widget,width=15,height=2,text="Green",command=lambda:greenfilter())
        f7.grid(row=7,column=0,padx=10,pady=10)
        f8=tkinter.Button(widget,width=15,height=2,text="Blue",command=lambda:bluefilter())
        f8.grid(row=8,column=0,padx=10,pady=10)
        
        
        
        
        def nofilter():
            self.img=filteredimage
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
    
        def bwfilter():
            tempimg1 = ImageEnhance.Color(filteredimage)    
            self.img = tempimg1.enhance(0)
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
            
        def sepiafilter():
            def get_sepia_pixel(red, green, blue, alpha):
                tRed = int((0.393 * red) + (0.769 * green) + (0.189 * blue))
                tGreen = int((0.349 * red) + (0.686 * green) + (0.168 * blue))
                tBlue = int((0.272 * red) + (0.534 * green) + (0.131 * blue))
                return tRed, tGreen, tBlue, alpha
            self.img=filteredimage
            w1,h1=self.img.size
            img1=filteredimage.copy()
            pixels = img1.load()
            for i in range(0, w1, 1):
                for j in range(0, h1, 1):
                    p = img1.getpixel( (i, j))
                    pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)
            self.img=img1        
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
        
        def invertfilter():
            self.img = filteredimage.copy()
            img_array=numpy.array(self.img)
            img_array=255-img_array
            self.img=PIL.Image.fromarray(img_array)
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
            
        def blurfilter():
            self.img=filteredimage.filter(ImageFilter.BoxBlur(5))
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
        
        def pixelfilter():
            w1,h1=self.img.size
            img1=filteredimage.copy()
            img1=img1.resize((100, 100))
            img1=img1.resize((w1, h1),PIL.Image.NEAREST)
            self.img=img1
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
            
        def redfilter():
            def get_pixel(red, green, blue, alpha):
                tRed = int((0.100 * red) + (0.500 * green) + (0.500 * blue))
                tGreen = int((0 * red) + (0 * green) + (0 * blue))
                tBlue = int((0 * red) + (0 * green) + (0 * blue))
                return tRed, tGreen, tBlue, alpha
            self.img=filteredimage
            w1,h1=self.img.size
            img1=filteredimage.copy()
            pixels = img1.load()
            for i in range(0, w1, 1):
                for j in range(0, h1, 1):
                    p = img1.getpixel( (i, j))
                    pixels[i, j] = get_pixel(p[0], p[1], p[2], 255)
            self.img=img1        
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
            
        def greenfilter():
            def get_pixel(red, green, blue, alpha):
                tRed = int((0 * red) + (0 * green) + (0* blue))
                tGreen = int((0.500 * red) + (0.100 * green) + (0.500 * blue))
                tBlue = int((0 * red) + (0 * green) + (0 * blue))
                return tRed, tGreen, tBlue, alpha
            self.img=filteredimage
            w1,h1=self.img.size
            img1=filteredimage.copy()
            pixels = img1.load()
            for i in range(0, w1, 1):
                for j in range(0, h1, 1):
                    p = img1.getpixel( (i, j))
                    pixels[i, j] = get_pixel(p[0], p[1], p[2], 255)
            self.img=img1        
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
            
        def bluefilter():
            def get_pixel(red, green, blue, alpha):
                tRed = int((0 * red) + (0 * green) + (0 * blue))
                tGreen = int((0 * red) + (0 * green) + (0* blue))
                tBlue = int((0.500 * red) + (0.500 * green) + (0.100 * blue))
                return tRed, tGreen, tBlue, alpha
            self.img=filteredimage
            w1,h1=self.img.size
            img1=filteredimage.copy()
            pixels = img1.load()
            for i in range(0, w1, 1):
                for j in range(0, h1, 1):
                    p = img1.getpixel( (i, j))
                    pixels[i, j] = get_pixel(p[0], p[1], p[2], 255)
            self.img=img1        
            img1 = ImageTk.PhotoImage(self.img)
            w1,h1=self.img.size
            self.ImageEdit.configure(width=w1,height=h1)
            self.ImageEdit.create_image((w1/2)+1.5,(h1/2)+1.5,image=img1)
            self.ImageEdit.image=img1
    
    def donothing():
        a=0;
    def exit(self):
        self.root.destroy()
        runpy.run_path(path_name='PhotoEditor.py')

    def __init__(self):
        self.img="";self.h=0;self.w=0;
        #window
        self.root = tkinter.Tk()
        self.root.title("Photo editor")
        self.root.geometry('1320x920')
        self.root.config(bg='#383838')
        self.root.iconbitmap('icon.ico')
        self.root.grid_rowconfigure(0, weight=1,minsize=5)
        self.root.grid_columnconfigure(1, weight=1,minsize=5)
        self.root.resizable(0, 0)
        
        self.hover=btnhover

        #menubar
        self.menubar = tkinter.Menu(self.root,bg='black',fg="white")
        self.filemenu = tkinter.Menu(self.menubar, tearoff='false',bg='#383838',fg='white')
        self.filemenu.add_command(label="Open", command=lambda:self.doOpenImg())
        self.filemenu.add_command(label="Save", command=lambda:self.donothing)
        self.filemenu.add_command(label="Save as...", command=lambda:self.doSaveAsImg())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=lambda:self.exit())
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)

        #Photo display screen
        self.ImageEdit = tkinter.Canvas(self.root, width="900", height="900",relief='raised',bg='#383838')      
        self.ImageEdit.grid(row=0,column=1)

        #Tools frame
        self.toolwidget=tkinter.Frame(self.root,padx=10, pady=100,bg="#383838")
        self.toolwidget.grid(row=0,column=2,sticky="nswe")

        #buttons frame with buttons
        self.btnwidget=tkinter.Frame(self.root,padx=10, pady=100,bg="#383835")
        self.btnwidget.grid(row=0,column=0,sticky="nswe")

        self.b1=tkinter.Button(self.btnwidget,text="🖌",bg="#383838",fg='white', activebackground="#DFDFDF",relief='ridge',
                  font=font.Font(size=15, weight='bold'),command=lambda:self.DrawOnImg(self.ImageEdit,self.toolwidget))
        self.b1.grid(row=0,column=0,padx=10, pady=5)
        self.hover.changeOnHover(self.b1, "#4A4A4A", "#383838",'Drawing tool \nDraw on Images.',1000)
        #Hovertip(b1,'Drawing tool \nDraw on Images.', hover_delay=1000)

        self.b2=tkinter.Button(self.btnwidget,text ="🗗",bg="#383838",fg='white', activebackground="#DFDFDF",relief='ridge',
                  font=font.Font(size=15, weight='bold'),command=lambda:self.doTransform(self.ImageEdit,self.toolwidget))
        self.b2.grid(row=0,column=1,padx=10, pady=5)
        self.hover.changeOnHover(self.b2, "#4A4A4A", "#383838",'Transform \nPerform Image Transformation (Resize, Rotate, etc).',1000)

        self.b3=tkinter.Button(self.btnwidget,text ="☀",bg="#383838",fg='white', activebackground="#DFDFDF",relief='ridge',
                  font=font.Font(size=15, weight='bold'),command=lambda:self.doAdjust(self.ImageEdit,self.toolwidget))
        self.b3.grid(row=1,column=0,padx=10, pady=5)
        self.hover.changeOnHover(self.b3, "#4A4A4A", "#383838",'Adjust \nChange color brightness, saturation, hue, etc',1000)

        self.b4=tkinter.Button(self.btnwidget,text ="",bg="#383838",fg='white', activebackground="#DFDFDF",relief='ridge',
                  font=font.Font(size=15, weight='bold'),command=lambda:self.doFilters(self.ImageEdit,self.toolwidget))
        self.b4.grid(row=1,column=1,padx=10, pady=5)
        self.hover.changeOnHover(self.b4, "#4A4A4A", "#383838",'Filters \nAdd filters',1000)
        
        self.doOpenImg()
        self.root.mainloop()
