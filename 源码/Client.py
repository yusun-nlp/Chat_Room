import socket
import threading
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import json
import os

IP = ''
PORT = ''
user_name = ''  # 当前用户
users = {'Julia': ['sunyu', '127.0.0.1:50001'], 'Meggie': ['maiji', '127.0.0.1:50001']}  # 用户列表
chat = '-------Group chat--------'  # 聊天对象, 默认为群聊

# 登录界面
root1 = tkinter.Tk()
root1.title('用户登录')
p = Image.open('icon.png')
icon = ImageTk.PhotoImage(p)
root1.tk.call('wm', 'iconphoto', root1._w, icon)
root1['height'] = 170
root1['width'] = 300

root1.resizable(0, 0)  # 限制窗口大小

# 用户名
label1 = tkinter.Label(root1, text='用户名:')
label1.place(x=20, y=30, width=100, height=20)
entry1 = tkinter.Entry(root1, width=80)
entry1.place(x=120, y=30, width=130, height=20)
# 密码
label2 = tkinter.Label(root1, text='密码:')
label2.place(x=30, y=60, width=80, height=20)
entry2 = tkinter.Entry(root1, width=80)
entry2.place(x=120, y=60, width=130, height=20)
entry2['show'] = '*'


# 登录按钮
def login(*args):
    global IP, PORT, user_name
    user_name = entry1.get()
    password = entry2.get()
    if user_name in users:
        if users[user_name][0] == password:
            IP, PORT = users[user_name][1].split(':')
            PORT = int(PORT)
            root1.destroy()
        else:
            tkinter.messagebox.showerror('密码错误', message='密码错误！\n请检查你的密码输入')
    else:
        tkinter.messagebox.showerror('用户名错误', message='用户名不存在！\n请检查你的用户名输入，或者点击注册进行用户创建')


def signin():
    def forsignin(*args):
        new_user = entry_1.get()
        new_pass = entry_2.get()
        new_pass_con = entry_3.get()
        if new_user in users:
            tkinter.messagebox.showerror('注册失败', message='用户名已存在！\n请重新输入用户名或直接返回页面登录')
        elif new_pass != new_pass_con:
            tkinter.messagebox.showerror('注册失败', message='两次密码输入不一致！\n请检查你的密码输入')
        else:
            users[new_user] = [new_pass, '127.0.0.1:50001']
            tkinter.messagebox.showinfo('注册成功', message='注册成功！\n请在登录界面重新登录')
            root2.destroy()

    global users
    # 注册界面
    root2 = tkinter.Tk()
    root2.title('用户注册')
    root2['height'] = 200
    root2['width'] = 300
    root2.resizable(0, 0)  # 限制窗口大小

    # 用户名
    label_1 = tkinter.Label(root2, text='用户名')
    label_1.place(x=20, y=30, width=100, height=20)
    entry_1 = tkinter.Entry(root2, width=80)
    entry_1.place(x=120, y=30, width=130, height=20)
    # 密码
    label_2 = tkinter.Label(root2, text='密码')
    label_2.place(x=30, y=60, width=80, height=20)
    entry_2 = tkinter.Entry(root2, width=80)
    entry_2.place(x=120, y=60, width=130, height=20)
    entry_2['show'] = '*'
    # 确认密码
    label_3 = tkinter.Label(root2, text='密码确认')
    label_3.place(x=30, y=90, width=80, height=20)
    entry_3 = tkinter.Entry(root2, width=80)
    entry_3.place(x=120, y=90, width=130, height=20)
    entry_3['show'] = '*'

    root2.bind('<Return>', forsignin)  # 回车绑定登录功能
    but = tkinter.Button(root2, text='注册', command=forsignin)
    but.place(x=110, y=140, width=60, height=25)

    root2.mainloop()


root1.bind('<Return>', login)  # 回车绑定登录功能
loginbut = tkinter.Button(root1, text='登录', command=login)
loginbut.place(x=70, y=110, width=60, height=25)
signinbut = tkinter.Button(root1, text='注册', command=signin)
signinbut.place(x=160, y=110, width=60, height=25)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
if user_name:
    s.sendall(user_name.encode('utf-8'))  # 发送用户名
