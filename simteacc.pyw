import os,sys,asyncio
import tkinter.font as tkf
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from tkinter import *
from math import log
from PIL import Image, ImageTk
from algo import trunc
from algo import exec as parser
from itertools import cycle
# from copy import deepcopy

root = Tk()
frame_scale=.85

def scl(orig, f=False, c=0):
    orig*=scale if c==0 else infinity if c==1 else donovan if c==2 else (infinity+donovan)/2
    if f: return float(orig)
    return int(orig)

sw=root.winfo_screenwidth()
sh=root.winfo_screenheight()
ww=round(int(sw)*0.8)
wh=round(ww/16*9)
fw=round(ww*frame_scale)
fh=round(wh*frame_scale)
px=round((sw-ww)/2)
py=abs(round((sh-wh)/2)-50)
print(f"[LOG]: SW: {sw}, SH: {sh}")
print(f"[LOG]: Width: {ww}, Height:{wh}")
print(f"[LOG]: FW: {fw}, FH:{fh}")

results, plot=[],[]
l_colors=cycle('rbgcmy')
placed_varis=False
signs=("+","-","*","/","=")
psign=("*","/")
nsign=("+","-","=")
numbs=("0","1","2","3","4","5","6","7","8","9")
varis=("x","y")
scale=ww/1229
truth=1 if scale<=1 else -1
infinity=pow(scale,3.5*(log(scale+1.3,1e6)-log(1,1e6))*10*truth)
donovan=pow(scale,3.5*(log(scale+.1,1e7)-log(1,1e7))*10*truth)
inches=0.0104166667
print(scale,infinity,donovan)

# Create app window
root.title("SimTeACC Final")
root.resizable(False, False)
root.geometry(f"{ww}x{wh}+{px}+{py}")

def res_path(rel_path):
    try: base_path=sys._MEIPASS
    except AttributeError: base_path=os.path.abspath('.')
    return os.path.join(base_path,rel_path)

def clear_output():
    for widgets in output_frame.winfo_children():
        widgets.destroy()
    outputLine.position=0

async def simulate_click(w):
    w.config(relief = "sunken")
    root.update_idletasks()
    await asyncio.sleep(.035)
    w.config(relief = "raised")
    w.invoke()

def add_text(word):
    global cycTyp, curTyp, results, plot
    curTyp['w'].config(state='normal')
    text=curTyp['w'].get(1.0,'end-1c')
    ll=text[-1] if text else ''
    if word=="b":
        if ll!='':
            if ll in '+=-()':
                if ll=='(':
                    curTyp['bo'].pop(-1)
                elif ll==')':
                    curTyp['bc'].pop(-1)
                curTyp['s'].pop(-1)
            elif ll in 'xy':
                curTyp['v'].pop(-1)
            elif ll=='/':
                curTyp['d'].pop(-1)
        curTyp['w'].delete('end-2c')
    elif word=="u":
        curTyp={"w":curTyp['w'], "v":[-1], "s":[0], 'd':[-1], "bo":[-1], "bc":[0]}
        curTyp['w'].delete(1.0,'end')
    elif word=='c':
        clear_output()
        if curTyp['w']==input_display2:
            add_text('s')
        for i in range(2):
            curTyp=next(cycTyp)
            add_text('u')
    elif word=="r":
        clear_output()
        plt.close()
        ppt=graTemplate()
        i2=input_display2.get(1.0,'end-1c')
        gi2=i2.split('=')
        if len(gi2)==1:gi2.append('')
        calculate(input_display1.get(1.0,'end-1c'))
        if plot:
            ppt=graph(ppt)
            plt.legend()
        if gi2[0] and plot:
            r=[results[0][:]]
            calculate(i2)
            if gi2[1] and plot:
                r.append(results[0][:])
                ppt=graph(ppt)
                plt.legend()
                titik_potong(r,ppt)
    elif word=='s':
        f=input_display1.get(1.0,'end-1c')
        g=f.split('=')
        if len(g)==1: g.append('')
        if (g[0] and g[1]) or curTyp['w']==input_display2:
            curTyp['w'].config(highlightthickness=0,bd=3)
            curTyp['w'].config(state=DISABLED)
            cycTyp=cycle([next(cycTyp),curTyp])
            curTyp=next(cycTyp)
            curTyp['w'].config(highlightbackground='red',highlightcolor='red',
                highlightthickness=3,bd=0)
    else:
        add_word = lambda: curTyp['w'].insert('end',word)
        if word in list('/*+=') and ll in '/*+-(':
            pass
        elif word in '-' and ll=='-':
            pass
        elif word=='=' and '=' in text or curTyp['bo']>curTyp['bc']:
            pass
        elif word in list('xy') and (curTyp['v'][-1]>=curTyp['s'][-1] or curTyp['v'][-1]<curTyp['d'][-1]):
            pass
        elif word not in list('xy+=-/*()') and ll in list('xy') and ll!='':
            pass
        elif word=='(' and curTyp['bo'][-1]>curTyp['bc'][-1]:
            pass
        elif word==')' and curTyp['bo'][-1]<curTyp['bc'][-1]:
            pass
        else:
            l=len(text)
            if word in '+=-()':
                if word=='(':
                    curTyp['bo'].append(l)
                elif word==')':
                    curTyp['bc'].append(l)
                curTyp['s'].append(l)
            elif word in 'xy':
                curTyp['v'].append(l)
            elif word=='/':
                curTyp['d'].append(l)
            add_word()
    # print(curTyp)
    curTyp['w'].config(state=DISABLED)

