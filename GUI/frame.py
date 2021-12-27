from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import errorcode
import requests
import json
import sys
from io import BytesIO
from fpdf import FPDF
import urllib.request
from propertyframe import App
#configure root window
root = Tk()
root.title("CrypToadz")
# root.geometry('1000x1000')
root.config(bg = "lavender")

#center root window
app_width = 1000
app_height = 1000
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

#create database connection
# db_ops = db_operations()

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


#frame for displaying records
displayFrame = LabelFrame(root, text = "Display Toadz", padx = 50, pady = 50, fg = "red", bd = 6)
# displayFrame.pack(padx = 10, pady = 10)
displayFrame.grid(row = 0, column = 0, padx = 20, pady = 5)

#a list that consists of all relevant data from display frame to pass to populateOutput
dfList = []


#displayFrame labels
priceLabel = Label(displayFrame)
lastSoldLabel = Label(displayFrame)
imgLabel = Label(displayFrame)
errorLabel = Label(displayFrame)

queryButton = Button(displayFrame)


#entry in the frame, rather than in the root
nIDEntry = Entry(displayFrame, borderwidth = 3)
nIDEntry.grid(row = 1, column = 0)
nIDEntry.insert(0, "CrypToadz ID")




queryButton = Button(displayFrame, text = "Execute", command = lambda:
[
# checkExistence(nIDEntry.get()),
priceFunc(nIDEntry.get()),
lastSoldPrice(nIDEntry.get()),
imageFunc(nIDEntry.get())
])
queryButton.grid(row = 2, column = 0)


#frame for query for data with filters
filterFrame = LabelFrame(root, text = "Filter Toadz", padx = 50, pady = 50)
# filterFrame.pack(padx = 10, pady = 10)
filterFrame.grid(row = 0, column = 1, padx = 20, pady = 10)

#filterFrame labels
# filterLabel = Label(filterFrame, text = "Select filter properties")
# filterLabel.grid(row = 0, column = 1)
toadLabel = Label(filterFrame)


filterButton = Button(filterFrame, text = "Query", command = lambda: filter(cList))


#output frame at the bottom of the screen
outputFrame = LabelFrame(root, text = "Output", padx = 65, pady = 20, fg = "purple", bd = 6)
# outputFrame.pack(padx = 10, pady = 10)
outputFrame.grid(row = 3, column = 0, pady = 5)
# practiceLabel = Label(outputFrame, text = "Practice")
# practiceLabel.grid(row = 0, column = 0)

#output frame labels
nftIDLabel = Label(outputFrame)
currPriceLabel = Label(outputFrame)
lsPriceLabel = Label(outputFrame)
imageLabel = Label(outputFrame)
noPriceLabel = Label(outputFrame)

#crudFrame
crudFrame = LabelFrame(root, text = "Sandbox", padx = 50, pady = 55, fg = "green", bd = 6)
# crudFrame.pack(padx = 10, pady = 10)
crudFrame.grid(row = 0, column = 2, padx = 20, pady = 5)

#crud queries
createQuery = ""
updateQuery = ""
deleteQuery = ""

#names argument for cursor
names = ()

#crud entries
usernameEntry = Entry(crudFrame)
currentUserEntry = Entry(crudFrame)
newUserEntry = Entry(crudFrame)
usernameEntry2 = Entry(crudFrame)

#crud varialbes
userNameVar = StringVar()
currentNameVar = StringVar()
newNameVar = StringVar()

#crud Button
crudBut = Button(crudFrame, text = "Execute")
# crudBut.config(state = DISABLED)
crudBut.grid(row = 3, column = 0)

#crud labels
crudLabel = Label(crudFrame)



#aggregate function frame
aggFrame = LabelFrame(root, text = "Ownerz", padx = 50, pady = 50, fg = "blue", bd = 6)
aggFrame.grid(row = 2, column = 0, padx = 20, pady = 5)

