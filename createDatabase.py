import requests
import urllib
import json  # Used to load data into JSON form

import mysql.connector

connection = mysql.connector.connect(
    host = "HOST IP",
    user = "DATABASE USER NAME",
    password = "DATABASE USER PASSWORD",
    database = 'DATABASE NAME'
)

print("Connected to database!")

# connection = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "tylerlewis",
#     database = 'cpsc408'
# )
#
# print("Connected to database!")

# import sqlite3
# connection = sqlite3.connect("/Users/lewis/Desktop/School/CPSC 408/9:14/chinook.db")

cursor = connection.cursor() #Create cursor object

url = "https://api.opensea.io/api/v1/asset/0x1cb1a5e65610aeff2551a50f76a87a7d3fb649c6/"

traitList = []
ownerList = []
nftList = []
historicalSales = []
currentSales = []

    # Take string of trait name and return its trait id
def t_type_to_t_id(t_type):
    t_id = 0
    if t_type == 'Background':
        t_id = 1
    elif t_type == 'Body':
        t_id = 2
    elif t_type == 'Head':
        t_id = 3
    elif t_type == 'Eyes':
        t_id = 4
    elif t_type == 'Mouth':
        t_id = 5
    elif t_type == 'Clothes':
        t_id = 6
    elif t_type == 'Accessory I':
        t_id = 7
    elif t_type == 'Accessory II':
        t_id = 8
    elif t_type == 'Custom':
        t_id = 9
    return t_id

def traitList_insertion(t_id,t_name):

    t_subid = 1 # Variabel to count of existing traits with same type, assign composite key
    # variable 't_subd' needs to start at 1 because the nft relation stores a 0 value as no value

    for curr_trait in traitList:
        if (curr_trait[0] == t_id):  # Came across trait with same type


            if (curr_trait[2] == t_name): # check is same name property. If exists then return and dont append traitList
                print("Repeat trait -- not inserted")
                return t_subid

            t_subid = t_subid + 1

    # No exact repeats found
    traitList.append((t_id,t_subid,t_name),)
    return t_subid

def add_properties(data):
    # Vars for adding NFT:
    nft_properties_list = [0,0,0,0,0,0,0,0,0]
    #                 1 2 3 4 5 6 7 8 9     Indexs for each property 1-9

    for curr_trait in data:
        t_type = curr_trait['trait_type']
        t_id = t_type_to_t_id(t_type) # Grab idNum from trait type
        if t_id == 0:
            continue # invalid trait, not one of the 9 types... NEXT TRAIT, gtfo

        t_name = curr_trait['value'] # Grab name of trait

        t_subid = traitList_insertion(t_id, t_name) # perform list insertion, grab subID

        nft_properties_list[t_id - 1] = t_subid

    return nft_properties_list


# Check if owner exists, add to database if not.
# Also return owner id # (index)
def add_owner(o_address, o_username):
    for index, o in enumerate(ownerList): # check if owner exists
        if o[1] == o_address:
            print("Duplicate owner -- not inserted")
            return o[0] # exists, so don't add, return ID #

    if o_username != None: # if not null, pull username. Will encounter error if you pull a null username
        o_username = o_username['username']

    print("Unique owner -- inserted")
    ownerList.append((len(ownerList),o_address, o_username),) # doesn't exist, add
    return len(ownerList)-1

# Add nft to database
def add_nft(n_id, o_id, nft_properties_list, image_url):
    p1 = nft_properties_list[0]
    p2 = nft_properties_list[1]
    p3 = nft_properties_list[2]
    p4 = nft_properties_list[3]
    p5 = nft_properties_list[4]
    p6 = nft_properties_list[5]
    p7 = nft_properties_list[6]
    p8 = nft_properties_list[7]
    p9 = nft_properties_list[8]

    nftList.append((n_id, o_id, image_url, p1,p2,p3,p4,p5,p6,p7,p8,p9),)

def add_sale_data(curr_id, ownerAddress, lastSaleData, inputOrders):
    sold = False
    if lastSaleData is not None:
        sold = True
        lastSalePrice = int(lastSaleData['total_price'])/1000000000000000000
        lastSaleDate = str(lastSaleData['event_timestamp'])
    else:
        print("No historical sale data")

    asking_price = 0
    top_bid = 0

    for order in inputOrders:
        bounty = int(order['current_bounty'])/10000000000000000 # price of order

        if ownerAddress == order['maker']['address']:
            if asking_price == 0:
                asking_price == bounty
            else:
                if bounty < asking_price:
                    asking_price == bounty # Lower asking price found, update var

        else: # order not made by owner
            if bounty > top_bid:
                top_bid = bounty

    current_value = 0 #take greatest price between asking/bid and set as current value
    if asking_price > top_bid:
        current_value = asking_price
    else:
        current_value = top_bid

    if sold:
        historicalSales.append((curr_id, lastSalePrice, lastSaleDate[:10]),)
    currentSales.append((curr_id, current_value),)

# Essentially main:
def create_database(id_nums):
    # Itterate through all NFTs between start and end id ints
    for curr_id in id_nums: # range of IDs want included in data

        print("\nWorking on ID# " + str(curr_id) + "...") # What freaking ID number am I looking at??? 🤣

        response = requests.request("GET", (url + str(curr_id) + '/')) # Load data
        data = json.loads(response.text)


        nft_properties_list = add_properties(data['traits'])

        o_id = add_owner(data['owner']['address'],data['owner']['user']) # store owner wallet address and return owners id number

        n_id = add_nft(curr_id, o_id, nft_properties_list,data['image_url'])

        add_sale_data(curr_id, data['owner']['address'], data['last_sale'], data['orders'])


# main

id_nums = [] # Need to account for all ID#s
for i in range(1,57):
    id_nums.append(i*1000000)
for i in range(1,6970):
    id_nums.append(i)

create_database(id_nums)

query = '''
    INSERT INTO nft
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
cursor.executemany(query, nftList)

query = '''
    INSERT INTO owners
    VALUES (%s,%s,%s)
    '''
cursor.executemany(query, ownerList)

query = '''
    INSERT INTO traits
    VALUES (%s,%s,%s)
    '''
cursor.executemany(query, traitList)

query = '''
    INSERT INTO historicalSales
    VALUES (%s,%s,%s);
    '''
cursor.executemany(query, historicalSales)

query = '''
    INSERT INTO currentValue
    VALUES (%s,%s)
    '''
cursor.executemany(query, currentSales)




connection.commit() # commit to database
connection.close()