frameRemov = lambda des: des.place_forget()
framePlace = lambda reb: reb.place(anchor='c',relx=.5,rely=.5,height=fh,width=fw)

def change_place(des,reb):
    add_text('c')
    frameRemov(des)
    framePlace(reb)
    reb.focus()

class graTemplate():
    def __init__(self):
        self.fig = plt.figure(figsize=(round(sw/256),round(sw/256)))
        self.ax = self.fig.gca()
        self.ax.grid(visible=True,alpha=.8,which='major',linestyle='-')
        self.ax.grid(visible=True,alpha=.3,which='minor',linestyle='--')
        self.ax.minorticks_on()
        self.ax.axvline(c='0')
        self.ax.axhline(c='0')
        self.ax.set_box_aspect(1)
        self.ax.axis('equal')

def titik_potong(r,ppt):
    global results
    a,b,t_p=r[0][:], r[1][:],[]
    def create_plt():
        ppt.ax.scatter(t_p[0],t_p[1],marker='.',s=220,label=f'TP ({trunc(t_p[0])},{trunc(t_p[1])})')
        outputLine(f'({trunc(t_p[0])},{trunc(t_p[1])})',outputLine.lp())
        plt.legend()
    def f(c,d):
        g=[]
        for i in c[1]:
            if i[2]!='x':
                g.append(i)
            else:
                g.append([i[0],i[1],''])
                g.append('(')
                g.append(d[1][0])
                g.append(')')
        calculate([c[0],g])
        t_p.append(results[0][1][0][1])
        create_plt()
    if a[0][0][2]=='y' and b[0][0][2]=='y':
        calculate([a[1],b[1]])
        t_p.append(results[0][1][0][1])
        if len(a[1])==1 or len(b[1])==1:
            if len(a[1])==1: t_p.append(a[1][0][1])
            elif len(b[1])==1: t_p.append(b[1][0][1])
            create_plt()
        else: f(a,results[0])
    elif a[0][0][2]=='y' and b[0][0][2]=='x':
        t_p.append(b[1][0][1])
        f(a,b)
    elif a[0][0][2]=='x' and b[0][0][2]=='y':
        t_p.append(a[1][0][1])
        f(b,a)

def graph(ppt):
    global plot, results
    a,b=0,0
    if plot[0][0]!=plot[1][0]:
        a=plot[0][1]
        ppt.ax.scatter(0,a,marker='.',s=220,label=f'TP Y (0,{trunc(a)})')
    if plot[0][1]!=plot[1][1]:
        b=trunc(plot[0][1]/(plot[0][1]-plot[1][1]))
        if plot[0][0]==plot[1][0]:
            b=plot[0][0]
        ppt.ax.scatter(b,0,marker='.',s=220,label=f'TP X ({trunc(b)},0)')
    ppt.ax.axline(plot[0],plot[1],c=next(l_colors),label=results[-1])
    f=max(abs(4*(a+b+1)),ppt.ax.get_xlim()[1])
    ppt.ax.set_xlim(f*-1,f)
    ppt.ax.set_ylim(f*-1,f)
    return ppt

