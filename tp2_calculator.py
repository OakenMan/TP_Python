import tkinter as tk
from tkinter.messagebox import showinfo


class Calculator(tk.Frame):

    expression = ""                 # Contient l'expression à calculer
    calc_done = False               # True si le calcul a été réalisé (après avoir appuyé sur '=')
    last_char_is_operator = False   # True si le dernier caractère est un opérateur (+, -, *, /)
    last_char_is_zero = False       # True si le dernier caractère est un zero (sert plus à rien?)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Ajoute la barre de résultat
        self.resbar = tk.Text(self)
        self.resbar["state"] = "normal"
        self.resbar["height"] = 2
        self.resbar["width"] = 25
        self.resbar.grid(row=4, column=0, columnspan=4, ipadx=5, ipady=5)

        # Ajoute tous les boutons
        self.add_buttons()

        # Ajoute le menu
        self.menuBar = tk.Menu(self)
        root["menu"] = self.menuBar
        self.menuBar.add_command(label="Settings", command=lambda: print("show settings"))
        self.menuBar.add_command(label="Help", command=lambda: showinfo("Help", "Do you really need help to use a calculator ?"))

    def add_buttons(self):
        button0 = tk.Button(self)
        button0["text"] = "0"
        button0["height"] = 2
        button0["width"] = 2
        button0["command"] = lambda: self.add_number("0")
        button0.grid(row=0, column=1, ipadx=5, ipady=5)

        button1 = tk.Button(self)
        button1["text"] = "1"
        button1["height"] = 2
        button1["width"] = 2
        button1["command"] = lambda: self.add_number("1")
        button1.grid(row=1, column=0, ipadx=5, ipady=5)

        button2 = tk.Button(self)
        button2["text"] = "2"
        button2["height"] = 2
        button2["width"] = 2
        button2["command"] = lambda: self.add_number("2")
        button2.grid(row=1, column=1, ipadx=5, ipady=5)

        button3 = tk.Button(self)
        button3["text"] = "3"
        button3["height"] = 2
        button3["width"] = 2
        button3["command"] = lambda: self.add_number("3")
        button3.grid(row=1, column=2, ipadx=5, ipady=5)

        button4 = tk.Button(self)
        button4["text"] = "4"
        button4["height"] = 2
        button4["width"] = 2
        button4["command"] = lambda: self.add_number("4")
        button4.grid(row=2, column=0, ipadx=5, ipady=5)

        button5 = tk.Button(self)
        button5["text"] = "5"
        button5["height"] = 2
        button5["width"] = 2
        button5["command"] = lambda: self.add_number("5")
        button5.grid(row=2, column=1, ipadx=5, ipady=5)

        button6 = tk.Button(self)
        button6["text"] = "6"
        button6["height"] = 2
        button6["width"] = 2
        button6["command"] = lambda: self.add_number("6")
        button6.grid(row=2, column=2, ipadx=5, ipady=5)

        button7 = tk.Button(self)
        button7["text"] = "7"
        button7["height"] = 2
        button7["width"] = 2
        button7["command"] = lambda: self.add_number("7")
        button7.grid(row=3, column=0, ipadx=5, ipady=5)

        button8 = tk.Button(self)
        button8["text"] = "8"
        button8["height"] = 2
        button8["width"] = 2
        button8["command"] = lambda: self.add_number("8")
        button8.grid(row=3, column=1, ipadx=5, ipady=5)

        button9 = tk.Button(self)
        button9["text"] = "9"
        button9["height"] = 2
        button9["width"] = 2
        button9["command"] = lambda: self.add_number("9")
        button9.grid(row=3, column=2, ipadx=5, ipady=5)

        buttonAC = tk.Button(self)
        buttonAC["text"] = "AC"
        buttonAC["height"] = 2
        buttonAC["width"] = 2
        buttonAC["command"] = lambda: self.clear_all()
        buttonAC.grid(row=0, column=0, ipadx=5, ipady=5)

        buttonC = tk.Button(self)
        buttonC["text"] = "C"
        buttonC["height"] = 2
        buttonC["width"] = 2
        buttonC["command"] = lambda: self.clear()
        buttonC.grid(row=0, column=2, ipadx=5, ipady=5)

        buttonAdd = tk.Button(self)
        buttonAdd["text"] = "+"
        buttonAdd["height"] = 2
        buttonAdd["width"] = 2
        buttonAdd["command"] = lambda: self.add_operator("+")
        buttonAdd.grid(row=0, column=3, ipadx=5, ipady=5)

        buttonMinus = tk.Button(self)
        buttonMinus["text"] = "-"
        buttonMinus["height"] = 2
        buttonMinus["width"] = 2
        buttonMinus["command"] = lambda: self.add_operator("-")
        buttonMinus.grid(row=1, column=3, ipadx=5, ipady=5)

        buttonProduct = tk.Button(self)
        buttonProduct["text"] = "*"
        buttonProduct["height"] = 2
        buttonProduct["width"] = 2
        buttonProduct["command"] = lambda: self.add_operator("*")
        buttonProduct.grid(row=2, column=3, ipadx=5, ipady=5)

        buttonDivide = tk.Button(self)
        buttonDivide["text"] = "/"
        buttonDivide["height"] = 2
        buttonDivide["width"] = 2
        buttonDivide["command"] = lambda: self.add_operator("/")
        buttonDivide.grid(row=3, column=3, ipadx=5, ipady=5)

        buttonEqual = tk.Button(self)
        buttonEqual["text"] = "="
        buttonEqual["height"] = 2
        buttonEqual["width"] = 2
        buttonEqual["command"] = lambda: self.calc()
        buttonEqual.grid(row=4, column=4, ipadx=5, ipady=5)

        buttonOpenPar = tk.Button(self)
        buttonOpenPar["text"] = "("
        buttonOpenPar["height"] = 2
        buttonOpenPar["width"] = 2
        buttonOpenPar["command"] = lambda: self.add_par("(")
        buttonOpenPar.grid(row=0, column=4, ipadx=5, ipady=5)

        buttonClosePar = tk.Button(self)
        buttonClosePar["text"] = ")"
        buttonClosePar["height"] = 2
        buttonClosePar["width"] = 2
        buttonClosePar["command"] = lambda: self.add_par(")")
        buttonClosePar.grid(row=1, column=4, ipadx=5, ipady=5)

        buttonDot = tk.Button(self)
        buttonDot["text"] = "."
        buttonDot["height"] = 2
        buttonDot["width"] = 2
        buttonDot["command"] = lambda: self.add_par(".")
        buttonDot.grid(row=2, column=4, ipadx=5, ipady=5)

        buttonPow = tk.Button(self)
        buttonPow["text"] = "^"
        buttonPow["height"] = 2
        buttonPow["width"] = 2
        buttonPow["command"] = lambda: self.add_par("**")
        buttonPow.grid(row=3, column=4, ipadx=5, ipady=5)

    # Ajoute un nombre à l'expression
    def add_number(self, symbol):
        if self.calc_done:
            return
        self.expression += symbol
        self.resbar.insert(tk.END, symbol)
        self.last_char_is_operator = False

    # Ajoute un opérateur à l'expression
    def add_operator(self, operator):
        if self.calc_done:
            return
        if self.last_char_is_operator:
            self.clear()
        self.expression += operator
        self.resbar.insert(tk.END, operator)
        self.last_char_is_operator = True
        self.last_char_is_zero = False

    # Ajoute des parenthèses (ou des virgules/puissances...) à l'expression
    def add_par(self, symbol):
        if self.calc_done:
            return
        self.expression += symbol
        self.resbar.insert(tk.END, symbol)

    # Effectue le calcul et affiche le résultat
    def calc(self):
        if self.calc_done:
            return
        self.calc_done = True
        self.resbar.insert(tk.END, " = \n")

        try:
            res = eval(self.expression)
        except SyntaxError:
            res = "SyntaxError"
        except ZeroDivisionError:
            res = "ZeroDivisionError"

        self.resbar.insert(tk.END, str(res))

    # Supprime le dernier caractère (ou tout si on a effectué le calcul)
    def clear(self):
        if self.calc_done:
            self.clear_all()
        else:
            self.expression = self.expression[:-1]
            self.resbar.delete('1.0', tk.END)
            self.resbar.insert(tk.END, self.expression)

    # Supprime toute l'expression
    def clear_all(self):
        self.expression = ""
        self.resbar.delete('1.0', tk.END)
        self.calc_done = False

# Créé la fenêtre et lance la main loop
root = tk.Tk()
root.title("Calculator")
app = Calculator(master=root)
app.mainloop()