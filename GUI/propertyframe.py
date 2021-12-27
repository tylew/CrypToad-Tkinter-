# from tkinter import *
# from urllib.request import urlopen
# from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import errorcode
import requests
import json
import sys

#
# root = Tk()
# root.title("CrypToadz")
# root.geometry('1000x1000')

try:
    connection = mysql.connector.connect(
    host = "34.132.124.28",
    user = "tyler",
    password = "rooter",
    database = 'finalproject'
    )

except mysql.connector.Error as err:
   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print('Invalid credentials')
   elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print('Database not found')
   else:
      print('Cannot connect to database:', err)

cursor = connection.cursor()
print("Connection Made")


#
import tkinter as tk
from tkinter import ttk



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("350x650")
        self.title('Traitz')

        # initialize data
        self.traitsList = {}
        self.traitsList[0] = self.traitsfunc(1)
        self.traitsList[1] = self.traitsfunc(2)
        self.traitsList[2] = self.traitsfunc(3)
        self.traitsList[3] = self.traitsfunc(4)
        self.traitsList[4] = self.traitsfunc(5)
        self.traitsList[5] = self.traitsfunc(6)
        self.traitsList[6] = self.traitsfunc(7)
        self.traitsList[7] = self.traitsfunc(8)
        self.traitsList[8] = self.traitsfunc(9)

        # set up variables
        self.option1_var = tk.StringVar(self)
        self.option2_var = tk.StringVar(self)
        self.option3_var = tk.StringVar(self)
        self.option4_var = tk.StringVar(self)
        self.option5_var = tk.StringVar(self)
        self.option6_var = tk.StringVar(self)
        self.option7_var = tk.StringVar(self)
        self.option8_var = tk.StringVar(self)
        self.option9_var = tk.StringVar(self)

        # create widgets
        #----
        # label
        label = ttk.Label(self,  text='Background').pack()

        # option menu
        option1_menu = ttk.OptionMenu(
            self,
            self.option1_var,
            self.option1_var.get(),
            *self.traitsList[0],
            command=self.option_changed)

        option1_menu.pack()


        label = ttk.Label(self,  text='Body').pack()

        # option menu
        option2_menu = ttk.OptionMenu(
            self,
            self.option2_var,
            self.option2_var.get(),
            *self.traitsList[1],
            command=self.option_changed)

        option2_menu.pack()

        # label
        label = ttk.Label(self,  text='Head').pack()

        # option menu
        option3_menu = ttk.OptionMenu(
            self,
            self.option3_var,
            self.option3_var.get(),
            *self.traitsList[2],
            command=self.option_changed)

        option3_menu.pack()

        # label
        label = ttk.Label(self,  text='Eyes').pack()

        # option menu
        option4_menu = ttk.OptionMenu(
            self,
            self.option4_var,
            self.option4_var.get(),
            *self.traitsList[3],
            command=self.option_changed)

        option4_menu.pack()

        # label
        label = ttk.Label(self,  text='Mouth').pack()

        # option menu
        option5_menu = ttk.OptionMenu(
            self,
            self.option5_var,
            self.option5_var.get(),
            *self.traitsList[4],
            command=self.option_changed)

        option5_menu.pack()

        # label
        label = ttk.Label(self,  text='Clothes').pack()

        # option menu
        option6_menu = ttk.OptionMenu(
            self,
            self.option6_var,
            self.option6_var.get(),
            *self.traitsList[5],
            command=self.option_changed)

        option6_menu.pack()

        # label
        label = ttk.Label(self,  text='Accessory I').pack()

        # option menu
        option7_menu = ttk.OptionMenu(
            self,
            self.option7_var,
            self.option7_var.get(),
            *self.traitsList[6],
            command=self.option_changed)

        option7_menu.pack()

        # label
        label = ttk.Label(self,  text='Accessory II').pack()

        # option menu
        option8_menu = ttk.OptionMenu(
            self,
            self.option8_var,
            self.option8_var.get(),
            *self.traitsList[7],
            command=self.option_changed)

        option8_menu.pack()

        # label
        label = ttk.Label(self,  text='Custom').pack()

        # option menu
        option9_menu = ttk.OptionMenu(
            self,
            self.option9_var,
            self.option9_var.get(),
            *self.traitsList[8],
            command=self.option_changed)

        option9_menu.pack()







        # output label
        self.output_label = ttk.Label(self, foreground='red')
        self.output_label.pack()
        self.option_changed()
        #output label
        self.myLabel = ttk.Label(self)
        self.button = ttk.Button(self, text = "Execute", command = lambda: self.callSP([self.option1_var.get(),self.option2_var.get(),self.option3_var.get(),self.option4_var.get(),self.option5_var.get(),self.option6_var.get(),self.option7_var.get(),self.option8_var.get(),self.option9_var.get(), '@out_NFT'])).pack()



    def traitsfunc(self, t_id):
        query = "SELECT traitname FROM traits WHERE t_id = {id};".format(id = t_id)
        ret = ['']
        for i in self.single(query):
            ret.append(i[0])

        return ret

    def single(self,query):
        cursor.execute(query)
        results = cursor.fetchall()
        return results


    def option_changed(self, *args):


        self.output_label['text'] = f'''You\'ve selected NFTs with the following traits: \n
        Background: {self.option1_var.get()}
        Body: {self.option2_var.get()}
        Head: {self.option3_var.get()}
        Eyes: {self.option4_var.get()}
        Mouth: {self.option5_var.get()}
        Clothes: {self.option6_var.get()}
        Accessory I: {self.option7_var.get()}
        Accessory II: {self.option8_var.get()}
        Custom: {self.option9_var.get()}
        '''



        #traitChoice = {(self.option1_var.get(),self.option2_var.get(),self.option3_var.get(),self.option4_var.get(),self.option5_var.get(),self.option6_var.get(),self.option7_var.get(),self.option8_var.get(),self.option9_var.get()),}
        #list = [self.option1_var.get(),self.option2_var.get(),self.option3_var.get(),self.option4_var.get(),self.option5_var.get(),self.option6_var.get(),self.option7_var.get(),self.option8_var.get(),self.option9_var.get(), '@out_NFT']

    def callSP(self, args):

        # global id
        # global myLabel
        # print(args)
        nftID = cursor.callproc('sp', args)
        if nftID[9] is None:
            # self.id = "No Such Toad"
            self.myLabel.config(text = "No Such Toad")
            self.myLabel.pack(pady = 5)
            # print(self.id)
            # self.noneLabel = ttk.Label(self, text = "No such NFT").pack()

        else:
            strNFT = str(nftID[9])
            # self.id = "Toad ID: " + strNFT
            self.myLabel.config(text = "Toad ID: " + strNFT)
            self.myLabel.pack(pady = 5)
            # print(self.id)
            # self.nftLabel = ttk.Label(self, text = "Toad ID: " + strNFT).pack(padx = 20)





if __name__ == "__main__":
    app = App()
    app.mainloop()
