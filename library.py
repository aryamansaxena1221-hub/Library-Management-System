from book import Book
from user import User
from notifications import Notifications
from reports import Reports
from datetime import datetime
import json
import os

class Library:
    df = 'library_data.json'

    def __init__(self):
        self.bks = []
        self.usrs = []
        self.load_data()

    def addb(self, bk):
        self.bks.append(bk)

    def addu(self, usr):
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
            print("ID:", usr.user_id, ",Name:", usr.name, ",Role:", usr.role)

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
        sorted_bks = sorted(self.bks, key=lambda b: b.times_borrowed, reverse=True)
        print("Top 5 Popular Books:")
        for bk in sorted_bks[:5]:
            print(bk.title, "- Borrowed", bk.times_borrowed, "times")

    def save_data(self):
        data = {
            "bks": [
                {
                    "book_id": bk.book_id,
                    "title": bk.title,
                    "author": bk.author,
                    "quantity": bk.quantity,
                    "price": bk.price,
                    "mbd": bk.max_borrow_days,
                    "times_borrowed": bk.times_borrowed
                }
                for bk in self.bks
            ],
            "usrs": [
                {
                    "user_id": usr.user_id,
                    "name": usr.name,
                    "role": usr.role,
                    "brw_bks": {
                        str(bid): dd.strftime('%Y-%m-%d')
                        for bid, (bk, dd) in usr.brw_bks.items()
                    }
                }
                for usr in self.usrs
            ]
        }
        with open(self.df, "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        if not os.path.exists(self.df):
            return
        with open(self.df, "r") as f:
            data = json.load(f)
        # Load books
        self.bks = []
        for b in data.get("bks", []):
            bk = Book(
                b["book_id"], b["title"], b["author"],
                b["quantity"], b["price"], b["mbd"]
            )
            bk.times_borrowed = b.get("times_borrowed", 0)
            self.bks.append(bk)
        # Load users
        self.usrs = []
        for u in data.get("usrs", []):
            usr = User(u["user_id"], u["name"], rl=u.get("role", "Member"))
            # Load borrowed books
            for bid, dd_str in u.get("brw_bks", {}).items():
                bk = self.gbi(int(bid))
                if bk:
                    due_dt = datetime.strptime(dd_str, "%Y-%m-%d")
                    usr.brw_bks[bk.book_id] = (bk, due_dt)
            self.usrs.append(usr)

# Sample main function for running the CLI menu
def main():
    lib = Library()
    while True:
        print("\n---- Library Menu ----")
        print("1. Show Books")
        print("2. Show Users")
        print("3. Add Book")
        print("4. Add User")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. View Popular Books")
        print("8. Overdue Report")
        print("9. User Borrow Summary")
        print("10. Save and Exit")

        Notifications.due_date(lib.usrs)

        choice = input("Enter your choice: ")
        if choice == "1":
            lib.showb()
        elif choice == "2":
            lib.showu()
        elif choice == "3":
            # Example: get input and add book
            book_id = int(input("ID: "))
            title = input("Title: ")
            author = input("Author: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            mbd = int(input("Max Borrow Days: "))
            bk = Book(book_id, title, author, quantity, price, mbd)
            lib.addb(bk)
        elif choice == "4":
            user_id = int(input("User ID: "))
            name = input("Name: ")
            role = input("Role (Member/Admin): ")
            usr = User(user_id, name, role)
            lib.addu(usr)
        elif choice == "5":
            uid = int(input("User ID: "))
            bid = int(input("Book ID: "))
            days = int(input("Days to borrow: "))
            usr = lib.gui(uid)
            bk = lib.gbi(bid)
            if usr and bk:
                usr.borrow_book(bk, days)
            else:
                print("Invalid User ID or Book ID.")
        elif choice == "6":
            uid = int(input("User ID: "))
            bid = int(input("Book ID: "))
            usr = lib.gui(uid)
            bk = lib.gbi(bid)
            if usr and bk:
                usr.return_book(bk)
            else:
                print("Invalid User ID or Book ID.")
        elif choice == "7":
            lib.show_pop_bks()
        elif choice == "8":
            Reports.obr(lib.usrs)
        elif choice == "9":
            Reports.ubs(lib.usrs)
        elif choice == "10":
            lib.save_data()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
