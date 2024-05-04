import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
import tkinter.font as font
from tkinter import ttk
import runpy;



class TextRecognitionApp:

    

    def __init__(self):
        self.root = tk.Tk()
        

        self.root.attributes('-fullscreen', True)

        self.root.resizable(True,True)

        self.root.config(bg='#383838')

        self.menubar = tk.Menu(self.root,bg='black',fg="white")
        self.filemenu = tk.Menu(self.menubar, tearoff='false',bg='#383838',fg='white')
        self.filemenu.add_command(label="Exit", command=lambda:self.exit())
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)




        welcometext = ttk.Label(self.root, text="Intelligent Text Recognition",font=font.Font(family="Fonarto",size=70) ,justify="center",background='#383838',foreground="white")
        welcometext.grid(row=0, column=0, pady=20, columnspan=3)



        # Create button to trigger text recognition
        self.recognize_button = tk.Button(self.root, text="Recognize Text",background='#383838',font=font.Font(family="Fonarto",size=25),foreground="white",compound = 'center',relief='ridge',command=self.recognize_text)
        self.recognize_button.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        # Create button to save text to a file
        self.save_button = tk.Button(self.root, text="Save Text File",background='#383838',font=font.Font(family="Fonarto",size=25),foreground="white",compound = 'center',relief='ridge',command=self.save_text_file, state="disabled")
        self.save_button.grid(row=1, column=1, padx=40, pady=40, sticky="nsew")

        self.text = ""
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        runpy.run_path(path_name='PhotoEditor.py')
    


    def recognize_text(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename()

        # Check if a file is selected
        if file_path:
            # Open the image using PIL
            img = Image.open(file_path)

            # Perform text recognition using pytesseract
            self.text = pytesseract.image_to_string(img)

            # Enable save button after text recognition
            self.save_button.config(state="normal")

            # Create a new window to display recognized text
            #--------------self.display_text_window(self.text)

    def save_text_file(self):
        # Open file dialog to choose where to save the text file
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        # Check if a file path is provided for saving
        if save_path:
            # Write the recognized text to the selected file
            with open(save_path, "w") as file:
                file.write(self.text)
                file.close()
                print(f"Text saved to {save_path}")

    def display_text_window(self, text):
        # Create a new window to display recognized text
        text_window = tk.Toplevel(self.root)
        text_window.title("Recognized Text")

        # Display the recognized text
        text_label = tk.Label(text_window, text=text, wraplength=500)
        text_label.pack()


