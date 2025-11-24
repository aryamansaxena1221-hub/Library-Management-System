#here i am importing book class entire data from book.py
from book import Book
#similarily i am importing user class data from user.py
from user import User
#doing the same by importing notifications from notifications.py
from notifications import Notifications
# and the same for reports
from reports import Reports
#now importing datetime module
from datetime import datetime
#and also importing json module 
import json
#and also importing os module
import os

#Now i am creating a library class
class Library:
    df = 'library_data.json'#creating this file to save data later 

    def __init__(self):#initializing the value of the library class 
        self.bks = []#here we are creating a list which is empty and we will use to store books
        self.usrs = []#here we are creating a list which is empty and we will use it store user data
        self.load_data()#we use this method to get any data which we have

    def addb(self, bk):#we are adding books by using this method
        self.bks.append(bk)#it will append that book in the list

    def addu(self, usr):#we are using it to add a new user
        self.usrs.append(usr)#we will append it in the list 

    def showb(self):#defining this method to show the books
        if not self.bks:#if a book is not in the list then print that no book is found
            print("No books found.")
            return
        print("Books in Library:")#otherwise print that books are in library
        for bk in self.bks:
            bk.display()#display entire information of the books

    def showu(self):# it shows the list of all the users
        if not self.usrs:#if somebody is not registered then print that the user is not registered 
            print("No users registered.")
            return
        print("Registered Users:")#otherwise print that the user is registered 
        for usr in self.usrs:#using loops
            print("ID:", usr.user_id, ",Name:", usr.name, ",Role:", usr.role)#now print the entire information of teh user

    def gbi(self, bid):#here we are finding by it's id
        for bk in self.bks:#using loop to check every book
            if bk.book_id == bid:#if the id is mathced 
                return bk
        return None#then return the book otherwise not 

    def gui(self, uid):#now doing the same thing for the user.
        for usr in self.usrs:#the loop will check if the user is present in the user list
            if usr.user_id == uid:#if id matched then return the user otherwise return none
                return usr
        return None

    def show_pop_bks(self):#this method is used to display popular books
        if not self.bks:#it is used to check whether the book list is empty or not 
            print("No books to show.")
            return
        sorted_bks = sorted(self.bks, key=lambda b: b.times_borrowed, reverse=True)#otherwise sort the list based on how many times the book has been borrowed 
        print("Top 5 Popular Books:")
        for bk in sorted_bks[:5]:
            print(bk.title, "- Borrowed", bk.times_borrowed, "times")#and then print till 0 to 4th index so basically top 5

    def saved(self):
        #we will now save the data
        data = {'bks': [], 'usrs': []}#we are creating a dictionary to set the data in the json file
        for bk in self.bks:#creating a loop for all books objects 
            data['bks'].append({'book_id': bk.book_id,
                                'title': bk.title,
                                'author': bk.author,
                                'quantity': bk.quantity,
                                'price': bk.price,
                                'mbd': bk.max_borrow_days,
                                'times_borrowed': bk.times_borrowed})
        for usr in self.usrs:#creating a loop for all the users.
            brw = {}
            for bid, (bk, dd) in usr.brw_bks.items():
                brw[str(bid)] = dd.strftime('%Y-%m-%d')
            data['usrs'].append({'user_id': usr.user_id,
                                 'name': usr.name,
                                 'role': usr.role,
                                 'borrowed_books': brw})
        try:#using try and except for error handling 
            with open(self.df, 'w') as f:
                json.dump(data, f, indent=4)
            print("Data saved.")#the data is saved 
        except Exception as e:
            print("Error saving:", e)

    def load_data(self):
        if not os.path.exists(self.df):#if the path of the does not exists then exit
            return
        try:
            with open(self.df, 'r') as f:#otherwise open it in read mode as f 
                data = json.load(f)#and load it 
            self.bks = []
            for bkdata in data.get('bks', []):
                bk = Book(
                    bkdata['book_id'],
                    bkdata['title'],
                    bkdata['author'],
                    bkdata['quantity'],
                    bkdata['price'],
                    bkdata['mbd']
                )
                bk.times_borrowed = bkdata.get('times_borrowed', 0)
                self.bks.append(bk)
            self.usrs = []
            for usrdata in data.get('usrs', []):
                usr = User(
                    usrdata['user_id'],
                    usrdata['name'],
                    usrdata.get('role', 'Member'))
                # Assign borrowed books
                for bid_str, dd_str in usrdata.get('borrowed_books', {}).items():
                    bk = self.gbi(int(bid_str))
                    if bk:
                        dd = datetime.strptime(dd_str, '%Y-%m-%d')
                        usr.brw_bks[bk.book_id] = (bk, dd)
                self.usrs.append(usr)
            print("Data loaded.")
        except Exception as e:
            print("Error loading:", e)

