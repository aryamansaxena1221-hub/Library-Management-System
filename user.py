from datetime import datetime, timedelta
class User:
    def __init__(self, uid, nm, rl='Member'):
        self.user_id = uid
        self.name = nm
        self.role = rl
        self.brw_bks = {}
    def borrow_book(self, bk, days):
        if self.role != 'Member':
            print(self.name,
                  "cannot borrow books")
            return
        if bk.available():
            if days>bk.max_borrow_days:
                print("Cannot borrow for more than",
                      bk.max_borrow_days,
                      "days")
                return
            if bk.book_id in self.brw_bks:
                print(self.name, "already borrowed '",bk.title)
                return
            due_dt=datetime.now()+timedelta(days=days)
            self.brw_bks[bk.book_id]=(bk,due_dt)
            bk.mquantity(-1)
            bk.ibc()
            print(self.name, 
                  "borrowed", 
                  bk.title, 
                  "for", 
                  days, 
                  "days, due on", 
                  due_dt.strftime('%Y-%m-%d'))
        else:
            print("Book",bk.title,"not available")
    def return_book(self, bk):
        if bk.book_id in self.brw_bks:
            del self.brw_bks[bk.book_id]
            bk.mquantity(1)
            print(self.name,"returned",bk.title)
        else:
            print(self.name,"does not have", bk.title,"borrowed")
    def view_borrowed_books(self):
        if not self.brw_bks:
            print(self.name,"has no borrowed books")
            return
        print(self.name+" Borrowed Books:")
        now = datetime.now()
        for bk, due_dt in self.brw_bks.values():
            days_left = (due_dt-now).days
            print("Title:", 
                  bk.title + 
                  ", Due in", 
                  days_left, 
                  "day on", 
                  due_dt.strftime('%Y-%m-%d'))
