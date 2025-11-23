from datetime import datetime

class Notifications:
    @staticmethod
    def due_date(users):
        today = datetime.now()
        for user in users:
            for book, due_date in user.brw_bks.values():
                days_left=(due_date - today).days
                if 0<= days_left<= 3:
                    print("Reminder:", 
                          user.name, "the book", 
                          book.title, "should be submitted in", 
                          days_left, 
                          "day")