def main():#now definining the main function 
    lib = Library()#creating lib as the object 
    while True:
        #running an infinite loop
        Notifications.due_date(lib.usrs)#addinig data of due date from notifications 
        print("Library Menu")
        print("1. Show books")
        print("2. Borrow book")
        print("3. Return book")
        print("4. View borrowed")
        print("5. Popular books")
        print("6. Overdue books report")
        print("7. User borrow summary")
        print("8. Add user")
        print("9. Show users")
        print("10. Save & exit")
        #these are all the options present 
        choice = input("Choose option: ")
        if choice == '1':#if options 1 is choosed then print all the available books 
            lib.showb()
        elif choice == '2':#if 2nd choice is taken 
            try:
                uid = int(input("User ID: "))#then ask the user id, the book id and how many days u want to borrow 
                bid = int(input("Book ID: "))
                days = int(input("Days to borrow: "))
            except ValueError:
                print("Please enter valid number")#for error handling if a valid number is not entered 
                continue
            usr = lib.gui(uid)#check the user by his id
            bk = lib.gbi(bid)#check the boook by the id 
            if usr and bk:# if they exist then the boook is borrowed 
                usr.borrow_book(bk, days)
            else:
                print("User or book not found")#otherwise print the error message 
        elif choice == '3':
            try:
                uid = int(input("User ID: "))#enter the id and book id 
                bid = int(input("Book ID: "))
            except ValueError:
                print("Please enter valid number")#once again message for error
                continue
            usr = lib.gui(uid)#check user id and book id 
            bk = lib.gbi(bid)
            if usr and bk:
                usr.return_book(bk)#if both correct then the return book
            else:
                print("User or book not found")
        elif choice == '4':
            try:
                uid = int(input("User ID: "))#ask user id 
            except ValueError:
                print("Invalid ID")#otherwise print error statement 
                continue
            usr = lib.gui(uid)#check his id 
            if usr:
                usr.view_borrowed_books()#display the borrowed books list 
            else:
                print("User not found")
        elif choice == '5':
            lib.show_pop_bks()#then to show popular books which are top 5
        elif choice == '6':
            Reports.obr(lib.usrs)#then to show overdue books reports click 6 
        elif choice == '7':
            Reports.ubs(lib.usrs)# click 7 for checking borrow summary of user
        elif choice == '8':
            try:
                new_uid = int(input("New user ID: "))#entering new user id 
                if lib.gui(new_uid):
                    print("User ID taken")#if id already there 
                    continue
                name = input("Name: ")#otherwise enter name
                role = input("Role (Admin/Member): ")#enter your role also
                if role not in ("Admin", "Member"):
                    role = "Member"#i am setting default role as member 
                lib.addu(User(new_uid, name, role))#add this data is addu mmethod 
                print(name, "with user ID", new_uid, "added as", role)#print the required information 
            except ValueError:
                print("Invalid input")#otherwise print invalid input 
        elif choice == '9':
            lib.showu()#show the list of all the users
        elif choice == '10':
            lib.saved()
            print("Data is saved")#and save the data 
            break
        else:
            print("Only choose between 1 to 10")# error message if somebody uses other option 

if __name__ == "__main__":
    main()
