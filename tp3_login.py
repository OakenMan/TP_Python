import tkinter as tk
from tkinter.messagebox import showinfo
import hashlib
import os

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

    # On génère le sel
    salt = os.urandom(32)

    # On génère le hash
    hash = hashlib.pbkdf2_hmac(
        'sha256',                               # Algo à utiliser
        entryPassword.get().encode('utf-8'),    # On convertit en bytes
        salt,                                   # On lui fournit le "sel"
        100000                                  # Nbr. d'itérations de l'algo
    )

    # On écrit le login, sel et hash dans un fichier binaire sous cette forme :
    # 0: login
    # 1: sel+hash
    with open("./infos.txt", "wb") as file:
        loginBytes = entryLogin.get().encode('utf-8')
        file.write(loginBytes)
        file.write('\n'.encode('utf-8'))
        file.write(salt+hash)
        showinfo("Success", "Sign up successfull!")


def logIn():

    with open("./infos.txt", "rb") as file:
        infos = file.readlines()

        # On récupère le salt et le hash de l'utilisateur
        login = infos[0][:-1]
        salt = infos[1][:32]
        hash = infos[1][32:]

        # On recréé le nouveau hash de la même façon qu'on a créé l'ancien
        currentHash = hashlib.pbkdf2_hmac(
            'sha256',
            entryPassword.get().encode('utf-8'),
            salt,
            100000
        )

        currentLogin = entryLogin.get().encode('utf-8')

        # Si les 2 hashs (et les 2 logins) sont identiques, c'est OK!
        if currentHash == hash and currentLogin == login:
            showinfo("Success", "Login successfull !")
        else:
            showinfo("Error", "Login or password incorrect !")

master.mainloop()