#aggregate frame entry for owner id
oIDEntry = Entry(aggFrame, borderwidth = 3)
oIDEntry.grid(row = 1, column = 0)
oIDEntry.insert(0, "Owner ID")

#aggFrame button
aggButton = Button(aggFrame, text = "Execute", command = lambda: ownerBone(oIDEntry.get()))
aggButton.grid(row = 2, column = 0)

#aggFrame labels
aggUserLabel = Label(outputFrame)
aggCountLabel = Label(outputFrame)
noOwnerLabel = Label(aggFrame)



#this button is wrapped in a frame for design purposes
#this button calls App, which launches a new window with filter functionality 
traits_button_border = Frame(root, highlightbackground = "black", highlightthickness = 2, bd=0)
traits_button_border.grid(row = 2, column = 2)
traitsButton = Button(traits_button_border, text = 'Traitz', fg = 'black', bg = 'yellow',font = (("Arial"),15), command = App)
traitsButton.pack()



#aggButton calls this function, which calls the callBone function, which fires
#the SQL stored procedure 'bone'
#bone is an aggregate function with a group by that returns the count of a user selected owner's Toadz
def ownerBone(oID):

    #error handling
    # if checkOwnerExistence(oID) == False:
    #     clearAggFrame()
    #     clearOutputFrame()
    #     return -1
    global noOwnerLabel
    noOwnerLabel.destroy()

    # ownerQuery = "CALL bone({oID});".format(oID = int(oID))
    args = [int(oID), '@totalToadz']
    result = callBone(args)
    #error handling if owner id doesn't exist
    if len(result) == 0:
        print("Owner Does Not Exist")
        noOwnerLabel = Label(aggFrame, text = "Owner ID Doesn't Exist", fg = "red")
        noOwnerLabel.grid(row = 3, column = 0)
    populateOutput(result)




#function for deleting all widgets in crudFrame
def clearCrudFrame():
    usernameEntry.destroy()
    currentUserEntry.destroy()
    newUserEntry.destroy()
    usernameEntry2.destroy()
    crudLabel.destroy()
    # crudBut.config(state = DISABLED)

#creates insert query (crudFrame)
def createQueryFunc(username):
    #global means I'm manipulating the actual vale of createQuery (to avoid local scope issues)
    global createQuery
    createQuery = '''
    INSERT INTO usernameView VALUES (101, 7000, '{username}');
    '''.format(username = username)



#creates update query (crudFrame)
def updateQueryFunc(newUser, currUser):
    global updateQuery
    global names
    updateQuery = '''
    UPDATE usernameView SET username = %s WHERE username = %s;
    '''
    names = (newUser, currUser)

#creates delete query (crudFrame)
def deleteQueryFunc(username):
    global deleteQuery
    deleteQuery = '''
    DELETE FROM usernameView WHERE username = '{username}'
    '''.format(username = username)

#function for handling user option based on drop down menu
def selected(event):

    global usernameEntry
    global currentUserEntry
    global newUserEntry
    global crudBut

    #if user wants to create new user
    if clicked.get() == "Create":
        clearCrudFrame()
        crudBut.config(text = "Create", state = ACTIVE)
        #username entry widget
        usernameEntry = Entry(crudFrame, borderwidth = 3)
        usernameEntry.grid(row = 1, column = 0)
        usernameEntry.insert(0, "Username")
        crudBut.config(command = lambda: [createQueryFunc(usernameEntry.get()), popWindow()])


        #if user wants to update current username
    elif clicked.get() == "Update":
        clearCrudFrame()
        crudBut.config(text = "Update", state = ACTIVE)
        #current username entry widget
        currentUserEntry = Entry(crudFrame, borderwidth = 3)
        currentUserEntry.grid(row = 1, column = 0)
        currentUserEntry.insert(0, "Current Username")

        #new username entry widget
        newUserEntry = Entry(crudFrame, borderwidth = 3)
        newUserEntry.grid(row = 2, column = 0)
        newUserEntry.insert(0, "New Username")
        crudBut.config(command = lambda: [updateQueryFunc(newUserEntry.get(), currentUserEntry.get()), popWindow()])


    #if user wants to delete current user
    elif clicked.get() == "Delete":
        clearCrudFrame()
        crudBut.config(text = "Delete", state = ACTIVE)
        #username entry widget
        usernameEntry2 = Entry(crudFrame, borderwidth = 3)
        usernameEntry2.grid(row = 1, column = 0)
        usernameEntry2.insert(0, "Username")
        crudBut.config(command = lambda: [deleteQueryFunc(usernameEntry2.get()), popWindow()])



