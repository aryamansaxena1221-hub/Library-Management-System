# Here, we are importing datetime module which is a module available in pythoon
from datetime import datetime
# Here, i am creating a notifications class 
class Notifications:
    @staticmethod # this is a static method. Static methods are those which are variables more to class and less to instance
    def due_date(users):
        #here i am defining a function called due_date whose main purpose is to tell how many days remain in the returning of the book
        today = datetime.now()#here, i am defining this function called today which will tell us the newest time 
        for user in users:#here we are starting a loop in users
            for book, due_date in user.brw_bks.values():#another loop so a nested loop
                days_left=(due_date - today).days#we are calculating the difference from the last date to return to today's date 
                if 0<= days_left<= 3:#setting the condition that if due date is more than of 0 or eual to 0 or less then 3 or even equal to 3 then print whatever is below
                    #Printing all the necessary data
                    print("Reminder:", 
                          user.name, "the book", 
                          book.title, "should be submitted in", 
                          days_left, 
                          "day")