class outputLine(Label):
    position=0
    def __init__(self,text,pos):
        Label.__init__(
            self,output_frame,text=text,wraplength=scl(fw*.385,c=3),
            font=("Courier New", scl(14)),bg="white")
        self.grid(column=1,row=pos,pady=5)

    def lp():
        outputLine.position+=1
        return outputLine.position-1

def calculate(equation):
    global tkinputvar, results, plot
    output_frame.grid_propagate(1)
    print("-"*32)
    try:
        results, plot=parser(equation[:])
    except ZeroDivisionError:
        results,plot=["Cannot divide numbers by 0"],[]
    print("-"*32)
    outputLine('-'*32,outputLine.lp())
    for i in range(1,len(results)):
        if results[i]!=' ':
            outputLine(results[i],outputLine.lp())
    outputLine('-'*32,outputLine.lp())
    gcfigure(output_frame,outputLine.position,2)
    root.update()
    output_frame.config(height=output_frame.winfo_height(),width=canvas_out.winfo_width())
    output_frame.grid_propagate(0)
    canvas_out.configure(scrollregion=canvas_out.bbox('all'))
    return equation

def gcfigure(f,r,c):
    f.grid_rowconfigure(0,weight=1)
    f.grid_rowconfigure(r,weight=1)
    f.grid_columnconfigure(0,weight=1)
    f.grid_columnconfigure(c,weight=1)

# Setting window background
bg_image=Image.open(res_path('resources/classroom.jpg')).resize((ww,wh))
bg_image=ImageTk.PhotoImage(bg_image)
bg_Image=Label(root, image=bg_image)
bg_Image.pack()
bg_Image.lower()

class changeButton(Button):
    def __init__(self,master,text,width,orig,end,**kwargs):
        Button.__init__(
            self,master, bd=scl(5), text=text,
            width=scl(width,c=1), font=("Tahoma",scl(12)),
            command=lambda:change_place(orig,end))
        self.conf(kwargs)
    def conf(self,configs):
        for k,v in configs.items():
            try: v=float(scl(v))
            except ValueError: pass
            except TypeError: pass
            if (k=="extra"):
                self.conf(v)
            else: self[k]=v

class pageFrame(Frame):
    def __init__(self,master,color,dx=50,dy=40,**kwargs):
        self.buttons=[]
        Frame.__init__(self,master,bg=color,padx=scl(dx),pady=scl(dy))
        for k,v in kwargs.items():
            try: v=float(scl(v))
            except ValueError: pass
            except TypeError: pass
            self[k]=v
        self.bind('<Tab>', lambda e: "break")

    def redirectBtn(self,red,text='Back Home',width=10,pos=1,**kwargs):
        self.buttons.append(changeButton(self,text,scl(width),self,red))
        last_button=self.buttons[len(self.buttons)-1]
        last_button.grid(column=1,row=pos,padx=scl(5),pady=scl(5))
        last_button.conf(kwargs)

class inputBtn(Button):
    def __init__(self,master,text,value,c):
        Button.__init__(self,master,text=text,fg='#FFF',
            activebackground=c,bg=c,font=('Tahoma',scl(15)),
            activeforeground='#FFF',
            command=lambda: add_text(value))

class lazyLabel(Label):
    def __init__(self,master,text,padx,pady,fg,bg,font,**kwargs):
        Label.__init__(self,master,text=text,padx=scl(padx),
            pady=scl(pady),fg=fg,bg=bg,font=font)
        for k,v in kwargs.items():
            try: v=round(float(scl(v)))
            except ValueError: pass
            except TypeError: pass
            self[k]=v

# frames
home_frame=pageFrame(root, '#468E59')

solver_frame=pageFrame(root, '#642b09')
solver_frame.redirectBtn(home_frame,font=('Tahoma',scl(12)))

short_frame=pageFrame(root,'#00B4D8')
short_frame.redirectBtn(home_frame,font=('Tahoma',scl(12)))

home_frame.redirectBtn(solver_frame,"Simple Solver",35,3)
home_frame.redirectBtn(short_frame,"Help/Shortcuts",35,4)
home_frame.focus()

# home items
    # home title
logo_title=lazyLabel(home_frame, '- SimTeACC -',60,20,'#FFF','#569ABD',
    ('Arial Black',scl(40),'bold'),relief="groove",bd=8,
    width=12)