#boolean to determine whether user commits or rollbacks query
commit_or_cancel = True

#commit or cancel handler
def choice(option):
    #close pop window
    pop.destroy()
    global crudLabel
    crudLabel.destroy()


    if option == "commit":
        #user wants to commit query
        commit_or_cancel = True
        if clicked.get() == "Create":
            update(createQuery, commit_or_cancel)
            crudLabel = Label(crudFrame, text = "Create Successful", fg = "green")
            crudLabel.grid(row = 4, column = 0)

        elif clicked.get() == "Delete":
            update(deleteQuery, commit_or_cancel)
            crudLabel = Label(crudFrame, text = "Delete Successful", fg = "green")
            crudLabel.grid(row = 4, column = 0)
        else:
            updateMany(updateQuery, names, commit_or_cancel)
            crudLabel = Label(crudFrame, text = "Update Successful", fg = "green")
            crudLabel.grid(row = 4, column = 0)
    else:
        #user wants to rollback query
        commit_or_cancel = False
        if clicked.get() == "Create":
            update(createQuery, commit_or_cancel)
        elif clicked.get() == "Delete":
            update(deleteQuery, commit_or_cancel)
        else:
            updateMany(updateQuery, names, commit_or_cancel)


#pop up window that displays commit or cancel option
def popWindow():

    global pop
    pop = Toplevel(root)
    pop.title("")
    # pop.geometry("250x150")
    #center root window
    pop_width = 250
    pop_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (pop_width / 2)
    y = (screen_height / 2) - (pop_height / 2)
    pop.geometry(f'{pop_width}x{pop_height}+{int(x)}+{int(y)}')
    # pop.config(bg = "lavender")



    #frame for popwwindow
    popFrame = Frame(pop)
    popFrame.grid(row = 3, column = 3)

    popLabel = Label(popFrame, text = "Commit Changes?")
    popLabel.grid(row = 0, column = 1, padx = 10, pady = 20)


    commit = Button(popFrame, text = "Commit", command = lambda: choice("commit"))
    commit.grid(row = 1, column = 0)

    cancel = Button(popFrame, text = "Cancel", command = lambda: choice("cancel"))
    cancel.grid(row = 1, column = 1)

crudOptions = [
    "Create",
    "Update",
    "Delete"
]

clicked = StringVar()

dropDownMenu = OptionMenu(crudFrame, clicked, *crudOptions, command = selected)
dropDownMenu.grid(row = 0, column = 0)


successLabel = Label(outputFrame)
def pdf(url):
    # save FPDF() class into a
    # variable pdf
    global successLabel
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    nftLabelText = nftIDLabel['text']
    currPriceText = currPriceLabel['text']
    lsPriceText = lsPriceLabel['text']

    nftLabelText = nftLabelText.encode('latin-1', 'replace').decode('latin-1')
    currPriceText = currPriceText.encode('latin-1', 'replace').decode('latin-1')
    lsPriceText = lsPriceText.encode('latin-1', 'replace').decode('latin-1')

    # .encode('latin-1')

    # set style and size of font
    # that you want in the pdf
    pdf.set_font('Arial', 'B', 14)


    # create a cell
    pdf.cell(200, 10, txt = nftLabelText, ln = 1, align = 'C')

    # add another cell
    pdf.cell(200, 10, txt = currPriceText, ln = 2, align = 'C')

    # add another cell
    pdf.cell(200, 10, txt = lsPriceText, ln = 3, align = 'C')

    #convert image to suitable format for FPDF
    toadImage = urllib.request.urlretrieve(url, "toadImage.PNG")
    pdf.image(toadImage[0], 82,40,60,60)

    # save the pdf with name .pdf
    pdf.output("MyToad.pdf").encode('latin-1')
    successLabel = Label(outputFrame, text = "Exported as MyToad.pdf", fg = "green")
    successLabel.grid(row = 5, column = 0)



