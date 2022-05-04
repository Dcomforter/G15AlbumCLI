import csv # For reading and writing into csv files
import hashlib # For hashing passwords
import pandas as pd # For deleting rows easily
import os
from datetime import datetime

def login():
    username = input("Username: ") # Get username

    user_found = False # Start with user not found
    correct_password = "" # Initital password
    
    # Check if the user exists in the database
    with open ('users.csv') as user_file:
        csv_reader = csv.reader(user_file, delimiter=',')
        for row in csv_reader:
            if username == row[0]: # User found
                user_found = True
                correct_password = row[1] # Get the password for that user

    # Ask for password if user is found.
    if user_found:
        password = input("Password: ") # Get user's password
        pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest() # Generate password hash

        if pass_hash == correct_password:
            return True, username
        else:
            print ("Wrong password.")
            return False, ""
    else:  # Ask for account creation if user not found  
        create_user = input("User does not exist.\nDo you want to create one?(y/n): ")
        if create_user.lower() == 'y':
            return createAccount(username) # Call createAccount function to create an account
        else:
            return False, ""

# Function to create an account and save it in the database
def createAccount(name):
    passphrase = input("Enter Password: ")
    confirm_passphrase = input("Confirm Password: ")

    if passphrase == confirm_passphrase:
        pass_hash = hashlib.md5(passphrase.encode("utf-8")).hexdigest() # Generate password hash

        address = input("Enter shipping address: ")
        card = input("Enter card number: ")
        # Save user info in the file
        with open ('users.csv', 'a+', newline='') as user_file:
            csv_writer = csv.writer(user_file)
            csv_writer.writerow([name, pass_hash, address, card])
        print("Account {} created successfully.".format(name))
        return True, name
    else:
        print("Password confirmation Error!")
        return False, ""

# Prints menu for the user
def userMessage():
    print("\n=========== List of commands =============")
    print("view all\t\t-\t View all items")
    print("view cart\t\t-\t View all items in your shopping cart")
    print("add [item number]\t-\t Add item to your shopping cart")
    print("rm [item]\t\t-\t Remove item from your shopping cart")
    print("checkout\t\t-\t Checkout all items from your currect shopping cart")
    print("view history\t\t-\t View your order history.")
    print("edit\t\t\t-\t Edit your account")
    print("delete\t\t\t-\t Delete your account")
    print("logout\t\t\t-\t Log out of your account\n")

# Menu for logged in user
def userMenu(user):
    print(user, "logged in.")
    userMessage()
    logged_in = True
    while logged_in:
        in_command = input(">> ").lower()

        # Check if input is not empty.
        if in_command == "":
            in_command = "null"

        command = in_command.split() # Parse the input

        # Process the input 
        if command[0] == "view":
            try:
                if command[1] == "all":
                    # Print all info from albums.csv
                    with open("albums.csv") as f:
                        csv_f = csv.reader(f)
                        for row in csv_f:
                            print('{:<15} {:<15} {:<15} {:<15} {:<15}'.format(*row))
                    print()
                    
                   
                elif command[1] == "cart":
                    print('{:<10} {:<10} {:<10} {:<10}'.format("Username", "AlbumID", "Quantity", "Price"))
                    #search for the username in carts.csv
                    with open("carts.csv") as f:
                        csv_f = csv.reader(f)
                        for row in csv_f:
                            #print the orders once found
                            if row[0] == user:
                                print('{:<10} {:<10} {:<10} ${:<10}'.format(*row))
                    print()
                        
                    
                elif command[1] == "history":
                    print('{:<10} {:<10} {:<10} {:<10}  {:<10}'.format("Username", "AlbumID", "Quantity", "Price", "Order Placed"))
                    #search for the username in orders.csv
                    with open("orders.csv") as f:
                        csv_f = csv.reader(f)
                        for row in csv_f:
                            #print the orders once found
                            if row[0] == user:
                                print('{:<10} {:<10} {:<10} ${:<10} {:<10}'.format(*row))
                    print()
                else:
                    raise IndexError
            except IndexError:
                print("Wrong input")
                userMessage()

        elif command[0] == "add":
            try:
                item_to_search = command[1]
                user_price = 0
                user_quantity = 0

                #search for item
                album_price, album_quantity = searchAlbums(item_to_search)

                # Check if the album exists
                if album_quantity == 0:
                    print("Album not found or sold out.")
                else:
                    user_quantity = int(input("Enter quantity: "))
                    # Check if the quantity does not exceed than inventory
                    if user_quantity >= int(album_quantity):
                        print("Quantity limit exceeded.")
                    else:
                        user_price = user_quantity * int(album_price)
                         #add the item to cart
                        with open ('carts.csv', 'a+', newline='') as user_file:
                            csv_writer = csv.writer(user_file)
                            csv_writer.writerow([user, item_to_search, user_quantity, user_price])
                        print("Album {} added to cart.\n".format(item_to_search))

            except IndexError:
                print("Enter an item.")


        elif command[0] == "rm":
            try:
                item_to_search = command[1]
                rmCart(user, item_to_search)
                print()
            except IndexError:
                print("Enter an item.")
                print()

        elif command[0] == "checkout":
            checkout(user)
            print("Checkout succssfully.")
            print()

        elif command[0] == "edit":
            # search through users.csv for that user
                # once found edit shipping and payment info
            editUser(user)
            print("Edited successfully.")
            print()

        elif command[0] == "delete":
            # search through users.csv for the user
                # remove that user
            # search through carts.csv for the user
                # remove that data
            # search through orders.csv for the user
                #remove that data
            deleteAcc(user)
            print("Account deleted")
            logged_in = False


        elif command[0] == "logout":
            print(user, "logged out successfully.")
            logged_in = False

        else:
            print("Wrong command.")
            userMessage()

    return


