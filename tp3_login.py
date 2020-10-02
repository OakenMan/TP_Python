import tkinter as tk
from tkinter.messagebox import showinfo
import hashlib
import os

#from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

master = tk.Tk()

labelLogin = tk.Label(master, text="Login :")
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

def encryptFile(in_filename, salt, password):

    # On génère une vrai clé "solide" à partir du mot de passe utilisateur
    key = PBKDF2(password, salt, dkLen=32)

    out_filename = in_filename + ".bin"

    with open(in_filename, 'r') as input_file:
        lines = input_file.readlines()

        data = ""

        for line in lines:
            data += line + '\n'

        data = data.encode('utf-8')

        cipher = AES.new(key, AES.MODE_CFB)
        ciphered_data = cipher.encrypt(data)

        with open(out_filename, 'wb') as output_file:
            output_file.write(cipher.iv)
            output_file.write(ciphered_data)
            output_file.close()

        input_file.close()

    showinfo("Success", "File encrypted !")


def decryptFile(in_filename, salt, password):

    # On regénère la clé à partir des données utilisateur
    key = PBKDF2(password, salt, dkLen=32)

    out_filename = in_filename[:-4]

    with open(in_filename, 'rb') as input_file:

        iv = input_file.read(16)

        ciphered_data = input_file.read()
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        original_data = cipher.decrypt(ciphered_data)

        print(original_data)

        with open(out_filename, 'wb') as output_file:
            output_file.write(original_data)
            output_file.close()

        input_file.close()

    showinfo("Success", "File decrypted !")


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

            labelFile = tk.Label(master, text="Filename :")
            labelFile.pack()

            entryFile = tk.Entry(master, width=20)
            entryFile.pack()

            buttonEncrypt = tk.Button(
                master,
                text="Encrypt",
                width=15,
                command=lambda: encryptFile(entryFile.get(), salt, entryPassword.get()))
            buttonEncrypt.pack()

            buttonDecrypt = tk.Button(
                master,
                text="Decrypt",
                width=15,
                command=lambda: decryptFile(entryFile.get(), salt, entryPassword.get()))
            buttonDecrypt.pack()

        else:
            showinfo("Error", "Login or password incorrect !")

master.mainloop()