pdfButton = Button(outputFrame)


#output frame has a fixed display, no matter the query.
#output frame always returns a toad's essential data. The other queries are just
#a matter of filters or CRUDs
#populateOutput accepts a list ==> [nftID, currPrice, lsPrice, photo]
def populateOutput(list):

    global nftIDLabel
    global currPriceLabel
    global lsPriceLabel
    global imageLabel
    global pdfButton
    global noPriceLabel
    global aggUserLabel
    global aggCountLabel



    #deletes the current display prior to displaying new information
    nftIDLabel.destroy()
    currPriceLabel.destroy()
    lsPriceLabel.destroy()
    imageLabel.destroy()
    noPriceLabel.destroy()
    successLabel.destroy()
    aggUserLabel.destroy()
    aggCountLabel.destroy()
    pdfButton.destroy()

    if len(list) == 2:
        clearOutputFrame()
        username = list[0]
        count = list[1]

        aggUserLabel = Label(outputFrame, text = "Username: " + username)
        aggUserLabel.grid(row = 0, column = 0)

        aggCountLabel = Label(outputFrame, text = "Total Toad Quantity: " + str(count))
        aggCountLabel.grid(row = 1, column = 0)
    elif len(list) == 3:
        clearOutputFrame()
        #current toad ID label
        nftIDLabel = Label(outputFrame, text = list[0])
        idText = nftIDLabel['text']
        nftIDLabel['text'] = "Toad ID: " + str(idText)
        nftIDLabel.grid(row = 0, column = 0)

        #current toad price label
        currPriceLabel = Label(outputFrame, text = list[1])
        priceText = currPriceLabel['text']
        currPriceLabel['text'] = "Price: " + str(priceText) + "E"#+ "Ξ"
        currPriceLabel.grid(row = 1, column = 0)

        #current toad last sold price label
        lsPriceLabel = Label(outputFrame, text = list[2])
        lsText = lsPriceLabel['text']
        if lsText == '0':
            lsPriceLabel.config(text = 'Unsold')
            lsPriceLabel.grid(row = 2, column = 0)
            # noPriceLabel = Label(outputFrame, text = "Unsold")
            # noPriceLabel.grid(row = 2, column = 0)
        else:
            lsPriceLabel['text'] = "Last Sold: " + str(lsText) + "E"#+ "Ξ"
            lsPriceLabel.grid(row = 2, column = 0)
        # print("Saved URL: " + savedURL)
        pdfButton = Button(outputFrame, text = "Export as PDF", command = lambda: pdf(savedURL))
        pdfButton.grid(row = 4, column = 0, pady = 5)





def checkExistence(n_id):
    if not n_id.isdigit():
        displayError(displayFrame, 3, 0)
        return False
    if (int(n_id)/1000000 >= 1) and (int(n_id)/1000000 <= 56):
        return True
    if (int(n_id) > 6969) or (int(n_id) <= 0):
        displayError(displayFrame, 3, 0)
        #if the n_id doesn't exist then the entire program shouldn't run, but it currently is
        return False
    else:
        return True

def displayError(frame, row, column):
    global errorLabel
    errorLabel.destroy()
    errorLabel = Label(frame, text = "Toad ID does not exist", fg = "red")
    errorLabel.grid(row = row, column = column)

