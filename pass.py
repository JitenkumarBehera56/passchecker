
import tkinter as tk
from tkinter import ttk
import hashlib, base64, random, string

root=tk.Tk()
root.title("PASS CHECKER PRO")
root.geometry("700x550")
root.configure(bg="black")
root.resizable(False,False)

password=tk.StringVar()
SPECIAL="!@#$%^&*()"

def strength(p):
    score=0
    if len(p)>=8: score+=1
    if len(p)>=12: score+=1
    if any(c.isupper() for c in p): score+=1
    if any(c.islower() for c in p): score+=1
    if any(c.isdigit() for c in p): score+=1
    if any(c in SPECIAL for c in p): score+=1
    return score

def crack_time(s):
    return ["Instant","Instant","Few Minutes","Few Days","Hundreds of Years","Millions of Years","Millions of Years"][min(s,6)]

def validate_password(p):
    errs=[]
    if len(p)<8: errs.append("Min 8 chars")
    if not any(c.isupper() for c in p): errs.append("Need Uppercase")
    if not any(c.islower() for c in p): errs.append("Need Lowercase")
    if not any(c.isdigit() for c in p): errs.append("Need Number")
    if not any(c in SPECIAL for c in p): errs.append("Need Special")
    return errs

def check():
    p=password.get()
    errs=validate_password(p)
    s=strength(p)
    length_lbl.config(text=f"Length : {len(p)}")
    if errs:
        st,color,val="Weak","red",20
        crack_lbl.config(text="Rules: "+" | ".join(errs),fg="red")
    else:
        crack_lbl.config(text=f"Crack Time : {crack_time(s)}",fg="cyan")
        if s<=3: st,color,val="Weak","red",30
        elif s<=5: st,color,val="Medium","yellow",65
        else: st,color,val="Strong","lime",100
    strength_lbl.config(text=f"Strength : {st}",fg=color)
    bar["value"]=val
    sha_txt.delete("1.0",tk.END); sha_txt.insert(tk.END,hashlib.sha256(p.encode()).hexdigest())
    b64_txt.delete("1.0",tk.END); b64_txt.insert(tk.END,base64.b64encode(p.encode()).decode())

def generate():
    chars=string.ascii_letters+string.digits+SPECIAL
    lst=[random.choice(string.ascii_uppercase),random.choice(string.ascii_lowercase),random.choice(string.digits),random.choice(SPECIAL)]
    lst += [random.choice(chars) for _ in range(10)]
    random.shuffle(lst)
    password.set("".join(lst))
    check()

def copy():
    root.clipboard_clear(); root.clipboard_append(password.get())

def clear():
    password.set(""); bar["value"]=0
    strength_lbl.config(text="Strength : -",fg="white")
    length_lbl.config(text="Length : -")
    crack_lbl.config(text="Crack Time : -",fg="cyan")
    sha_txt.delete("1.0",tk.END); b64_txt.delete("1.0",tk.END)

def toggle():
    if entry.cget("show")=="*":
        entry.config(show=""); eye.config(text="Hide")
    else:
        entry.config(show="*"); eye.config(text="Show")

tk.Label(root,text="PASS CHECKER PRO",bg="black",fg="lime",font=("Consolas",22,"bold")).pack(pady=10)
frame=tk.Frame(root,bg="black"); frame.pack()
entry=tk.Entry(frame,textvariable=password,width=35,font=("Consolas",14),bg="#111",fg="lime",insertbackground="lime",show="*")
entry.grid(row=0,column=0,padx=5)
eye=tk.Button(frame,text="Show",command=toggle,bg="#222",fg="lime"); eye.grid(row=0,column=1)
btn=tk.Frame(root,bg="black"); btn.pack(pady=10)
for t,c in [("CHECK",check),("GENERATE",generate),("COPY",copy),("CLEAR",clear)]:
    tk.Button(btn,text=t,command=c,bg="#111",fg="lime",width=12,font=("Consolas",10,"bold")).pack(side=tk.LEFT,padx=5)
style=ttk.Style(); style.theme_use("default"); style.configure("green.Horizontal.TProgressbar",troughcolor="black",background="lime")
bar=ttk.Progressbar(root,length=500,style="green.Horizontal.TProgressbar"); bar.pack(pady=10)
strength_lbl=tk.Label(root,text="Strength : -",bg="black",fg="white"); strength_lbl.pack()
length_lbl=tk.Label(root,text="Length : -",bg="black",fg="lime"); length_lbl.pack()
crack_lbl=tk.Label(root,text="Crack Time : -",bg="black",fg="cyan"); crack_lbl.pack()
tk.Label(root,text="SHA256",bg="black",fg="orange").pack()
sha_txt=tk.Text(root,height=4,width=75,bg="#111",fg="lime"); sha_txt.pack()
tk.Label(root,text="Base64",bg="black",fg="orange").pack()
b64_txt=tk.Text(root,height=2,width=75,bg="#111",fg="lime"); b64_txt.pack()
tk.Label(root,text=">>> Cyber Security Tool <<<",bg="black",fg="green").pack(pady=8)
root.mainloop()