else:
    s.sendall('no'.encode('utf-8'))  # 没有输入用户名则标记no

# 如果没有用户名则将ip和端口号设置为用户名
addr = s.getsockname()  # 获取客户端ip和端口号
addr = addr[0] + ':' + str(addr[1])
if user_name == '':
    user_name = addr

# 聊天界面
root = tkinter.Tk()
root.title(user_name)  # 窗口命名为用户名
root['height'] = 500
root['width'] = 680
root.resizable(0, 0)  # 限制窗口大小
p = Image.open('icon.png')
icon = ImageTk.PhotoImage(p)
root.tk.call('wm', 'iconphoto', root._w, icon)

# 创建文本输入框
text_v = tkinter.StringVar()
text_v.set('')
textbox = tkinter.Text(root, font=('微软雅黑', 10))
textbox.place(x=190, y=330, width=480, height=155)


# 发送
def send(*args):
    onlinde_users.append('-------Group chat--------')
    print(chat)
    if chat not in onlinde_users:
        tkinter.messagebox.showerror('发送错误', message=chat + '不在线或不存在')
    if chat == user_name:
        tkinter.messagebox.showerror('发送错误', message='不能发送消息给自己！')
        return
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    mes = ' (' + date + ') ' + textbox.get('0.0', 'end') + ':;' + user_name + ':;' + chat  # 添加聊天对象标记
    # print(mes)
    s.sendall(mes.encode('utf-8'))
    textbox.delete('0.0', 'end')  # 发送后清空文本框


# 创建发送按钮
text = tkinter.Button(root, text='发送', command=send, bd=0)
text.place(x=590, y=450, width=50, height=25)
root.bind('<Return>', send)

# 在线用户查看框
onlinde_users = []
# 创建多行文本框, 显示在线用户
userlist = tkinter.Listbox(root, font=('微软雅黑', 12))
userlist.place(x=5, y=5, width=180, height=485)


# 私聊功能
def private(*args):
    global chat
    online_indexs = userlist.curselection()  # 选择进行私聊的对象的索引
    online_index = online_indexs[0]
    if online_index > 0:
        chat = userlist.get(online_index)
        if chat == '-------Group chat--------':
            root.title(user_name)
            return
        pri_title = user_name + '->' + chat
        root.title(pri_title)


userlist.bind('<ButtonRelease-1>', private)

# 信息显示框
mesbox = ScrolledText(root, font=('微软雅黑', 11))
mesbox.place(x=190, y=5, width=480, height=320)
mesbox.tag_configure('blue', foreground='blue')
mesbox.tag_configure('green', foreground='green')
mesbox.tag_configure('red', foreground='red')
mesbox.tag_configure('grey', foreground='grey')
mesbox.tag_configure('pink', foreground='pink')
mesbox.insert(tkinter.END, '欢迎使用FISH聊天室！\n', 'blue')
mesbox.insert(tkinter.END, '----------------------------------------------------------------------------')

# 菜单功能
mflag = 0
photo_l = ''
file_l = ''
offline = ''


def see_photo():
    photo_l.destroy()
    file_l.destroy()
    offline.destroy()
    # p_path = 'F:/大三上/计算机网络/PJ/Chat_Room/client_photo_cache/'
    # os.system("start explorer %s" % p_path)
    p_path = r'F:\大三上\计算机网络\PJ\Chat_Room\client_photo_cache'
    os.system("explorer.exe %s" % p_path)


def see_file():
    photo_l.destroy()
    file_l.destroy()
    offline.destroy()
    f_path = r'F:\大三上\计算机网络\PJ\Chat_Room\client_file_cache'
    os.system("explorer.exe %s" % f_path)


def user_exit():
    photo_l.destroy()
    file_l.destroy()
    offline.destroy()
    root.destroy()
    s.close()