def clearDisplayFrame():
    #reset all widgets in the frame
    priceLabel.destroy()
    lastSoldLabel.destroy()
    imgLabel.destroy()

def clearOutputFrame():
    nftIDLabel.destroy()
    currPriceLabel.destroy()
    lsPriceLabel.destroy()
    imageLabel.destroy()
    noPriceLabel.destroy()
    pdfButton.destroy()
    successLabel.destroy()
    aggUserLabel.destroy()
    aggCountLabel.destroy()




#function that returns nft price
def priceFunc(n_id):

    if checkExistence(n_id) == False:
        clearDisplayFrame()
        clearOutputFrame()
        return -1


    if errorLabel:
        errorLabel.destroy()

    priceQuery = '''
    SELECT price
    FROM currentValue
    WHERE n_id = {nftID}
    '''.format(nftID = n_id)

    dfList.append(n_id)
    dfList.append(single_attribute2(priceQuery))





#function that returns nft last sold price
def lastSoldPrice(n_id):

    global lastSoldLabel

    if checkExistence(n_id) == False:
        noPriceLabel.destroy()
        clearDisplayFrame()
        clearOutputFrame()
        return -1

    #remove current label
    lastSoldLabel.destroy()
    noPriceLabel.destroy()

    if errorLabel:
        lastSoldLabel.destroy()
        noPriceLabel.destroy()
        # return -1

    lastSoldQuery = '''
    SELECT salePrice
    FROM historicalSales
    WHERE n_id = {nftID}
    '''.format(nftID = n_id)



    dfList.append(single_attribute2(lastSoldQuery))




savedURL = ""


def imageFunc(n_id):

    global imageLabel
    global savedURL
    if checkExistence(n_id) == False:
        clearDisplayFrame()
        clearOutputFrame()
        imageLabel.destroy()
        return -1


    #query to retrieve image of specific NFT
    imageQuery = '''
    SELECT image_url
    FROM nft
    WHERE n_id = {nftID}
    '''.format(nftID = n_id)

    #images require unique code, so I'm not calling single_attribute here
    cursor.execute(imageQuery)
    url = cursor.fetchall()
    url = [i[0] for i in url]

    #check if list is empty
    if not url:
        return -1
    else:
        url = url[0]
        savedURL = url

    #display image
    response = requests.get(url)
    photo = Image.open(BytesIO(response.content))
    photo = photo.resize((135,135))
    photo = ImageTk.PhotoImage(photo)



    #calling populateOutput since dfList is fully populated now
    populateOutput(dfList)
    #clearing dfList for next queries
    dfList.clear()

    imageLabel = Label(outputFrame, image = photo)
    imageLabel.image = photo
    imageLabel.grid(row = 3, column = 0)




# function to return a single attribute values from table
def single_attribute(frame, query):
    cursor.execute(query)
    results = cursor.fetchall()
    myLabel = Label(frame, text = results)
    return myLabel

def single_attribute2(query):
    cursor.execute(query)
    results = cursor.fetchall()
    # print("Result: " + str(results))
    if not results:
        return '0'
    else:
        return str(results[0][0])

def callBone(args):

    getUserName = "SELECT username FROM owners WHERE o_id = {oID}".format(oID = args[0])
    cursor.execute(getUserName)
    username = cursor.fetchall()

    result = cursor.callproc('bone', args)

    if username[0][0] is None:
        return []
    else:
        return [username[0][0], result[1]]




def update(query, bool):
    #execute query
    cursor.execute(query)
    #commit the query if bool is true
    if bool == True:
        connection.commit()
    elif bool == False: #rollback query if bool is false
        connection.rollback()
    else:
        print("Error occurred during update")


def updateMany(query, records, bool):
    #execute query
    cursor.execute(query, records)
    if bool == True:
        connection.commit()
    elif bool == False:
        connection.rollback()
    else:
        print("Error occurred during updates")





root.mainloop()
cursor.close()
connection.close()
