import multiprocessing
import json
import socket
import select
import pyodbc
UserOnline = []
UserInSistem = {}
def Base():
    connectionString = (r'Driver={SQL Server};Server=DESKTOP-RVA44I5\MSSQLSERVERS;Database=test;Trusted_Connection=yes')
    connection = pyodbc.connect(connectionString)
    dbCursor = connection.cursor()
    return dbCursor, connection

def LogIn(data,dbCursor, connection):
    print('L')
    requestString = """ select ID, Name, Fname from Users where Login = ? AND Password = ?"""
    dbCursor.execute(requestString, (data.get('b'), data.get('c')))
    #print(dbCursor)
    i = 0
    for row in dbCursor.fetchall():
        i+=1
        print(row[0], row[1], row[2])
    if i == 0:
        return None
    return row[0], row[1], row[2]


def RegInBase(data, dbCursor, connection):
    try:
        requestString = """INSERT INTO Users (Name,Fname,Login,Password) VALUES
        (?,?,?,?)
        """
        dbCursor.execute(requestString, (data.get('b'), data.get('c'), data.get('d'), data.get('e')))
        #print(dbCursor)
        connection.commit()


        return True
    except pyodbc.IntegrityError:
        return False
def listen_for_client(cs):
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
        #     client_sockets.remove(cs)
        # else:
            # if we received a message, replace the <SEP>
            # token with ": " for nice printing
            #msg = msg.replace(separator_token, ": ")
        # iterate over all connected sockets
        # for client_socket in client_sockets:
        #     # and send the message
        #     client_socket.send(msg.encode())
def Handler(sock):
   # print(sock)
    dbCursor, connection = Base()
    requestString = """ select ID, Name,Fname from Users"""
    dbCursor.execute(requestString)
    for row in dbCursor.fetchall():
        #UserInSistem[str(row[1] + ' '+ row[2])] = row[0]
        UserInSistem[row[0]] = [row[1],row[2]]
    print(UserInSistem)
    try:
        data = sock.recv(1024)  # Should be ready
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        return False
    if not data:
        print("Disconnected by")
        return False
    #print(data.decode())
    #print(data, '\n')
    data = json.loads(data.decode())

    if data.get('a') == '<-Запрос на регистрацию->':
        if RegInBase(data, dbCursor, connection):
            answer = json.dumps({'a': '<-Запрос на регистрацию->', 'b': 'Пользователь зарегестрирован'})
            sock.sendall(answer.encode())

        else:
            answer = json.dumps({'a': '<-Запрос на регистрацию->', 'b': 'Пользователь с таким логином уже зарегестрирован'})
            sock.sendall(answer.encode())


    elif data.get('a') == '<-Запрос на вход->':
        id,name,fname = LogIn(data, dbCursor, connection)
        if id:

            for i in UserInSistem:
                if i == id:
                    d = i
            UserInSistem.pop(d)
            answer = json.dumps({'a': '<-Запрос на вход->', 'b': 'Пользователь залогинен', 'c': name, 'd': fname, 'e': UserInSistem})
            print(answer)
            sock.sendall(answer.encode())
            UserOnline.append(id)

        else:
            answer = json.dumps({'a': '<-Запрос на вход->', 'b': 'В базе нет такого пользователя'})
            sock.sendall(answer.encode())
        print(UserOnline)
    # elif data.get('a') == '<-Готов общаться->':
    #     listen_for_client(sock,data.get('b'))

    #elif data.get('a') == '<-Отправить сообщение>':






def main():
    host = socket.gethostname()
    port = 8008
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server = ('localhost', 8088)
        sock = socket.socket()
        sock.bind(server)

        print('Start Server')
        sock.listen(5)
        sock.setblocking(False)

        inputs = [sock]
        outputs = []
        while True:
            # вызов `select.select` который проверяет сокеты в
            # списках: `inputs`, `outputs` и по готовности, хотя бы
            # одного - возвращает списки: `reads`, `send`, `excepts`
            reads, send, excepts = select.select(inputs, outputs, inputs)
            print(reads)
            for conn in reads:
                if conn == sock:
                    new_conn, client_addr = conn.accept()
                    print('SinIn_OK ', client_addr)
                    # new_conn.setblocking(False)
                    inputs.append(new_conn)
                else:
                    # addr = sock.getpeername()
                    if not Handler(conn):
                        inputs.remove(conn)
                        if conn in outputs:
                            outputs.remove(conn)
                        conn.close()

                    # pid = os.fork()
                    # if pid:
                    #     pass
                    # else:
                    #     Handler(conn)


main()