def detail_menu():
    global mflag, photo_l, file_l, offline
    if mflag == 0:
        photo_l = tkinter.Button(root, command=see_photo, text='查看本地图片', bd=0)
        photo_l.place(x=0, y=360, width=90, height=30)
        file_l = tkinter.Button(root, command=see_file, text='查看本地文件', bd=0)
        file_l.place(x=0, y=390, width=90, height=30)
        offline = tkinter.Button(root, text='退出', command=user_exit, bd=0)
        offline.place(x=0, y=420, width=90, height=30)
    else:
        photo_l.destroy()
        file_l.destroy()
        offline.destroy()
        mflag = 0


# 菜单按钮
m_p = tkinter.PhotoImage(file='./icon/menu.png')
menu = tkinter.Button(root, image=m_p, command=detail_menu, bd=0)
menu.place(x=5, y=450, width=40, height=40)

# 表情按钮
# 定义7个表情，使用全局变量, 方便创建和销毁
e1 = ''
e2 = ''
e3 = ''
e4 = ''
e5 = ''
e6 = ''
e7 = ''
# 将图片打开存入变量中
p1 = tkinter.PhotoImage(file='./emoji/愉快.png')
p2 = tkinter.PhotoImage(file='./emoji/可爱.png')
p3 = tkinter.PhotoImage(file='./emoji/爱你.png')
p4 = tkinter.PhotoImage(file='./emoji/笑哭.png')
p5 = tkinter.PhotoImage(file='./emoji/大哭.png')
p6 = tkinter.PhotoImage(file='./emoji/流汗.png')
p7 = tkinter.PhotoImage(file='./emoji/难受.png')
# 用字典将标记与表情图片一一对应, 用于后面接收标记判断表情贴图
dic = {'aa**': p1, 'bb**': p2, 'cc**': p3, 'dd**': p4, 'ee**': p5, 'ff**': p6, 'gg**': p7}
eflag = 0  # 判断表情面板开关的标志


def mark(exp):  # 参数是发的表情图标记, 发送后将按钮销毁
    global eflag
    mes = exp + ':;' + user_name + ':;' + chat
    s.sendall(mes.encode('utf-8'))
    e1.destroy()
    e2.destroy()
    e3.destroy()
    e4.destroy()
    e5.destroy()
    e6.destroy()
    e7.destroy()
    eflag = 0


def e_1():
    mark('aa**')


def e_2():
    mark('bb**')


def e_3():
    mark('cc**')


def e_4():
    mark('dd**')


def e_5():
    mark('ee**')


def e_6():
    mark('ff**')


def e_7():
    mark('gg**')


def rollout():
    global e1, e2, e3, e4, e5, e6, e7, eflag
    if eflag == 0:
        eflag = 1
        e1 = tkinter.Button(root, command=e_1, image=p1, relief=tkinter.FLAT, bd=0)
        e1.place(x=148, y=225)
        e2 = tkinter.Button(root, command=e_2, image=p2, relief=tkinter.FLAT, bd=0)
        e2.place(x=183, y=225)
        e3 = tkinter.Button(root, command=e_3, image=p3, relief=tkinter.FLAT, bd=0)
        e3.place(x=218, y=225)
        e4 = tkinter.Button(root, command=e_4, image=p4, relief=tkinter.FLAT, bd=0)
        e4.place(x=253, y=225)
        e5 = tkinter.Button(root, command=e_5, image=p5, relief=tkinter.FLAT, bd=0)
        e5.place(x=148, y=260)
        e6 = tkinter.Button(root, command=e_6, image=p6, relief=tkinter.FLAT, bd=0)
        e6.place(x=183, y=260)
        e7 = tkinter.Button(root, command=e_7, image=p7, relief=tkinter.FLAT, bd=0)
        e7.place(x=218, y=260)
    else:
        e1.destroy()
        e2.destroy()
        e3.destroy()
        e4.destroy()
        e5.destroy()
        e6.destroy()
        e7.destroy()
        eflag = 0


# 创建表情按钮
e_p = tkinter.PhotoImage(file='./icon/emoji.png')
emoji = tkinter.Button(root, image=e_p, command=rollout, bd=0)
emoji.place(x=200, y=295, width=30, height=30)


