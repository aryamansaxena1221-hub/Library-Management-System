from datetime import datetime

class Reports:
    @staticmethod
    def obr(users):
        today= datetime.now()
        print("Overdue Books Report")
        overduefound = False
        for user in users:
            for book, duedate in user.brw_bks.values():
                if duedate < today:
                    daysoverdue = (today - duedate).days
                    print("User:", 
                          user.name, 
                          "Book:", 
                          book.title, 
                          "Days Overdue:",
                            daysoverdue)
                    overduefound=True
        if not overduefound:
            print("No overdue books")
    @staticmethod
    def ubs(users):
        print("User Borrow Summary:")
        for user in users:
            count=len(user.brw_bks)
            print(user.name,
                  "has borrowed", 
                  count,
                  "book")