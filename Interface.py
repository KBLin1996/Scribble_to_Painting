import tkinter as tk
import os
import subprocess, platform
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import PIL.Image
import PIL.ImageTk
import matlab.engine
import time
import _thread
import shutil



class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns='*', logfunc=print):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc
        self.style=8
        self.cnt=0
    def on_created(self, event):
        self.cnt=self.cnt+1
        if os.path.basename(event.src_path)[-3:]!='png':
            self.log(os.path.basename(event.src_path) + " has been created", filename=os.path.basename(event.src_path), flag=1)
        time.sleep(1)
        if os.path.basename(event.src_path)[-3:]=='png':
            if self.cnt%2 == 0 :
                self.log(os.path.basename(event.src_path) + " has been created", filename=os.path.basename(event.src_path)
                                        ,filepath=event.src_path, flag=1)
                print(event.src_path)
                #start=time.time()
                #my_img1=PIL.Image.open(event.src_path)
                #my_img1.show()
                self.log("Now Setting...",filename=os.path.basename(event.src_path),style=self.style,cnt=self.cnt,filepath=event.src_path,flag=2)
    
                #end=time.time()
                #self.log("transfer accomplished,total time:%d" %(end-start))            
        #print("??")
        #self.log("123")
    def on_deleted(self, event):
        self.log(os.path.basename(event.src_path) + " deleted")

    def on_modified(self, event):
        self.log(os.path.basename(event.src_path) + " has been modified")

    def on_moved(self, event):
        self.log("moved " + os.path.basename(event.src_path) + " to " + os.path.basename(event.dest_path)) 
    
    def set_style(self,style=0):
        self.style=style