# 发送图片按钮
# 将图片上传到图片服务端的缓存文件夹中
def sendPhoto(fileName):
    PORT1 = 50002  # 图片服务器端口号
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((IP, PORT1))
    print(s1, ': ', fileName)
    picture = fileName.split('/')[-1]
    print(picture)
    message = 'put ' + picture
    s1.sendall(message.encode('utf-8'))
    time.sleep(0.1)
    print('正在上传图片')
    with open(fileName, 'rb') as f:
        while True:
            a = f.read(1024)
            print(a)
            if not a:
                break
            s1.sendall(a)
        time.sleep(3)  # 延时确保文件发送完整
        s1.sendall('EOF'.encode('utf-8'))
        print('图片上传成功')
    s1.sendall('quit'.encode('utf-8'))
    time.sleep(1)
    # 上传成功后发信息给所有的客户端
    mes = '``#' + picture + ':;' + user_name + ':;' + chat
    s.sendall(mes.encode('utf-8'))


def picture():
    fileName = tkinter.filedialog.askopenfilename(title='请选择一张图片')
    if fileName:
        sendPhoto(fileName)


# 创建图片按钮
i_p = tkinter.PhotoImage(file='./icon/photo.png')
photo = tkinter.Button(root, image=i_p, command=picture, bd=0)
photo.place(x=235, y=295, width=30, height=30)


# 发送文件
def sendFile(fileName):
    PORT2 = 50003
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((IP, PORT2))
    print(s2, ': ', fileName)
    file_n = fileName.split('/')[-1]
    print(file_n)
    message = 'put ' + file_n
    s2.sendall(message.encode('utf-8'))
    time.sleep(0.1)
    print('正在上传文件')
    with open(fileName, 'rb') as f:
        while True:
            a = f.read(1024)
            print(a)
            if not a:
                break
            s2.sendall(a)
        time.sleep(5)  # 延时确保文件发送完整
        s2.sendall('EOF'.encode('utf-8'))
        print('文件上传成功')
    s2.sendall('quit'.encode('utf-8'))
    time.sleep(1)
    # 上传成功后发信息给所有的客户端
    mes = '++#' + file_n + ':;' + user_name + ':;' + chat
    s.sendall(mes.encode('utf-8'))


def forFile():
    fileName = tkinter.filedialog.askopenfilename(title='请选择一个文件')
    if fileName:
        sendFile(fileName)


# 创建文件按钮
f_p = tkinter.PhotoImage(file='./icon/file.png')
file = tkinter.Button(root, image=f_p, command=forFile, bd=0)
file.place(x=270, y=295, width=30, height=30)


# # 创建截屏按钮
# s_p = tkinter.PhotoImage(file='screencut.png')
# screencut = tkinter.Button(root, image=s_p, command=rollout, bd=0)
# screencut.place(x=305, y=295, width=30, height=30)


# 接收服务端发送的信息
# 接收图片
def recievePhoto(fileName):
    PORT1 = 50002
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((IP, PORT1))
    message = 'get ' + fileName
    s1.sendall(message.encode('utf-8'))
    fileName = './client_photo_cache/' + fileName
    print('正在下载图片')
    with open(fileName, 'wb') as f:
        while True:
            pic = s1.recv(1024)
            if pic == 'EOF'.encode('utf-8'):
                print('下载成功！')
                break
            f.write(pic)
    time.sleep(1)
    s1.sendall('quit'.encode('utf-8'))


# 接收文件
def recieveFile(fileName):
    PORT2 = 50003
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((IP, PORT2))
    message = 'get ' + fileName
    s2.sendall(message.encode('utf-8'))
    fileName = './client_file_cache/' + fileName
    print('正在下载文件到缓存')
    with open(fileName, 'wb') as f:
        while True:
            pic = s2.recv(1024)
            if pic == 'EOF'.encode('utf-8'):
                print('下载成功！')
                break
            f.write(pic)
    time.sleep(10)
    s2.sendall('quit'.encode('utf-8'))


