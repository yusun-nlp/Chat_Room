import socket
import threading
import queue
import json
import time
import sys

IP = '127.0.0.1'
PORT = 50001
online_users = []  # 在线用户列表, (conn, send_user, addr)
lock = threading.Lock()  # 创建锁, 防止多个线程在写入信息的时候顺序变乱
mes_q = queue.Queue()  # 存放客户端发来的消息


def get_users():
    users = []
    for i in range(len(online_users)):
        users.append(online_users[i][1])
    return users


class ChatServer(threading.Thread):
    """重写聊天消息线程类，继承threading.Thread"""
    global online_users, mes_q, lock

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.ADDR = ('127.0.0.1', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 将接收到的消息放入消息队列mes_q
    def get_mes(self, message, addr):
        lock.acquire()
        try:
            mes_q.put((addr, message))
        finally:
            lock.release()

    def del_user(self, conn, addr):
        item = 0
        for i in online_users:
            if i[0] == conn:
                online_users.pop(item)
                print(' Remaining online users: ', end='')  # 打印剩余在线用户(conn)
                u = get_users()
                self.get_mes(u, addr)
                print(u)
                break
            item += 1

    # 将消息队列中的所有消息发送给所有在线用户
    def sendMessage(self):
        while True:
            if not mes_q.empty():
                mes_send = ''
                message = mes_q.get()  # 取出消息队列的第一个元素
                if isinstance(message[1], str):  # 判断message[1]是否为str类型
                    for i in range(len(online_users)):
                        for j in range(len(online_users)):
                            # 在所有在线用户列表中寻找当前消息的接受者
                            if message[0] == online_users[j][2]:
                                print('消息来自用户[{}]'.format(j))
                                mes_send = ' ' + online_users[j][1] + ': ' + message[1]
                                break
                        print(online_users[i][0])
                        print(mes_send)
                        online_users[i][0].send(mes_send.encode('utf-8'))
                if isinstance(message[1], list):
                    print(message[1])
                    mes_send = json.dumps(message[1])
                    # print('list:', mes_send)
                    for i in range(len(online_users)):
                        try:
                            online_users[i][0].send(mes_send.encode('utf-8'))
                        except:
                            pass

    # 接收所有客户端发来的消息
    def recieveMessage(self, conn, addr):
        send_user = ''
        send_user = conn.recv(1024)
        send_user = send_user.decode('utf-8')
        for i in range(len(online_users)):
            if send_user == online_users[i][1]:
                print('用户已经存在')
                send_user = '' + send_user + '_2'
        if send_user != '':
            if send_user == 'no':
                send_user = addr[0] + ':' + str(addr[1])
            online_users.append((conn, send_user, addr))
            print('建立聊天连接：', addr, ': ', send_user, end='')
            u = get_users()
            print('\n', u)
            self.get_mes(u, addr)
            try:
                while True:
                    message = conn.recv(1024)
                    message = message.decode('utf-8')
                    print(message)
                    self.get_mes(message, addr)  # 保存信息到队列
                conn.close()
            except:
                print(send_user + ' Connection lose')
                self.del_user(conn, addr)  # 将断开用户移出users
                conn.close()

    def run(self):  # 启动线程
        self.s.bind(self.ADDR)
        self.s.listen(5)
        print('正在运行Chat Server的线程')
        t = threading.Thread(target=self.sendMessage)
        t.start()
        while True:
            conn, addr = self.s.accept()
            print('conn=', conn, 'addr=', addr)
            t1 = threading.Thread(target=self.recieveMessage, args=(conn, addr))
            t1.start()
        self.s.close()


class PhotoServer(threading.Thread):
    """重写聊天图片线程类，继承threading.Thread"""

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.ADDR = ('127.0.0.1', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.photo = '.\\server_photo_cache\\'

    # 将缓存中的图片发送给客户端
    def sendPhoto(self, picture, conn):
        print(picture)
        pic_name = picture.split()[1]
        pic_path = self.photo + pic_name
        print('开始发送图片')
        file = open(pic_path, 'rb')
        while True:
            pic = file.read(1024)
            if not pic:
                break
            conn.send(pic)
        time.sleep(1)  # 延时
        conn.send('EOF'.encode('utf-8'))
        print('图片发送成功')

    # 将上传的图片存放在缓冲中
    def recvPhoto(self, picture, conn):
        print(picture)
        pic_name = picture.split()[1]
        pic_path = self.photo + pic_name
        print('开始上传图片')
        file = open(pic_path, 'wb+')
        while True:
            pic = conn.recv(1024)
            if pic == 'EOF'.encode('utf-8'):
                print('图片上传成功')
                break
            print(file, ': ', pic)
            file.write(pic)
            file.flush()
        file.close()

    # 处理图片
    def recievePhoto(self, conn, addr):
        while True:
            picture = conn.recv(1024)
            picture = picture.decode('utf-8')
            print('从{0}接收照片：{1}'.format(addr, picture))
            if picture == 'quit':
                break
            action = picture.split()[0]  # 判断是接收还是发送
            if action == 'get':
                self.sendPhoto(picture, conn)
            elif action == 'put':
                self.recvPhoto(picture, conn)
        conn.close()
        print('---')

    def run(self):  # 启动线程
        self.s.bind(self.ADDR)
        self.s.listen(5)
        print('正在运行Photo Server的线程')
        while True:
            conn, addr = self.s.accept()
            print('conn=', conn, 'addr=', addr)
            t2 = threading.Thread(target=self.recievePhoto, args=(conn, addr))
            t2.start()
        self.s.close()


class FileServer(threading.Thread):
    """重写聊天文件线程类，继承threading.Thread"""

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.ADDR = ('127.0.0.1', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file = '.\\server_file_cache\\'

    # 将缓存中的文件发送给客户端
    def sendFile(self, file_n, conn):
        print(file_n)
        file_name = file_n.split()[1]
        file_path = self.file + file_name
        print('开始发送文件')
        file = open(file_path, 'rb')
        while True:
            f_content = file.read(1024)
            if not f_content:
                break
            conn.send(f_content)
        time.sleep(5)  # 延时
        conn.send('EOF'.encode('utf-8'))
        print('文件发送成功')

    # 将上传的文件存放在缓冲中
    def recvFile(self, file_n, conn):
        print(file_n)
        file_name = file_n.split()[1]
        file_path = self.file + file_name
        print('开始上传文件')
        file = open(file_path, 'wb+')
        while True:
            f_content = conn.recv(1024)
            if f_content == 'EOF'.encode('utf-8'):
                print('文件上传成功')
                break
            print(file, ': ', f_content)
            file.write(f_content)
            file.flush()
        file.close()

    # 处理文件
    def recieveFile(self, conn, addr):
        while True:
            file_n = conn.recv(1024)
            file_n = file_n.decode('utf-8')
            print('从{0}接收文件：{1}'.format(addr, file_n))
            if file_n == 'quit':
                break
            action = file_n.split()[0]  # 判断是接收还是发送
            if action == 'get':
                self.sendFile(file_n, conn)
            elif action == 'put':
                self.recvFile(file_n, conn)
        conn.close()
        print('---')

    def run(self):  # 启动线程
        self.s.bind(self.ADDR)
        self.s.listen(5)
        print('正在运行File Server的线程')
        while True:
            conn, addr = self.s.accept()
            print('conn=', conn, 'addr=', addr)
            t3 = threading.Thread(target=self.recieveFile, args=(conn, addr))
            t3.start()
        self.s.close()


if __name__ == '__main__':
    chat_server = ChatServer(PORT)
    chat_server.start()
    photo_server = PhotoServer(PORT + 1)
    photo_server.start()
    file_server = FileServer(PORT + 2)
    file_server.start()
    while True:
        time.sleep(1)
        if not chat_server.isAlive():
            print("Chat Server线程不存在")
            sys.exit(0)
        if not photo_server.isAlive():
            print("Photo Server线程不存在")
            sys.exit(0)
        if not file_server.isAlive():
            print("File Server线程不存在")
            sys.exit()