# search album info
def searchAlbums(item):
    price = 0
    inventory = 0
    with open("albums.csv") as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            # return the price and inventory when found
            if row[0] == item:
                price = row[3]
                inventory = row[4]

    return price, inventory


# Removes item from cart                
def rmCart(user, item):
    with open('carts.csv') as readFile: # Read the file
        reader = csv.reader(readFile, delimiter=',')
        for row in reader:
            if row[0] == user and row[1] == item: # Display removed message
                print("Album {} removed from cart.".format(item))
            else: # Create a backup file to save the contents without the serched item
                with open('cartsBackup.csv', 'a+', newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    name = row[0]
                    id = row[1]
                    qt = row[2]
                    total = row[3]
                    writer.writerow([name, id, qt, total])
    
    # Remove the old file and rename the new file.
    os.remove('carts.csv')
    os.rename('cartsBackup.csv', 'carts.csv')
            

# Checkout from cart
def checkout(user):
    #search through cart for that user
    #remove from cart
    # edit inventory
    # add to order history
    with open('carts.csv') as readFile: # Read the file
        reader = csv.reader(readFile, delimiter=',')
        for row in reader:
            if row[0] == user: # edit the inventory and add to history
                editInventory(row[1], row[2])
                addHistory(user, row[1], row[2], row[3])
            else: # Create a backup file to save the contents without the serched item
                with open('cartsBackup.csv', 'a+', newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    name = row[0]
                    id = row[1]
                    qt = row[2]
                    total = row[3]
                    writer.writerow([name, id, qt, total])
    
    # Remove the old file and rename the new file.
    os.remove('carts.csv')
    os.rename('cartsBackup.csv', 'carts.csv')

# Edits the inventory based on quantity provided
def editInventory(id, quantity):
    new_quantity = 0
    with open('albums.csv') as rf: # Read the file
        readerf = csv.reader(rf, delimiter=',')
        for r in readerf:
            if r[0] == id: # edit the inventory
                new_quantity = int(r[4]) - int(quantity)
            else:
                new_quantity = r[4]
            # Create a backup file to save the contents without the serched item
            with open('albumsBackup.csv', 'a+', newline='') as writeFile:
                writer = csv.writer(writeFile)
                albumid = r[0]
                name = r[1]
                artist = r[2]
                price = r[3]
                inv = new_quantity
                writer.writerow([albumid, name, artist, price, inv])
    
    # Remove the old file and rename the new file.
    os.remove('albums.csv')
    os.rename('albumsBackup.csv', 'albums.csv')


# Add to order history
def addHistory(user, id, quantity, total):
    now = datetime.now() # get current date and time
    f_now = now.strftime("%Y/%m/%d %H:%M") #formatted date and time
    with open("orders.csv", 'a+', newline='') as f:
        f_writer = csv.writer(f)
        f_writer.writerow([user, id, quantity, total, f_now])


# Edit user info
def editUser(user):
    new_address = ""
    new_card = ""
    with open("users.csv") as rf:
        reader = csv.reader(rf)
        for row in reader:
            if row[0] == user:
                new_address = input("New address: ")
                new_card = input("New card number: ")
            else:
                new_address = row[2]
                new_card = row[3]
            
            with open("usersBackup.csv", 'a+', newline='') as wf:
                writer = csv.writer(wf)
                writer.writerow([row[0], row[1], new_address, new_card])

    # Remove the old file and rename the new file.
    os.remove('users.csv')
    os.rename('usersBackup.csv', 'users.csv')


# Delete all data for that user
def deleteAcc(user):
     # search through users.csv for the user
                # remove that user
    # with open('users.csv', 'r') as inp, open('users_edit.csv', 'w') as out:
    #     writer = csv.writer(out)
    #     for row in csv.reader(inp):
    #         if row[0] != user:
    #             writer.writerow(row)
    #         # search through carts.csv for the user
    #             # remove that data
    
    # with open('carts.csv', 'r') as inp, open('carts_edit.csv', 'w') as out:
    #     writer = csv.writer(out)
    #     for row in csv.reader(inp):
    #         if row[0] != user:
    #             writer.writerow(row)
    #         # search through orders.csv for the user
    #             #remove that data

    # with open('orders.csv', 'r') as inp, open('orders_edit.csv', 'w', newline='') as out:
    #     writer = csv.writer(out)
    #     for row in csv.reader(inp):
    #         if row[0] != user:
    #             writer.writerow(row)

    # os.remove('users.csv')
    # os.remove('carts.csv')
    # os.remove('orders.csv')
    # os.rename('users_edit.csv', 'users.csv')
    # os.rename('carts_edit.csv', 'carts.csv')
    # os.rename('orders_edit.csv', 'orders.csv')

    files = ["orders.csv", "users.csv", "carts.csv"]
    for file in files:
        df = pd.read_csv(file)
        df = df[df.Username != user]
        df.to_csv(file, index=False)