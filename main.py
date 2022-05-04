from functions import login
from functions import userMenu

# Prints message for main menu
def mainMessage():
    print("\n=========== List of commands ==============")
    print("login\t\t-\t Log In User/Create an account")
    print("exit\t\t-\t Exit the program\n")
    print("exit\t\t-\t Exit the program\n")

def main():
    mainMessage()

    # Initialize variables
    logged_in = False
    curr_user = ""

    while not logged_in:
        
        command = input(">> ").lower()
        
        if command == "login":
            logged_in, curr_user = login()
            if logged_in:
                userMenu(curr_user)
                logged_in = False
                mainMessage()
            else:
                mainMessage()
            
        elif command == "exit":
            print("Thanks for using this program.")
            break
        else:
            print("Wrong input.")
            mainMessage()

if __name__ == '__main__':
    main()