# 接收消息的函数
def recv():
    global onlinde_users
    print(s)
    while True:
        message = s.recv(1024).decode('utf-8')
        print('待处理消息：' + message)
        # 如果没有异常，则收到的是在线用户列表；否则，收到的是信息
        try:
            message = json.loads(message)
            onlinde_users = message
            userlist.delete(0, tkinter.END)  # 清空用户列表
            user_num = ('在线用户个数：' + str(len(message)))
            userlist.insert(tkinter.END, user_num)
            userlist.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
            userlist.insert(tkinter.END, '-------Group chat--------')
            for i in range(len(message)):
                if message[i] == user_name:
                    userlist.insert(tkinter.END, (message[i]))
                    userlist.itemconfig(tkinter.END, fg='grey')
                else:
                    userlist.insert(tkinter.END, (message[i]))
                    userlist.itemconfig(tkinter.END, fg='green')
        except:
            message = message.split(':;')
            message1 = message[0].strip()  # 消息
            print(message1)
            message2 = message[1]  # 发送消息的用户
            message3 = message[2]  # 聊天对象
            t_text = message1.split(': ')[1]
            print(t_text)
            if_photo = t_text.split('#')  # 如果前面是``则说明是图片
            # 发送的是表情或者图片
            if (t_text in dic) or if_photo[0] == '``' or if_photo[0] == '++':
                # 用不同个颜色区分私聊or群聊or自己发的消息
                message4 = '\n' + message2 + '：'  # \n发送消息的用户：
                date = time.strftime('%Y-%m-%d %H:%M:%S')
                message4 = message4 + ' (' + date + ') '
                if 'Group chat' in message3:
                    if message2 == user_name:
                        mesbox.insert(tkinter.END, message4, 'blue')
                    else:
                        mesbox.insert(tkinter.END, message4, 'green')
                elif message2 == user_name or message3 == user_name:
                    if message2 == user_name:
                        mesbox.insert(tkinter.END, message4, 'grey')
                    else:
                        mesbox.insert(tkinter.END, message4, 'red')
                if if_photo[0] == '``':
                    mesbox.insert(tkinter.END, '\n')
                    recievePhoto(if_photo[1])
                    send_photo = './client_photo_cache/' + if_photo[1]
                    if 'Group chat' in message3 or message2 == user_name or message3 == user_name:
                        # img = tkinter.PhotoImage(file=send_photo)
                        img = Image.open(send_photo)
                        img = ImageTk.PhotoImage(img)
                        mesbox.image_create(tkinter.END, image=img)
                elif if_photo[0] == '++':
                    mesbox.insert(tkinter.END, '\n')
                    recieveFile(if_photo[1])
                    send_file = './client_file_cache/' + if_photo[1]
                    if 'Group chat' in message3 or message2 == user_name or message3 == user_name:
                        file_icon = './icon/download.png'
                        icon_f = Image.open(file_icon)
                        img = ImageTk.PhotoImage(icon_f)
                        mesbox.image_create(tkinter.END, image=img)
                        mes = '发送文件：' + if_photo[1]
                        mesbox.insert(tkinter.END, mes)
                        file_box = tkinter.messagebox.askyesno(title='收到文件', message=message2 + '发送了一个文件，是否打开')
                        if file_box:
                            # 从缓存区打开该文件
                            os.system("start %s" % send_file)
                else:
                    if 'Group chat' in message3 or message2 == user_name or message3 == user_name:
                        mesbox.image_create(tkinter.END, image=dic[t_text])
            # 发送的是普通的消息
            else:
                message1 = '\n' + message1
                if 'Group chat' in message3:
                    if message2 == user_name:
                        mesbox.insert(tkinter.END, message1, 'blue')
                    else:
                        mesbox.insert(tkinter.END, message1, 'green')
                elif message2 == user_name or message3 == user_name:
                    if message2 == user_name:
                        mesbox.insert(tkinter.END, message1, 'grey')
                    else:
                        mesbox.insert(tkinter.END, message1, 'red')
                # elif message3 == 'exit':
                #     mesbox.insert(tkinter.END, '用户 ' + message2 + ' 已下线', 'pink')
        mesbox.see(tkinter.END)  # 显示在最后


t = threading.Thread(target=recv)
t.start()

root.mainloop()
s.close()
