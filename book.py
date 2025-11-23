class Book:
    def __init__(self, 
                book_id, 
                title, 
                author, 
                quantity, 
                price, 
                max_borrow_days):
        self.book_id=book_id
        self.title=title
        self.author=author
        self.quantity=quantity
        self.price=price
        self.max_borrow_days=max_borrow_days
        self.times_borrowed=0

    def display(self):
        print("ID:", self.book_id, ", Title:", self.title, ", Author:", self.author,
              ", Quantity:", self.quantity, ", Price:", self.price,
              ", Max Borrow:", self.max_borrow_days, "days")

    def available(self):
        return self.quantity>0

    def mquantity(self, n):
        self.quantity+=n

    def ibc(self):
        self.times_borrowed+=1