sub_title=lazyLabel(
    home_frame,"Simple Teacher Assitant CC\nFor Teachers, By Students",25,5,'#656565','#C7C7C7',
    ("Garamond",scl(14),'italic bold'),relief='ridge',bd=3)
    # home object placement
r=1
for x in (logo_title,sub_title):
    x.grid(row=r,column=1,pady=10)
    r+=1
logo_title.grid(pady=(0,10),sticky="news")
sub_title.grid(pady=(0,42.0))
gcfigure(home_frame,5,2)
framePlace(home_frame)




# Shortcuts frame and variables
help_msg=[['0-9, XY, ()+-/*=', "You can now type out any number/variable"],
          ['S',"Shortcut for the ↕ button which is used to switch between equation inputs. You can only switch from the first equation when you have completed it e.g. x+y=10"],
          ['G',"Shortcut for the graph button."],
          ['Enter', "Shortcut for the ANSWER button."],
          ['Backspace', 'Shortcut for the ⌫ button.'],
          ['Ctrl-Backspace', 'Shortcut for the CE button. CE clears only the equation input you are at.'],
          ['Shift-Backspace', 'Shortcut for the C button. C clears everything including the output and other equation inputs.'],
          ['Notice','While this software can be used to do single variable equations and as a calculator, it is mainly made to do 2 variable equations.'],
          ['Notice','If your input happens to be too long and is now pass the bottom border, you can scroll down to continue seeing it.']]
class helpDialogue(Label):
    def __init__(self,text,row,col,lwrap=0,sti='news',**args):
        Label.__init__(self,short_frame,text=text,bg="#ff7d00",padx=5,pady=7,bd=5,relief='ridge',
            font=('Tahoma',scl(12)),wraplength=lwrap,justify='left')
        self.grid(column=col,row=row,sticky=sti,padx=(0,5))
        for k,v in args.items():
            try: v=round(float(scl(v)))
            except ValueError: pass
            except TypeError: pass
            self[k]=v
helpDialogue('Help/Shortcuts',1,2,anchor='c',sti='n',padx=scl(100))
for i in range(len(help_msg)):
    helpDialogue(help_msg[i][0],i+3,1,anchor='c')
    helpDialogue(help_msg[i][-1],i+3,2,scl(750))
gcfigure(short_frame,len(help_msg)+3,3)

# Solver frame and variables
contain_out=pageFrame(solver_frame,"#f2cf9d",0,0,
    height=scl(fh*.61,c=2))
canvas_out=Canvas(contain_out,bg='#f2cf9d',yscrollincrement=4)
scroll_out=Scrollbar(contain_out,command=canvas_out.yview)
output_frame=pageFrame(canvas_out,"#f2cf9d",20,20)
canvas_out.windows_item = canvas_out.create_window((0,0), window=output_frame, anchor='nw')
canvas_out.config(yscrollcommand=scroll_out.set)

canvas_out.bind('<Configure>', lambda e: canvas_out.configure(scrollregion=canvas_out.bbox('all')))

class inpDsp(Text):
    def __init__(self, bg='#f2cf9d'):
        Text.__init__(self, solver_frame, bg=bg, state='disabled',
            font=('Courier New',scl(12)), height=scl(3), relief='sunken',
            width=scl(round(fw*.045),c=3),wrap='char',bd=3,padx=5,pady=5,
            exportselection=False,cursor='left_ptr')
        self.bind('<FocusIn>',lambda _: solver_frame.focus())

input_display1=inpDsp()
input_display2=inpDsp('#FFF')
cycTyp=cycle([{"w":input_display1, "v":[-1], "s":[0], 'd':[-1], "bo":[-1], "bc":[0]},
              {"w":input_display2, "v":[-1], "s":[0], 'd':[-1], "bo":[-1], "bc":[0]}])
curTyp=next(cycTyp)
curTyp['w'].config(highlightbackground='red',highlightcolor='red',
    highlightthickness=3, bd=0)

title_solver=lazyLabel(solver_frame,"See Below for Output",0,0,"#FFF",
    "#865840",("Arial Black",scl(24),"bold"),relief='ridge',bd=5)
graph_button=Button(solver_frame, text="Graph", bd=scl(5),
    font=("Tahoma", scl(13)),width=scl(fw*.05,c=1),
    command=lambda: plt.show(block=False) if plot else "break")

