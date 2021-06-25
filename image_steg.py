from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import tkinter.font as font
import numpy as np
import math
import webbrowser
import base64

global path_image

image_display_size = 300, 300

new = 1
url = "https://www.gmail.com"

def OpenWeb():
	webbrowser.open(url,new=new)

def encode():
    enc = Toplevel()
    enc.title("Encode")
    enc.geometry("700x600")
    enc.configure(bg='lavender')
    Label(enc, text="SECRET DATA TRANSMISSION", bg="gray30", fg="snow",width="300", height="3", font=("Caliber", 13)).pack()
    sec_data = Label(enc, text="Enter secret data here", bg='lavender', fg="gray10",font=("Times New Roman", 15))
    sec_data.place(x=470, y=110)

    txt = Text(enc, wrap=WORD, width=30)
    txt.place(x=440, y=160, height=165)
    key = Label(enc,text="Enter secret key",bg='lavender', fg="gray10",font=("Times New Roman",15))
    key.place(x=20,y=400)

    #passw_var=tk.StringVar()
    #password=passw_var.get()
    #passw_var.set("")
    #passw_entry=tk.Entry(enc, textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')
    #passw_entry.place(x=20,y=430)
    
    
    txt_place=Text(enc,wrap=WORD, width=30)
    #txt_place.tag_configure("hidden", elide=True)
    txt_place.place(x=20,y=430,height = 30)

    def on_click():
        global path_image
        path_image = filedialog.askopenfilename()
        load_image = Image.open(path_image)
        load_image.thumbnail(image_display_size, Image.ANTIALIAS)
        np_load_image = np.asarray(load_image)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(enc, image=render)
        img.image = render
        img.place(x=20, y=145)

    def encrypt_data_into_image():
        global path_image
        data = txt.get(1.0, "end-1c")
        key = txt_place.get(1.0, "end-1c")
        res = encrypt(key, data)
        img = cv2.imread(path_image)
        data = [format(ord(i), '08b') for i in res]
        _, width, _ = img.shape
        PixReq = len(data) * 3

        RowReq = PixReq / width
        RowReq = math.ceil(RowReq)

        count = 0
        charCount = 0

        for i in range(RowReq + 1):
            while (count < width and charCount < len(data)):
                char = data[charCount]
                charCount += 1
                for index_k, k in enumerate(char):
                    if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                            k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                        img[i][count][index_k % 3] -= 1
                    if (index_k % 3 == 2):
                        count += 1
                    if (index_k == 7):
                        if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                            img[i][count][2] -= 1
                        if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                            img[i][count][2] -= 1
                        count += 1
            count = 0

        cv2.imwrite("encrypted_image.png", img)
        success_label = Label(enc, text="Encryption Successful!",
                              bg='lavender', fg="gray10",font=("Times New Roman", 20))
        success_label.place(x=240, y=500)
        

    def encrypt(key, clear):
        enc = []

        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) +
                         ord(key_c)) % 256)

            enc.append(enc_c)

        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    buttonFont = font.Font(family='Helvetica', size=11, weight='bold')


    buttonselect = Button(enc, text="Choose Image", bg="gray30",fg="snow",bd=3, font=buttonFont, command= on_click)
    buttonselect.place(x=100, y=100)


    buttonencode = Button(enc, text="Encode", bd=3, bg="gray30", fg="snow",font=buttonFont, command=encrypt_data_into_image)
    buttonencode.place(x=530, y=400)
    



def decode():
    dnc = Toplevel()
    dnc.title("Decode")
    dnc.geometry("600x600")
    dnc.configure(bg='lavender')
    Label(dnc, text="SECRET DATA TRANSMISSION", bg="gray30", fg = "snow",width="300", height="3", font=("Caliber", 13)).pack()
    l = Label(dnc, text="Key", bg="lavender",fg="gray30",font=("Times New Roman",15))
    l.place(x=20,y=100)
    T=Text(dnc,wrap=WORD, width=30)
    T.place(x=80,y=100,height = 30)
    
    
    def clickButton():
        global path_image
        path_image = filedialog.askopenfilename()
        load = Image.open(path_image)
        load.thumbnail(image_display_size, Image.ANTIALIAS)
        load = np.asarray(load)
        load = Image.fromarray(np.uint8(load))
        render = ImageTk.PhotoImage(load)
        img = Label(dnc, image=render)
        img.image = render
        img.place(x=200, y=200)


    def decrypt_data_from_image():
        global path_image
        key = T.get(1.0, "end-1c")
        img = cv2.imread(path_image)
        data = []
        stop = False
        for index_i, i in enumerate(img):
            i.tolist()
            for index_j, j in enumerate(i):
                if ((index_j) % 3 == 2):
                
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    if (bin(j[2])[-1] == '1'):
                        stop = True
                        break
                else:
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    data.append(bin(j[2])[-1])
            if (stop):
                break

        message = []
        
        for i in range(int((len(data) + 1) / 8)):
            message.append(data[i * 8:(i * 8 + 8)])
        
        message = [chr(int(''.join(i), 2)) for i in message]
        message = ''.join(message)
        res = decode(key, message)
        
        S=tk.Scrollbar(dnc)
        t=tk.Text(dnc,height=5,width=55)
        S.pack(side=tk.RIGHT,fill=tk.X)
        S.place(x=80,y=430)
        t.pack(side=tk.LEFT,fill=tk.X)
        t.place(x=80,y=430,height=100)
        S.config(command=t.yview)
        t.config(yscrollcommand=S.set)
        t.insert(tk.END,res)

    def decode(key, enc):
        dec = []
        
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)

            dec.append(dec_c)
        return "".join(dec)

    main_button = Button(dnc, text="Decrypt", bd=3, bg="gray30", fg="snow",font=buttonFont, command=decrypt_data_from_image)
    main_button.place(x=400, y=100)

    dec_button = Button(dnc, text="Choose Image", bg="gray30",fg="snow",bd=3, font=buttonFont, command= clickButton)
    dec_button.place(x=20, y=200)




stg = Tk()
stg.title("Secret Data Transmission")
stg.geometry("500x400+300+150")

stg.configure(bg='lavender')
Label(stg, text="SECRET DATA TRANSMISSION", bg="gray35", fg="snow",width="300", height="3", font=("Caliber", 13)).pack()

buttonFont = font.Font(family='Helvetica', size=11, weight='bold')
first=Button(stg, text="Encrypt", bg="gray35",fg="snow",height="2", width="20", bd=3, font=buttonFont, command=encode)
first.place(x=150, y=100)

second=Button(stg, text="Decrypt", bg="gray35",fg="snow",height="2", width="20", bd=3, font=buttonFont, command=decode)
second.place(x=150, y=200)

third=Button(stg,text="Share", bg="gray35", fg="snow",height="2",width="20", bd = 3 ,font=buttonFont,command=OpenWeb)
third.place(x=150,y=300)
stg.mainloop()