class my_UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('AI Painting Transfer')
        self.window.geometry('830x850')
        #self.back=tk.Frame(self.window,width=1000,height=1000,bg='black')
        #self.back.place(x=0,y=0)
        self.window.resizable(0, 0) # Not allow resizing in the x or y direction
        self.watchdog = None
        self.watch_path = '.'
        self.msgbox=tk.Frame(self.window)
        self.msgbox_var=tk.StringVar()
        self.msgbox_label=tk.Label(self.msgbox, relief=tk.SUNKEN, anchor=tk.W,
                           textvariable=self.msgbox_var,bg='dim gray',font=('Times New Roman', 10),fg='ghost white')
        self.label = tk.Label(self.window, bg='SlateGray2', width=46, height=1, text='Painting Style', font=('Times New Roman', 16))
        self.label.place(x=60, y=260)        
        self.my_title2=PIL.Image.open('Paintings/title/image25_style8.png')
        self.my_title2=self.my_title2.resize((int(220*self.my_title2.size[0]/self.my_title2.size[1]),220),PIL.Image.BILINEAR)
        self.my_title2=PIL.ImageTk.PhotoImage(self.my_title2)
        self.title_img2=tk.Label(self.window,image=self.my_title2,text='title2')
        self.title_img2.place(x=450,y=20)
        #self.scrollbar = None
        #self.frame=tk.Frame(self.window,height=100)
        #self.frame.place(x=60,y=670)
        self.t_style=8
        self.t_cnt=0
        self.t_filepath='E:/Scribble_to_Painting/input/1.jpg'
        self.t_filename='1.jpg'
        self.t_lock=0
        #self.frame2=tk.Frame(self.window,width=460,height=180)#,background='')
        #self.frame2.place(x=350,y=650)
        
        #self.f1 = tk.Listbox(self.frame,width=27,height=5)
        #self.scrollbar = tk.Scrollbar(self.frame,orient="vertical")
        self.eng= matlab.engine.start_matlab()


        my_title1=PIL.Image.open('Paintings/title/image_25_region_1.png')
        my_title1=my_title1.resize((int(220*my_title1.size[0]/my_title1.size[1]),220),PIL.Image.BILINEAR)
        my_title1=PIL.ImageTk.PhotoImage(my_title1)
        title_img1=tk.Label(self.window,image=my_title1,text='title1')
        title_img1.place(x=100,y=20)
        
        my_arrow1=PIL.Image.open('Paintings/title/right-arrow_new.png')
        my_arrow1=my_arrow1.resize((int(60*my_arrow1.size[0]/my_arrow1.size[1]),60),PIL.Image.BILINEAR)
        my_arrow1=PIL.ImageTk.PhotoImage(my_arrow1)
        arrow_img1=tk.Label(self.window,image=my_arrow1,text='arrow1')
        arrow_img1.place(x=350,y=90)
        #風格
        b_img1=self.my_image(filename='Paintings/Degas/Degas.gif')
        label_img1=tk.Label(self.window,image=b_img1,text='Degas')
        label_img1.place(x=80,y=470)
        b_img2=self.my_image(filename='Paintings/Escher/Escher.gif')
        label_img2=tk.Label(self.window,image=b_img2,text='Escher')
        label_img2.place(x=270,y=470)
        b_img3=self.my_image(filename='image_test/style/3.jpg')
        label_img3=tk.Label(self.window,image=b_img3,text='Kandinsky')
        label_img3.place(x=460,y=470)
        b_img4=self.my_image(filename='image_test/style/4.jpg')
        label_img4=tk.Label(self.window,image=b_img4,text='Lifshutz')
        label_img4.place(x=650,y=470)
        b_img5=self.my_image(filename='Paintings/Magritte/Magritte.gif')
        label_img5=tk.Label(self.window,image=b_img5,text='Magritte')
        label_img5.place(x=80,y=320)
        b_img6=self.my_image(filename='image_test/style/6.jpg')
        label_img6=tk.Label(self.window,image=b_img6,text='Monet')
        label_img6.place(x=270,y=320)
        b_img7=self.my_image(filename='image_test/style/7.jpg')
        label_img7=tk.Label(self.window,image=b_img7,text='Pierre-Auguste_Renoir')
        label_img7.place(x=460,y=320)
        b_img8=self.my_image(filename='Paintings/van Gogh/van_Gogh.gif')
        label_img8=tk.Label(self.window,image=b_img8,text='van_Gogh')
        label_img8.place(x=650,y=320)
        
        self.var = tk.StringVar()
        r1 = tk.Radiobutton(self.window, text='Degas',
                            variable=self.var, value='Degas',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r1.place(x=80, y=580)

        r2 = tk.Radiobutton(self.window, text='Escher',
                            variable=self.var, value='Escher',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r2.place(x=270, y=580)
        
        r3 = tk.Radiobutton(self.window, text='Kandinsky',
                            variable=self.var, value='Kandinsky',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r3.place(x=460, y=580)
        
        r4 = tk.Radiobutton(self.window, text='Lifshitz',
                            variable=self.var, value='Lifshitz',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r4.place(x=650, y=580)
        
        r5 = tk.Radiobutton(self.window, text='Magritte',
                            variable=self.var, value='Magritte',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r5.place(x=80, y=420)
        
        r6 = tk.Radiobutton(self.window, text='Monet',
                            variable=self.var, value='Monet',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r6.place(x=270, y=420)
        
        r7 = tk.Radiobutton(self.window, text='Renoir',
                            variable=self.var, value='Renoir',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r7.place(x=460, y=420)
        
        r8 = tk.Radiobutton(self.window, text='van Gogh',
                            variable=self.var, value='van Gogh',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        r8.place(x=650, y=420)

        #history
        self.mypath = "tmp"
        self.history()
        
        #按鈕
        
        b1 = tk.Button(self.window,text='Start\nTransfer',
                       command=self.callback,width=14,height=2,bg='SkyBlue3',bd=5)
        b1.place(x=525,y=745)
        b2 = tk.Button(self.window,text='Start\nWatching',
                       command=self.start_watchdog,width=14,height=2,bg='LightSkyBlue2',bd=5)
        b2.place(x=670,y=685)
        b2 = tk.Button(self.window,text='Stop\nWatching',
                       command=self.stop_watchdog,width=14,height=2,bg='LightSkyBlue2',bd=5)
        b2.place(x=670,y=745)
        b2 = tk.Button(self.window,text='Select',
                       command=self.select_path,width=14,height=2,bg='LightSkyBlue2',bd=5)
        b2.place(x=525,y=685)
        b2 = tk.Button(self.window,text='New\nstyle',
                       command=self.UploadAction,width=14,height=2,bg='LightSkyBlue2',bd=5)
        b2.place(x=380,y=685)        
        b2 = tk.Button(self.window,text='Open\nResult',
                       command=self.callback_openresult,width=14,height=2,bg='LightSkyBlue2',bd=5)
        b2.place(x=380,y=745)
        self.window.mainloop()

    def my_image(self,filename=""):
        b_img_1=PIL.Image.open(filename)
        b_img_1=b_img_1.resize((int(100*b_img_1.size[0]/b_img_1.size[1]),100),PIL.Image.BILINEAR)
        b_img1=PIL.ImageTk.PhotoImage(b_img_1)
        return b_img1

    def history(self):
        """
        files = os.listdir(self.mypath)        
        for f in files:
            self.f1.insert(tk.END, f)
        self.f1.pack(side="left",fill="y")
        self.scrollbar.pack(side="right", fill="y")
        self.f1.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.f1.yview)
        """
        l = tk.Label(self.window, 
            text="Now: "+self.t_filename,
            bg='SlateGray2',
            font=('Times New Roman', 16),
            width=20, height=1
            )
        l.place(x=60, y=640)
        b_img_1=PIL.Image.open(self.t_filepath)
        v = int(140*b_img_1.size[0]/b_img_1.size[1])
        if v>300:
            v=300
        b_img_1=b_img_1.resize((v,140),PIL.Image.BILINEAR)
        b_img1=PIL.ImageTk.PhotoImage(b_img_1)
        self.b_img_user=b_img1
        self.label_img8=tk.Label(self.window,image=self.b_img_user,text='user')
        self.label_img8.place(x=60,y=680)


    def open_myfilepath(self, filepath='tmp'):
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
    def UploadAction(self,event=None):
        filename= filedialog.askopenfilename()
        print('Selected:', filename)
        if os.path.exists('image_test/style/9.jpg'):
            os.remove('image_test/style/9.jpg')
        shutil.copyfile(filename, 'image_test/style/9.jpg')
        #os.popen('copy C:/Users/steve/Desktop/scribble2drawing-master/scribble2drawing-master/image_test/style/9.png '+filename)
        #os.rename(filename,'image_test/style/9.png')
        self.r = tk.Radiobutton(self.window, text='other',
                            variable=self.var, value='other',
                            font=('Times New Roman', 16),
                            command=self.print_selection)
        self.r.place(x=650,y=810)
        self.style=9
        self.print_selection()
        #self.watchdog.set_style(style=9)
    def callback_openresult(self):
        self.open_myfilepath(filepath='C:/Users/steve/Desktop/scribble2drawing-master/scribble2drawing-master/result/final')
    def callback(self):
        #self.open_myfilepath(filepath=self.mypath)
        self.log("Now Loading...")
        if self.t_lock==0:
            self.t_lock=1
            _thread.start_new_thread(self.start_mat, (self.t_style,self.t_cnt,self.t_filepath))
            #self.t_lock=0
            print("Open Matlab Succeed!")
        elif self.t_lock==1:
            print("Unable to Open Matlab")
    def mytitle(self,path='Paintings/title/image25_style8.png'):
        self.my_title2=PIL.Image.open(path)
        self.my_title2=self.my_title2.resize((int(220*self.my_title2.size[0]/self.my_title2.size[1]),220),PIL.Image.BILINEAR)
        self.my_title2=PIL.ImageTk.PhotoImage(self.my_title2)
        self.title_img2=tk.Label(self.window,image=self.my_title2,text='title2')
        self.title_img2.place(x=450,y=20)
        
    def print_selection(self):
        self.label.config(text = 'Painting Style:  ' + self.var.get(), font=('Times New Roman', 16))
        if self.var.get()=='van Gogh':
            self.mytitle(path='Paintings/title/image25_style8.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=8)
                self.t_style=8
        elif self.var.get()=='Renoir':
            self.mytitle(path='Paintings/title/image25_style7.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=7)
                self.t_style=7
        elif self.var.get()=='Monet':
            self.mytitle(path='Paintings/title/image25_style6.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=6)
                self.t_style=6
        elif self.var.get()=='Magritte':
            self.mytitle(path='Paintings/title/image25_style5.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=5)
                self.t_style=5
        elif self.var.get()=='Lifshitz':
            self.mytitle(path='Paintings/title/image25_style4.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=4)
                self.t_style=4
        elif self.var.get()=='Kandinsky':
            self.mytitle(path='Paintings/title/image25_style3.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=3)
                self.t_style=3
        elif self.var.get()=='Escher':
            self.mytitle(path='Paintings/title/image25_style2.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=2)
                self.t_style=2
        elif self.var.get()=='Degas':
            self.mytitle(path='Paintings/title/image25_style1.png')
            if self.watchdog !=None:
                self.watchdog.set_style(style=1)
                self.t_style=1
        elif self.var.get()=='other':
            self.mytitle(path='image_test/style/9.jpg')
            if self.watchdog !=None:
                self.watchdog.set_style(style=9)
                self.t_style=9
    def start_watchdog(self):
        if self.watchdog is None:
            self.history()
            self.watchdog = Watchdog(path=self.watch_path, logfunc=self.log)
            self.watchdog.start()
            self.open_myfilepath(filepath="C:\Windows\System32\mspaint.exe")
            self.log('AI Painting Transfer started')
        else:
            self.history()
            self.log('AI Painting Transfer already started')

    def stop_watchdog(self):
        if self.watchdog:
            self.history()
            self.watchdog.stop()
            self.watchdog = None
            self.log('AI Painting Transfer stopped')
        else:
            self.history()
            self.log('AI Painting Transfer is not running')

    def select_path(self):
        self.mypath = filedialog.askdirectory()
        if self.mypath:
            self.history()
            self.watch_path = self.mypath
            self.log("Selected path: " + self.mypath)

    def start_mat(self,my_style,my_cnt,my_filepath):
        result = self.eng.main(my_filepath, my_cnt, my_style)
        my_img1=PIL.Image.open(result)
        my_img1.show()  
        self.log("Transfer Completed")
        self.t_lock=0
    def log(self, message,filename="",flag=0,style=0,cnt=0,filepath=''):
        self.msgbox_var.set(message)
        self.msgbox_label.pack()
        self.msgbox.place(width=500,height=100,x=0,y=830)
        print(message)
        if flag==1:
            #self.f1.insert(tk.END, filename)
            self.history()
        elif flag==2:
            self.t_style=style
            self.t_cnt=cnt
            self.t_filepath=filepath
            self.t_filename=filename
            self.history()
            #self.start_mat(my_style=style,my_cnt=cnt,my_filepath=filepath)

        
if __name__ == '__main__':
    my_UI()