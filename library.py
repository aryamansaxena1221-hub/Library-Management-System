from book import Book
from user import User
from notifications import Notifications
from reports import Reports
from datetime import datetime
import json
import os

class Library:
    df='library_data.json' 

    def __init__(self):
        self.bks = []
        self.usrs = []
        self.load_data()

    def addb(self, 
            bk):
        self.bks.append(bk)

    def addu(self, 
             usr):
        self.usrs.append(usr)

    def showb(self):
        if not self.bks:
            print("No books found.")
            return
        print("Books in Library:")
        for bk in self.bks:
            bk.display()

    def showu(self):
        if not self.usrs:
            print("No users registered.")
            return
        print("Registered Users:")
        for usr in self.usrs:
            print("ID:", usr.user_id, 
                  ",Name:", usr.name, 
                  ",Role:", usr.role)

    def gbi(self, bid):
        for bk in self.bks:
            if bk.book_id == bid:
                return bk
        return None

    def gui(self, uid):
        for usr in self.usrs:
            if usr.user_id == uid:
                return usr
        return None

    def show_pop_bks(self):
        if not self.bks:
            print("No books to show.")
            return
        sorted_bks = sorted(self.bks, 
                            key=lambda b: b.times_borrowed,
                            reverse=True)
        print("Top 5 Popular Books:")
        for bk in sorted_bks[:5]:
            print(bk.title, 
                  "- Borrowed", 
                  bk.times_borrowed, 
                  "times")

    def saved(self):
        data = {'bks': [], 'usrs': []}
        for bk in self.bks:
            data['bks'].append({'book_id': bk.book_id,
                                
                                'title': bk.title,
                                'author': bk.author,
                                'quantity': bk.quantity,
                                'price': bk.price,
                                'mbd': bk.max_borrow_days,
                                'times_borrowed': bk.times_borrowed})
        for usr in self.usrs:
            brw = {}
            for bid, (bk, dd) in usr.borrowed_books.items():
                brw[str(bid)] = dd.strftime('%Y-%m-%d')
            data['usrs'].append({'user_id': usr.user_id,
                                 'name': usr.name,
                                 'role': usr.role,
                                 'borrowed_books': brw})
        try:
            with open(self.df, 'w') as f:
                json.dump(data, f, indent=4)
            print("Data saved.")
        except Exception as e:
            print("Error saving:", e)

    def load_data(self):
        if not os.path.exists(self.df):
            return
        try:
            with open(self.df, 'r') as f:
                data = json.load(f)
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
                usr = User(usrdata['user_id'], 
                           usrdata['name'], 
                           usrdata.get('role', 'Member'))
                for bid_str, dd_str in usrdata.get('borrowed_books', {}).items():
                    bk = self.gbi(int(bid_str))
                    if bk:
                        dd = datetime.strptime(dd_str, '%Y-%m-%d')
                        usr.borrowed_books[bk.book_id] = (bk,dd)
                self.usrs.append(usr)
            print("Data loaded.")
        except Exception as e:
            print("Error loading:",e)

def main():
    lib = Library()

    if not lib.bks:
        lib.addb(Book(1, "Python Crash Course", "E. Matthes", 4, 350, 14))
        lib.addb(Book(2, "1984", "George Orwell", 2, 250, 10))
        lib.addb(Book(3, "To Kill a Mockingbird", "Harper Lee", 5, 300, 12))
        lib.addb(Book(4, "Pride and Prejudice", "Jane Austen", 3, 280, 15))
        lib.addb(Book(5, "The Great Gatsby", "F. Scott Fitzgerald", 6, 320, 10))
        lib.addb(Book(6, "Moby Dick", "Herman Melville", 2, 400, 14))
        lib.addb(Book(7, "War and Peace", "Leo Tolstoy", 1, 500, 20))
        lib.addb(Book(8, "The Catcher in the Rye", "J.D. Salinger", 7, 270, 12))
        lib.addb(Book(9, "The Hobbit", "J.R.R. Tolkien", 10, 350, 14))
        lib.addb(Book(10, "Fahrenheit 451", "Ray Bradbury", 4, 300, 10))
        lib.addb(Book(11, "Brave New World", "Aldous Huxley", 4, 330, 14))
        lib.addb(Book(12, "The Odyssey", "Homer", 3, 370, 20))
        lib.addb(Book(13, "Crime and Punishment", "Fyodor Dostoevsky", 2, 450, 20))
        lib.addb(Book(14, "Jane Eyre", "Charlotte Brontë", 5, 310, 15))
        lib.addb(Book(15, "The Divine Comedy", "Dante Alighieri", 1, 550, 25))
        lib.addb(Book(16, "The Brothers Karamazov", "Fyodor Dostoevsky", 2, 480, 20))
        lib.addb(Book(17, "Les Misérables", "Victor Hugo", 3, 420, 20))
        lib.addb(Book(18, "Dracula", "Bram Stoker", 6, 295, 12))
        lib.addb(Book(19, "The Iliad", "Homer", 3, 380, 20))
        lib.addb(Book(20, "The Grapes of Wrath", "John Steinbeck", 4, 310, 15))

    if not lib.usrs:
        lib.addu(User(100, "Alice", role="Member"))
        lib.addu(User(200, "Bob", role="Admin"))

    while True:
        Notifications.due_date(lib.usrs)

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

        choice = input("Choose option: ")

        if choice == '1':
            lib.showb()

        elif choice == '2':
            try:
                uid = int(input("User ID: "))
                bid = int(input("Book ID: "))
                days = int(input("Days to borrow: "))
            except ValueError:
                print("Please enter valid number")
                continue
            usr = lib.gui(uid)
            bk = lib.gbi(bid)
            if usr and bk:
                usr.borrow_book(bk, days)
            else:
                print("User or book not found")

        elif choice == '3':
            try:
                uid = int(input("User ID: "))
                bid = int(input("Book ID: "))
            except ValueError:
                print("Please enter valid number")
                continue
            usr = lib.gui(uid)
            bk = lib.gbi(bid)
            if usr and bk:
                usr.return_book(bk)
            else:
                print("User or book not found")

        elif choice == '4':
            try:
                uid = int(input("User ID: "))
            except ValueError:
                print("Invalid ID")
                continue
            usr = lib.gui(uid)
            if usr:
                usr.view_borrowed_books()
            else:
                print("User not found")

        elif choice == '5':
            lib.show_pop_bks()

        elif choice == '6':
            Reports.obr(lib.usrs)

        elif choice == '7':
            Reports.ubs(lib.usrs)

        elif choice == '8':
            try:
                new_uid = int(input("New user ID: "))
                if lib.gui(new_uid):
                    print("User ID taken")
                    continue
                name = input("Name: ")
                role = input("Role (Admin/Member): ")
                if role not in ("Admin", "Member"):
                    role = "Member"
                lib.addu(User(new_uid, name, role))
                print(name, 
                      "with user ID", 
                      new_uid, 
                      "has been successfully added and your role is", 
                      role)
            except ValueError:
                print("Invalid input")

        elif choice == '9':
            lib.showu()

        elif choice == '10':
            lib.saved()
            print("Data is saved")
            break

        else:
            print("Only choose between 1 to 10")

if __name__ == "__main__":
    from notifications import Notifications
    from reports import Reports
    main()
