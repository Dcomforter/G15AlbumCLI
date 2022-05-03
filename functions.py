import csv # For reading and writing into csv files
import hashlib # For hashing passwords
import pandas as pd # For deleting rows easily

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

        # Save user info in the file
        with open ('users.csv', 'a+', newline='') as user_file:
            csv_writer = csv.writer(user_file)
            csv_writer.writerow([name, pass_hash])
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
        command = in_command.split() # Parse the input

        # Process the input 
        if command[0] == "view":
            try:
                if command[1] == "all":
                    # Print all info from albums.csv
                    with open("albums.csv") as f:
                        csv_f = csv.reader(f)
                        for row in csv_f:
                            print('{:<15} {:<15} {:<20} {:<25}'.format(*row))
                    
                   
                elif command[1] == "cart":
                    #search for the username in carts.csv
                    with open("carts.csv") as f:
                        csv_f = csv.reader(f)
                        for row in csv_f:
                            #print the orders once found
                            if row[0] == user:
                                print('{:<10} {:<10} {:<10} {:<10}'.format(*row))
                        
                    
                elif command[1] == "history":
                    #search for the username in orders.csv
                    searchRow(user, "orders.csv")
                        #print the orders once found
                    # for row in result:
                    #     print(row)
                    print("view history working")
                else:
                    raise IndexError
            except IndexError:
                print("Wrong input")
                userMessage()

        elif command[0] == "add":
            item_to_search = command[1]
            #search for item
            #add the item to cart
            print("add", item_to_search, "working")

        elif command[0] == "rm":
            item_to_search = command[1]
            #search for item
            #remove the item from cart
            print("rm", item_to_search, "working")

        elif command[0] == "checkout":
            #search through cart for that user
                #remove from cart
                #edit inventory
                # add to order history
            print("checkout working")

        elif command[0] == "edit":
            # search through users.csv for that user
                # once found edit shipping and payment info
            print("edit working")

        elif command[0] == "delete":
            # search through users.csv for the user
                # remove that user
            # search through carts.csv for the user
                # remove that data
            # search through orders.csv for the user
                #remove that data
            print("delete working")


        # logout does not logout successfully when running other commands
        elif command[0] == "logout":
            print(user, "logged out successfully.")
            logged_in = False

        else:
            print("Wrong command.")
            userMessage()

    return


# def searchRow(user, filename):
#     # value = []
#     with open(filename) as f:
#         csv_f = csv.reader(f)
#         for row in csv_f:
#             #print the orders once found
#             if row[0] == user:
#                 # print[row]
#     return
                

def searchRow(user, filename):
    df = pd.read_csv(filename)
    for i in range(len(df)):
        if df["Username"][i] == user:
            print(df.columns)
            print("\n")

    