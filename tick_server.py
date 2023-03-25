import socket
import threading
import win10toast
from threading import *
from multiprocessing import Queue
from tkinter import *
import time
# clients queue of addresses
q=Queue()
# ui queue of flag (0-working 1-exiting)
qe=Queue()
qe.put("0")
def ui():
    root = Tk()
    root.configure(background="#050505")
    root.geometry("300x250")
    root.title("Server")
    a = StringVar()
    a.set("00")
    text1=Label(root,text="Connected clients:",background="#050505",foreground="#1aff00")
    text1.place(x=0,y=0)
    b = Label(root, textvariable=a,background="#050505",foreground="#1aff00")
    b.place(x=0, y=20)
    def on_close():
        try:
            root.destroy()
        except:print("Error destroying window")
        qe.get()
        qe.put("1")
    def submit():
        k = 0
        while True:
            qs = int(q.qsize())
            am = []
            for i in range(qs):
                am.append(q.get())
            for i in am:
                q.put(i)
            s = ""
            for i in am:
                try:
                    s = s + str(i)+"\n"
                except:pass
            try:
                a.set(s)
            except:pass
            try:
                root.update()
            except:pass
            time.sleep(0.1)

    Thread(target=submit, daemon=True).start()
    root.protocol(name="WM_DELETE_WINDOW",func=on_close)
    root.mainloop()
def threaded_client(c:socket.socket,add):
    qs=int(q.qsize())
    am=[]
    for i in range(qs):
        am.append(q.get())
    print(am)
    for i in am:
        q.put(i)
    while True:
        c.sendall(b"online?")
        try:
            data = c.recv(2048)
        except:
            break
        if data == b"yes":
            pass
        else:break
    return False
def control_client(c:socket.socket,add):
    a=threaded_client(c,add)
    if a==False:
        qs = int(q.qsize())
        am = []
        for i in range(qs):
            am.append(q.get())
        for i in range(len(am)):
            try:
                if am[i] == str(add[0]) + ":" + str(add[1]):
                    am.pop(i)
            except:break
        for i in am:
            q.put(i)
        try:
            t=win10toast.ToastNotifier()
            t.show_toast("Tick Server","Client disconnect",duration=2,threaded=True)
        except:pass
def loop():
    while True:
        con, add = s.accept()
        print("Client accepted")
        q.put(str(add[0]) + ":" + str(add[1]))
        time.sleep(0.01)
        Thread(target=control_client, args=(con, add,), daemon=True).start()
# selecting host and port
host_select=int(input("SELECT HOST(1.localhost or 2.local_ip)"))
if host_select==1:
    host="127.0.0.1"
if host_select==2:
    host=socket.gethostbyname(socket.gethostname())
else:exit(2)
port=int(input("PORT:"))
print("Server address "+host+":"+str(port))
# binding server
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host,port))

except OSError as e:
    print("Error:"+str(e))
    if str(e)=="[WinError 10048] Обычно разрешается только одно использование адреса сокета (протокол/сетевой адрес/порт)":
        print("This port is busy\nPlease select other port\nclosing...")
        exit(1)
s.listen(50)
# starting ui
Thread(target=ui,args=(),daemon=True).start()
print("Server started")
# starting loop
Thread(target=loop, daemon=True).start()
while True:
    a=qe.get()
    qe.put(a)
    if a=="1":
        print("closing...")
        qe.put("1")
        exit(0)
    try:
        time.sleep(0.1)
    except:pass


