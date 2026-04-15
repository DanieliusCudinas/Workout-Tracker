class Product:

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Price cannot be less than 0 or equal to 0")
        self._price = value

    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("Stock cannot be less than 0")
        self._stock = value

    def get_total_price(self, quantity):
        return self.price * quantity
    
    def display_info(self):
        print(f"Name: {self.name} | Price: {self.price} | Stock: {self.stock}")




class Book (Product):

    def __init__(self, name, price, stock, author):
        super().__init__(name, price, stock)
        self.author = author

    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        if not value:
            raise ValueError("Authors name cannot be empty")
        self._author = value

    def get_total_price(self, quantity):
        if quantity >= 3:
            return self.price * quantity * 0.9
        else:
            return self.price * quantity
        
    def display_info(self):
        print(f"Name: {self.name}, Author: {self.author} | Price: {self.price} | Stock: {self.stock}")




class Electronic (Product):

    def __init__(self, name, price, stock, warranty_years):
        super().__init__(name, price, stock)
        self.warranty_years = warranty_years

    @property
    def warranty_years(self):
        return self._warranty_years
    
    @warranty_years.setter
    def warranty_years(self, value):
        if value <= 0:
            raise ValueError("Warranty cannot be less than 1 year")
        self._warranty_years = value

    def get_total_price(self, quantity):
        return (self.price + self._warranty_years * 10) * quantity
    
    def display_info(self):
        print(f"Name: {self.name}| Warranty Years: {self.warranty_years} | Price: {self.price} | Stock: {self.stock}")




class CartItem:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        return self.product.get_total_price(self.quantity)




class ShoppingCart:

    def __init__(self, items = None):
        self._items = items if items is not None else []
    
    def add_product(self, product, quantity):
        item = CartItem(product, quantity)
        self._items.append(item)

    def remove_product(self, product_name):
        for item in self._items:
            if item.product.name != product_name:
                self._items = item

    def get_total(self):
        total = 0
        for item in self._items:
            total += item.get_subtotal()
        return total
    
    def display_cart(self):
        for item in self._items:
            print(f"{item.product.name} | Quantity: {item.quantity} | Subtotal: {item.get_subtotal()} €")
        print(f"Total: {self.get_total()} €")




class Customer:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self._cart = ShoppingCart()
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self):
        return self._email
    
    @name.setter
    def email(self, value):
        if not value:
            raise ValueError("Email cannot be empty")
        self._email = value

    def shop(self, product, quantity):
        self._cart.add_product(product, quantity)
    
    def view_cart(self):
        self._cart.display_cart()
    
    def checkout(self):
        total = self._cart.get_total()
        print(f"Total to pay: {total} €")
        self._cart = ShoppingCart()



# Create products 
book1 = Book("Python Guide", 30, 10, "Smith") 
laptop = Electronic("Dell Laptop", 800, 5, 2)

# Create customer (composition: customer owns cart) 
customer = Customer("Anna", "anna@email.com")
                    
# Shopping (aggregation: cart references products, doesn't own them)
customer.shop(book1, 2) 
customer.shop(laptop, 1) 
customer.view_cart() 
total = customer.checkout()

# Products still exist after checkout (aggregation) 
print(book1._name)  # Still accessible 
# But cart items are gone (composition) 
customer.view_cart()  # Empty cart 