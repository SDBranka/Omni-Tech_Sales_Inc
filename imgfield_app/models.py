from django.db import models
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# Handles: 123-456-7890, (123) 456-7890, 123 456 7890, 123.456.7890, +91 (123) 456-7890
# (Doesn't Work---> PHONE_REGEX = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$)') 


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2 or not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Please enter a valid first name"
        if len(postData['last_name']) < 2 or not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Please enter a valid last name"
        if len(postData['email']) < 2 or not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email"
        email_in_db = self.filter(email = postData['email'])        #ensure no duplicate email exists
        if email_in_db:
            errors["email"] = "This email already exists in the database"
        if len(postData['password']) < 8:
            errors["password"] = "Please enter a valid password"
        if not postData['password'] == postData['confirm_pw']:
            errors['confirm_pw'] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['lemail']) < 2 or not EMAIL_REGEX.match(postData['lemail']):
            errors["email"] = "Please enter a valid email"
        if len(postData['lpassword']) < 8:
            errors["password"] = "Please enter a valid password"

        email_in_db = self.filter(email = postData['lemail'])
        if not email_in_db:
            errors['email'] = "This email is not registered"
        else:
            user = User.objects.get(email=postData["lemail"])
            pw_to_hash = postData["lpassword"]
            if not bcrypt.checkpw(pw_to_hash.encode(), user.password.encode()):
                errors['email'] = "Incorrect password entered"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    security_level = models.IntegerField()
    # user_reviews
    # user_orders
    # user_quotes
    # user_contact_infos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class ProductManager(models.Manager):
    def new_product_validator(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "Please enter a valid product name"
        item_in_db = self.filter(name = postData['name'])        #ensure no duplicate name exists
        if item_in_db:
            errors["name"] = "This product already exists in the database"
        if len(postData['part_number']) < 2:
            errors['part_number'] = "Please enter a valid product part number"        
        part_number_in_db = self.filter(name = postData['part_number'])        #ensure no duplicate part number exists
        if part_number_in_db:
            errors["part_number"] = "This part number already exists in the database"
        if len(postData['manufacturer']) < 2:
            errors['manufacturer'] = "Please enter a valid product"      
        if len(postData['price']) < 2:
            errors['price'] = "Please enter a valid price"
        if len(postData['desc']) < 10:
            errors["desc"] = "Please enter a valid description"
        if len(postData['quantity_in_stock']) < 1:
            errors["quantity_in_stock"] = "Please enter a valid quantity"
        return errors


class Product(models.Model):
    name = models.CharField(max_length=45)
    part_number = models.CharField(max_length=27)
    manufacturer = models.CharField(max_length=45, null=True, blank= True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    desc = models.CharField(max_length=189)
    exp_desc = models.TextField(null=True, blank=True )
    quantity_in_stock = models.IntegerField()
    # product_photos
    # product_reviews
    # categories
    # order_of_product
    # quote_of_product
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()


class EnteredItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}

        if len(postData['name']) < 5:
            errors['name'] = "Please enter a valid product name"
        if len(postData['part_number']) > 0 and len(postData['part_number']) < 4:
            errors['part_number'] = "Please enter a valid product part number"        
        if len(postData['manufacturer']) > 0 and len(postData['manufacturer']) < 2:
            errors['manufacturer'] = "Please enter a valid product"      
        if len(postData['price']) > 0 and len(postData['price']) < 2:
            errors['price'] = "Please enter a valid price"
        return errors
        
        
class EnteredItem(models.Model):
    name = models.CharField(max_length=100)
    part_number = models.CharField(max_length=27, null=True, blank= True)
    manufacturer = models.CharField(max_length=45, null=True, blank= True)
    price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    notes = models.TextField(null=True, blank= True)
    # order_of_items
    # quote_of_items
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EnteredItemManager()


class Photo(models.Model):
    photo_of = models.ForeignKey(
        Product, 
        related_name="product_photos",
        on_delete = models.CASCADE
    )
    img = models.ImageField(upload_to='product_images', default = "product_images/no_img_available.jpg", null = True, blank = True)
    img_alt = models.CharField(max_length=27, default="no photo available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    product_in_category = models.ManyToManyField(
        Product,
        related_name="categories"
    )
    name = models.CharField(max_length=27)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    # order_product
    # order_item
    # order_contact_info
    ordered_by = models.ForeignKey(
        User, 
        related_name="user_orders",
        on_delete=models.CASCADE
    )
    ref_number = models.CharField(max_length=10)
    total_price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    status = models.CharField(max_length=27)
    # status choices = {open, pending, in process, completed, archived }
    special_instructions = models.TextField(null=True, blank=True)
    office_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    product_on_order = models.ForeignKey(
        Product,
        related_name="order_of_product",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        related_name="order_product",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    combined_price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    item_on_order = models.ForeignKey(
        EnteredItem,
        related_name="order_of_item",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        related_name="order_item",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    combined_price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quote(models.Model):
    # quote_product
    # quote_item
    # quote_contact_info
    quoted_by = models.ForeignKey(
        User, 
        related_name="user_quotes",
        on_delete=models.CASCADE
    )
    ref_number = models.CharField(max_length=10)
    total_price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    status = models.CharField(max_length=27)
    # status choices = {open, pending, in process, completed, archived }
    special_instructions = models.TextField(null=True, blank=True)
    office_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuoteProduct(models.Model):
    product_on_quote = models.ForeignKey(
        Product,
        related_name="quote_of_product",
        on_delete=models.CASCADE
    )
    quote = models.ForeignKey(
        Quote,
        related_name="quote_product",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    combined_price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuoteItem(models.Model):
    item_on_quote = models.ForeignKey(
        EnteredItem,
        related_name="quote_of_item",
        on_delete=models.CASCADE
    )
    quote = models.ForeignKey(
        Quote,
        related_name="quote_item",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    combined_price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ContactInfo(models.Model):
    user = models.ManyToManyField(
        User,
        related_name="user_contact_infos"
    )
    order =  models.ForeignKey(
        Order, 
        related_name="order_contact_info",
        on_delete = models.CASCADE,
        null=True, blank=True,
    )
    quote =  models.ForeignKey(
        Quote, 
        related_name="quote_contact_info",
        on_delete = models.CASCADE,
        null=True, blank=True,
    )
    address_1 = models.CharField(max_length=54)
    address_2 = models.CharField(max_length=54, null=True, blank=True)
    city = models.CharField(max_length=54)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=54)
    country = models.CharField(max_length=54)
    phone = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    product_reviewed = models.ForeignKey(
        Product, 
        related_name="product_reviews",
        on_delete = models.CASCADE
    )
    reviewed_by = models.ForeignKey(
        User, 
        related_name="user_reviews",
        on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