contain_out.grid(row=2,column=2,rowspan=3,padx=scl(15,0),pady=scl(7),sticky='nsew')
contain_out.grid_propagate(0)
contain_out.grid_rowconfigure(0,weight=1)
contain_out.grid_columnconfigure(0,weight=1)
canvas_out.grid(row=0,column=0,sticky='nsew')
scroll_out.grid(row=0,column=1,sticky='ns')
graph_button.grid(row=5,column=2,padx=scl(15,0),pady=7,sticky='news')
input_display1.grid(row=2,column=1,sticky='news',pady=scl(3))
input_display2.grid(row=3,column=1,sticky='news',pady=scl(3))
title_solver.grid(row=1,column=2,padx=scl(15,0),pady=scl(0,7),sticky='ew')

solver_frame.grid_columnconfigure(1,weight=1)
solver_frame.grid_columnconfigure(2,weight=1)
solver_frame.grid_rowconfigure(2,weight=1)
solver_frame.grid_rowconfigure(3,weight=1)
solver_frame.grid_rowconfigure(4,weight=1)
solver_frame.buttons[0].grid(sticky='w')
gcfigure(solver_frame,10,10)


number_contain=pageFrame(solver_frame,solver_frame['bg'],0,0,height=scl(fh*.5,c=2))
number_contain.grid(row=4,column=1,rowspan=2,sticky='news')
number_contain.grid_propagate(0)
for i in range(1,6):
    number_contain.grid_rowconfigure(i,weight=1)
    number_contain.grid_columnconfigure(i,weight=1)
number_contain.grid_columnconfigure(5,weight=0)
number_contain.grid_rowconfigure(6,weight=1)

input_b_d = {
    "1":"1",               "2":"2",                "3":"3",               "+":["+",'#a47e1b'],
    "4":"4",               "5":"5",                "6":"6",               "-":["-",'#a47e1b'],
    "7":"7",               "8":"8",                "9":"9",               "×":["*",'#a47e1b'],
    "X":"x",               "0":"0",                "Y":"y",               "÷":["/",'#a47e1b'],
    "(":["(",'#a47e1b'],   " ↕ ":["s",'#ba7938'],  ")":[")",'#a47e1b'],   "=":["=",'#a47e1b'],
    "CE":["u",'#ba7938'], "C":["c",'#ba7938'],   "⌫ ":["b",'#ba7938'],  "ANS":["r",'#ba7938']
}
input_b_d_values=[x if type(x)!=list else x[0] for x in input_b_d.values()]

input_b=[]
for k,v in input_b_d.items():
    c='#c46404'
    if len(v)>1:
        c,v=v[1],v[0]
    input_b.append(inputBtn(number_contain,k,v,c))

for x in range(len(input_b)):
    input_b[x].grid(row=int(x/4)+1,column=(x%4)+1, padx=scl(5),pady=scl(5),sticky='news')

# frame bindings
for v in input_b_d_values:
    if input_b_d_values.index(v)==20:break
    solver_frame.bind(v,lambda e, v=v: asyncio.run(simulate_click(input_b[input_b_d_values.index(v)])))
solver_frame.bind("<Control-BackSpace>",lambda e: asyncio.run(simulate_click(input_b[input_b_d_values.index('u')])))
solver_frame.bind("<Shift-BackSpace>",lambda e: asyncio.run(simulate_click(input_b[input_b_d_values.index('c')])))
solver_frame.bind("<BackSpace>",lambda e: asyncio.run(simulate_click(input_b[input_b_d_values.index('b')])))
solver_frame.bind("<Return>",lambda e: asyncio.run(simulate_click(input_b[input_b_d_values.index('r')])))
solver_frame.bind("g",lambda e: asyncio.run(simulate_click(graph_button)))
solver_frame.bind("<Escape>", lambda e: asyncio.run(simulate_click(solver_frame.buttons[0])))


home_frame.bind("1",lambda e: asyncio.run(simulate_click(home_frame.buttons[0])))
home_frame.bind("2",lambda e: asyncio.run(simulate_click(home_frame.buttons[1])))

short_frame.bind("<Escape>", lambda e: asyncio.run(simulate_click(short_frame.buttons[0])))

root.mainloop()