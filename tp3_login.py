import tkinter as tk
from tkinter.messagebox import showinfo
import hashlib

master = tk.Tk()

labelLogin = tk.Label(master, text="Login :")
labelLogin["text"] = "Login :"
labelLogin.pack()

entryLogin = tk.Entry(master, width=20)
entryLogin.pack()

labelPassword = tk.Label(master, text="Password :")
labelPassword.pack()

entryPassword = tk.Entry(master, width=20, show='*')
entryPassword.pack()

buttonSignUp = tk.Button(master, text="Sign Up", width=15, command=lambda: signUp())
buttonSignUp.pack()

buttonLogIn = tk.Button(master, text="Log In", width=15, command=lambda: logIn())
buttonLogIn.pack()

def signUp():
    hash = hashlib.sha512(entryPassword.get().encode()).hexdigest()
    with open("./infos.txt", "w") as file:
        file.write(entryLogin.get()+"\n"+hash)
        showinfo("Success", "Sign up successfull!")
        

def logIn():
    hash = hashlib.sha512(entryPassword.get().encode()).hexdigest()
    with open("./infos.txt", "r") as file:
        infos = file.readlines()
        trueHash = infos[1]
        if trueHash == hash:
            showinfo("Success", "Login successfull !")
        else:
            showinfo("Error", "Password incorrect !")

master.mainloop()