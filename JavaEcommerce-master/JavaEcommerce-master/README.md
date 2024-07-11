# JavaEcommerce
This java console application for E-Commerce has the following sections:

Login - Existing User and Admin

Register - New User

Home - User

View Categories

View products based on category.

Add products to cart.

View Products

Add products to cart.

View Cart

Check out products from cart.

View Order

Logout Home - Admin

View Categories

Add Category

Remove Category

View Products

Add Product

Edit Product

Delete Product

View Orders

Logout

-> Java for coding -> 'CSV' file for storing and retrieving data.

# Files used for each sections:

1."User credential" file for storing user data.

2."Category data" file for storing categories.

3."Product data" file for storing Products.

4."Cart data" file for storing user cart details for each user.

5."Order data" file for storing user order details for each user.

#Applicaption working and steps

# Steps
1.Used MVC (Model, View, Controller) architecture for developing the console application.

2.Added the required Models, Views and Controller along with Interface implementation to achieve abstraction.

3.Added user-defined exceptions to catch anf handle the exceptions.

4.Used encapsulation to hide data and used getter and setter for getting and setting the data for the models.

5.Used "ArrayList" to store and manipulate data according to the user preferrences.

6.Used "CSV" Files for handling data.

7.Stored the file path, Scanner class other sensitive information in a separate Utility folder.

8.Used Singleton pattern to avoid creating objects.

9.Used "Date" class for handling date for orders.

10.Handled exceptions for invalid choices.

# Challenges I faced
1.A problem while trying to update the cart count of a user product in the "CSV File".

2.while updating the cart already existing cart is appended

3.Faced "StackOverFlow" - Caught this while creating parallel objects through constructor. -> Solved it by passing the instance "this" to other constructor.
