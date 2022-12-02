import os
import socket
from threading import Thread

#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)





def connect(sock, addres):
    host = socket.gethostname()
    port = 5000
    server = (host, port)
    sock = socket.socket()
    sock.bind(server)

    print('Start Server')
    sock.listen(2)
    while True:
        conn, addres = sock.accept()
        Form = []
        print(conn, addres[0], addres[1])
        pid  = os.fork()
        if pid:
            while True:
                data = conn.recv(1024).decode()
                if data:
                    Form = (str(data).split(' '))
                    print(Form)
                    conn.send((' успешно создал(-а) аккаунт').encode())
        else:
            connect(sock, addres)
            exit()




    #conn.close()

connect()

# while 1 :
#     #conn, addres = sock.recvfrom(1024)
#     # conn , addres = sock.accept()
#     # print (conn,addres[0], addres[1])
#     while True:
#
#         data = conn.recv(1024).decode('utf-8')
#         print(data)
