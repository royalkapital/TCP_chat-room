# imports
import socket
import threading
from tkinter import *
from tkinter import messagebox
# import sys


# client's GUI class
class GUI:
    # firstly open login window and when the login is True, client will see chat window.
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.configure(width=500, height=300)

        self.icon_img = PhotoImage(file='icon_photo.png')
        self.login.iconphoto(False, self.icon_img)

        self.msg_login = Label(self.login,
                               text='Please login nickname to continue',
                               justify=CENTER,
                               font='Helvetica 14 bold')
        self.msg_login.place(relheight=0.15,
                             relx=0.2,
                             rely=0.07)

        self.label_name = Label(self.login,
                                text='Name: ',
                                font='Helvetica 12')
        self.label_name.place(relheight=0.2,
                              relx=0.1,
                              rely=0.215)

        self.entry_name = Entry(self.login,
                                font='Helvetica 14')
        self.entry_name.place(relwidth=0.6,
                              relheight=0.13,
                              relx=0.22,
                              rely=0.25)
        self.entry_name.focus()
        self.entry_name.bind('<Return>', lambda event: self.admin(self.entry_name.get()))

        self.go = Button(self.login,
                         text='LOGIN',
                         font='Helvetica 14 bold',
                         bg='green',
                         command=lambda: self.admin(self.entry_name.get()))
        self.go.place(relx=0.42,
                      rely=0.63)

        self.window.mainloop()

    # if client's nickname is admin, server have to check him password.
    # So client have to enter the password
    def admin(self, name):
        ctrl_name = client.recv(1024).decode(FORMAT)
        if ctrl_name == 'NAME':
            client.send(name.encode(FORMAT))
            ctrl_pass = client.recv(1024).decode(FORMAT)
            if ctrl_pass == 'PASS':
                self.label_pass = Label(self.login,
                                        text='Password: ',
                                        font='Helvetica 12')
                self.label_pass.place(relheight=0.2,
                                      relx=0.05,
                                      rely=0.4)
                self.entry_password = Entry(self.login,
                                            font='Helvetica 14')
                self.entry_password.place(relwidth=0.6,
                                          relheight=0.13,
                                          relx=0.22,
                                          rely=0.43)
                self.entry_password.focus()
                self.entry_password.bind('<Return>', lambda event: self.admin_check(name, self.entry_password.get()))

                self.go_as_admin = Button(self.login,
                                          text='LOGIN AS ADMIN',
                                          font='Helvetica 14 bold',
                                          bg='green',
                                          command=lambda: self.admin_check(name, self.entry_password.get()))
                self.go_as_admin.place(relx=0.35,
                                       rely=0.63)
            elif ctrl_pass == 'BAN':
                messagebox.showwarning('warning', 'Connection refused because of ban! You have banned by admin.')
                self.exit()

            elif ctrl_pass == 'USED':
                messagebox.showwarning('warning', 'The nick has used by other user.')
                self.exit()

            else:
                self.go_ahead(name)

    # If the server answer as ACCEPT, client will login as admin.
    # Otherwise client app will close.
    def admin_check(self, name, password):
        client.send(password.encode(FORMAT))
        ctrl_accept = client.recv(1024).decode(FORMAT)

        if ctrl_accept == 'ACCEPT':
            self.go_ahead(name)
        elif ctrl_accept == 'REFUSE':
            self.warning = messagebox.showwarning('warning', 'Password is incorrect. Please try again.')
            self.login.destroy()
            self.exit()

    # It is the function to close login window and enter the chat window.
    def go_ahead(self, name):
        self.login.destroy()
        self.layout(name)

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The layout of the chat window.
    def layout(self, name):
        self.name = name

        self.window.deiconify()
        self.window.title('CHATROOM')
        self.window.resizable(width=False,
                              height=False)
        self.window.configure(width=470,
                              height=550,
                              bg="#d6c7c7")

        self.window.iconphoto(False, self.icon_img)

        self.label_top = Label(self.window,
                               bg='#2b4536',
                               height=40)
        self.label_top.place(relwidth=1)

        self.label_head = Label(self.label_top,
                                bg="#2b4536",
                                fg="#EAECEE",
                                text=self.name,
                                font='Helvetica 13 bold',
                                pady=5)
        self.label_head.place(relwidth=1)

        self.text_cons = Text(self.window,
                              width=20,
                              height=2,
                              bg="#d6c7c7",
                              fg="#000000",
                              font="Helvetica 14",
                              padx=5,
                              pady=5,
                              spacing1=5,
                              spacing2=10,
                              spacing3=0)
        self.text_cons.place(relheight=0.745,
                             relwidth=1,
                             rely=0.08)

        self.label_bottom = Label(self.window,
                                  bg="#2b4536",
                                  height=50)
        self.label_bottom.place(relwidth=1,
                                rely=0.85)

        self.entry_msg = Entry(self.label_bottom,
                               bg="#d6c7c7",
                               fg="#000000",
                               font="Helvetica 13")
        self.entry_msg.place(relwidth=0.74,
                             relheight=0.06,
                             rely=0.008,
                             relx=0.011)
        self.entry_msg.focus()
        self.entry_msg.bind('<Return>', lambda event: self.send_button(self.entry_msg.get()))

        self.button_msg = Button(self.label_bottom,
                                 text="Send",
                                 font="Helvetica 12 bold",
                                 width=20,
                                 bg="#ABB2B9",
                                 command=lambda: self.send_button(self.entry_msg.get()))
        self.button_msg.place(relx=0.77,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.22)

        self.text_cons.config(cursor="arrow")

        scrollbar = Scrollbar(self.text_cons)
        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.text_cons.yview)

        self.text_cons.config(state=DISABLED)

    # The layout of the send button which is right-bottom side of the chat window.
    def send_button(self, msg):
        self.text_cons.config(state=DISABLED)
        self.msg = msg
        self.entry_msg.delete(0, END)
        snd = threading.Thread(target=self.send_message)
        snd.start()

    # This is the function which is the receive messages from server.
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'PENALTY':
                    self.warning_kick = messagebox.showwarning('warning', 'You were kicked by an admin!')
                    self.window.destroy()
                    self.exit()

                self.text_cons.config(state=NORMAL)
                self.text_cons.insert(END,
                                      message + "\n")

                self.text_cons.config(state=DISABLED)
                self.text_cons.see(END)
            except:
                messagebox.showerror('error', 'An error occured!')
                # print('An error occured!')
                self.window.destroy()
                self.exit()
                break

    # This is a function which send messages to the server when we click the send button.
    def send_message(self):
        self.text_cons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            if message[len(self.name)+2:].startswith('/'):
                if self.name == 'admin':
                    if message[len(self.name)+2:].startswith('/kick'):
                        client.send(f'KICK {message[len(self.name)+2+6:]}'.encode(FORMAT))
                    elif message[len(self.name)+2:].startswith('/ban'):
                        client.send(f'BAN {message[len(self.name)+2+5:]}'.encode(FORMAT))
                else:
                    messagebox.showinfo('info', 'Commands can only be executed by the admin!')
            else:
                client.send(message.encode(FORMAT))
            break

    def exit(self):
        messagebox.showinfo('exit', 'Thank you for using our chat application politely.')
        quit()


# connection parameters
PORT = 9999
SERVER = '192.168.67.1'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# main
if __name__ == '__main__':
    g = GUI()


