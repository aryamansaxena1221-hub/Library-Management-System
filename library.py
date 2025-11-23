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
            for bid, (bk, dd) in usr.brw_bks.items():
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

def main():
    lib = Library()
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
                print(name, "with user ID", new_uid, "added as", role)
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
    main()
