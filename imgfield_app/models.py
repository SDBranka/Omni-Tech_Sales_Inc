from decimal import Decimal
from django.db import models
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
NUMSWDASH_REGEX = re.compile(r'^[0-9-]+$')
PHONENUM_REGEX = re.compile(r'^[0-9-()+]+$')
PRICE_REGEX = re.compile(r'^[0-9]+\.[0-9]+$')
NUMBER_REGEX = re.compile(r'^[0-9]+$')


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

    def email_validator(self, postData):
        errors = {}

        if len(postData['email']) < 2 or not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email"
        email_in_db = self.filter(email = postData['email'])
        if not email_in_db:
            errors['email'] = "This email is not registered"
        return errors

    def edit_profile_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2 or not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Please enter a valid first name"
        if len(postData['last_name']) < 2 or not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Please enter a valid last name"
        if len(postData['email']) < 2 or not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email"
        user = self.get(id=postData['user_id'])
        if user.email != postData['email']:
            email_in_db = self.filter(email = postData['email'])
            if email_in_db:
                errors['email'] = "This email is already registered to another user"
        return errors


class User(models.Model):
    # user_reviews
    # user_orders
    # user_quotes
    # user_contact_infos
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    security_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class ContactInfoManager(models.Manager):
    def new_contact_validator(self, postData):
        errors = {}

        if len(postData['address_1']) < 5:
            errors['address_1'] = "Address 1 must be longer than 5 characters"
        if len(postData['city']) < 2:
            errors['city'] = "City name must be longer than 2 characters"
        if len(postData['zip_code']) < 5 or not NUMSWDASH_REGEX.match(postData['zip_code']):
            errors["zip_code"] = "Please enter a valid zip_code"
        if len(postData['state']) < 1:
            errors['state'] = "Please select your state"
        if len(postData['country']) < 1:
            errors['country'] = "Please select your country"
        if len(postData['phone']) < 10  or not PHONENUM_REGEX.match(postData['phone']):
            errors["phone"] = "Please enter a valid phone in the format ###-###-####"
        return errors


class ContactInfo(models.Model):
    # orders
    # quotes
    user = models.ManyToManyField(
        User,
        related_name="user_contact_infos"
    )
    address_1 = models.CharField(max_length=54)
    address_2 = models.CharField(max_length=54, null=True, blank=True)
    city = models.CharField(max_length=54)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=54)
    country = models.CharField(max_length=54)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContactInfoManager()


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
        if len(postData['price']) < 2 or not PRICE_REGEX.match(postData['price']):
            errors['price'] = "Please enter a valid price in ###.## format"
        if len(postData['desc']) < 10:
            errors["desc"] = "Please enter a valid description"
        if len(postData['quantity_in_stock']) < 1:
            errors["quantity_in_stock"] = "Please enter a valid quantity"
        elif not NUMBER_REGEX.match(postData['quantity_in_stock']):
            errors['quantity_in_stock'] = "Please enter a numeric quantity"
        return errors

    def edit_product_validator(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "Please enter a valid product name"
        if len(postData['part_number']) < 2:
            errors['part_number'] = "Please enter a valid product part number"        
        if len(postData['manufacturer']) < 2:
            errors['manufacturer'] = "Please enter a valid product"      
        if len(postData['price']) < 2 or not PRICE_REGEX.match(postData['price']):
            errors['price'] = "Please enter a valid price in ###.## format"
        if len(postData['desc']) < 10:
            errors["desc"] = "Please enter a valid description"
        if len(postData['quantity_in_stock']) < 1:
            errors["quantity_in_stock"] = "Please enter a valid quantity"
        elif not NUMBER_REGEX.match(postData['quantity_in_stock']):
            errors['quantity_in_stock'] = "Please enter a numeric quantity"
        return errors
        

class Product(models.Model):
    # product_photos
    # product_reviews
    # categories
    # order_of_product
    # quote_of_product
    name = models.CharField(max_length=108)
    part_number = models.CharField(max_length=27)
    manufacturer = models.CharField(max_length=45, null=True, blank= True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    desc = models.CharField(max_length=189)
    exp_desc = models.TextField(null=True, blank=True)
    quantity_in_stock = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()


class EnteredItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}

        if len(postData['name']) < 5:
            errors['name'] = "Please enter a valid product name"
        if len(postData['part_number']) > 0 and len(postData['part_number']) < 3:
            errors['part_number'] = "Please enter a valid product part number"        
        if len(postData['manufacturer']) > 0 and len(postData['manufacturer']) < 3:
            errors['manufacturer'] = "Please enter a valid product"      
        if len(postData['price']) < 2:
            errors['price'] = "Please enter a valid price"
        elif not PRICE_REGEX.match(postData['price']):
            errors['price'] = "Please enter a valid price in ###.## format"
        if len(postData['quantity']) < 1:
            errors['quantity'] = "Please enter a valid quantity"            
        elif not NUMBER_REGEX.match(postData['quantity']):
            errors['quantity'] = "Please enter a numeric quantity"
        return errors


class EnteredItem(models.Model):
    # order_of_items
    # quote_of_items
    name = models.CharField(max_length=108)
    part_number = models.CharField(max_length=27, null=True, blank= True)
    manufacturer = models.CharField(max_length=45, null=True, blank= True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    notes = models.TextField(null=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EnteredItemManager()


class AdminItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}

        if len(postData['name']) < 5:
            errors['name'] = "Please enter a valid product name"
        if len(postData['part_number']) > 0 and len(postData['part_number']) < 3:
            errors['part_number'] = "Please enter a valid product part number"        
        if len(postData['manufacturer']) > 0 and len(postData['manufacturer']) < 3:
            errors['manufacturer'] = "Please enter a valid product"      
        if len(postData['price']) < 1:
            errors['price'] = "Please enter a valid price"
        elif not PRICE_REGEX.match(postData['price']):
            errors['price'] = "Please enter a valid price in ###.## format"
        if len(postData['quantity']) < 1:
            errors['quantity'] = "Please enter a valid quantity"            
        elif not NUMBER_REGEX.match(postData['quantity']):
            errors['quantity'] = "Please enter a numeric quantity"
        return errors


class AdminItem(models.Model):
    # order_of_adminitem
    # quote_of_adminitem
    name = models.CharField(max_length=108)
    part_number = models.CharField(max_length=27, null=True, blank= True)
    manufacturer = models.CharField(max_length=45, null=True, blank= True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    is_discount = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminItemManager()


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


class CategoryManager(models.Manager):
    def category_validator(self, postData):
        errors = {}

        if len(postData['name']) < 3 or len(postData['name']) > 25:
            errors['name'] = "Please enter a valid category name"
        category_in_db = self.filter(name = postData['name'])        #ensure no duplicate category exists
        if category_in_db:
            errors["name"] = "This category already exists in the database"
        return errors


class Category(models.Model):
    product_in_category = models.ManyToManyField(
        Product,
        related_name="categories"
    )
    name = models.CharField(max_length=27)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManager()


class OrderManager(models.Manager):
    def attached_quote_validator(self, postData):
        errors = {}

        if len(postData['ref_number']) < 9:
            errors["ref_number"] = "A reference number must be at least 9 characters long"
        ref_number_in_db = self.filter(ref_number = postData['ref_number'])        #ensure no duplicate ref_number exists
        if ref_number_in_db:
            errors["ref_number"] = "This ref_number already exists in the database. Attached orders should increment by '-1'"
        if len(postData['name']) < 5:
            errors['name'] = "A valid product name should be longer than 5 characters"
        if len(postData['part_number']) > 0 and len(postData['part_number']) < 4:
            errors['part_number'] = "If there is a part number, it should be longer than 4 characters"
        if len(postData['manufacturer']) > 0 and len(postData['manufacturer']) < 3:
            errors['manufacturer'] = "If there is a manufacturer, it should be longer than 3 characters"
        if len(postData['price']) < 2:
            errors['price'] = "Please enter a valid price"
        elif not PRICE_REGEX.match(postData['price']):
            errors['price'] = "Please enter a valid price in ###.## format"
        if len(postData['quantity']) < 1:
            errors['quantity'] = "Please enter a valid quantity"        
        elif not NUMBER_REGEX.match(postData['quantity']):
            errors['quantity'] = "Please enter only digits in quantity"
        return errors

    def ref_number_validator(self, postData):
        errors = {}

        if len(postData['order_ref_num']) < 2:
            errors['ref_number'] = "Please enter a valid product ref_number"
        ref_number_in_db = self.filter(ref_number = postData['order_ref_num'])        #ensure ref_number exists
        if not ref_number_in_db:
            errors["ref_number"] = "This order reference number does not exist in the database"
        return errors


class Order(models.Model):
    # order_product
    # order_item
    # order_adminitem
    # order_contact_info
    ordered_by = models.ForeignKey(
        User, 
        related_name="user_orders",
        on_delete=models.CASCADE
    )
    contact_info =  models.ForeignKey(
        ContactInfo, 
        related_name="orders",
        on_delete = models.CASCADE,
        null=True, blank=True,
    )
    ref_number = models.CharField(max_length=10)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    status = models.CharField(max_length=27)
    # status choices = {open, pending, in process, completed, archived }
    special_instructions = models.TextField(null=True, blank=True)
    office_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()


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
    combined_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
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
    combined_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderAdminItem(models.Model):
    adminitem_on_order = models.ForeignKey(
        AdminItem,
        related_name="order_of_adminitem",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        related_name="order_adminitem",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    combined_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    is_discount = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuoteManager(models.Manager):
    def ref_number_validator(self, postData):
        errors = {}

        if len(postData['quote_ref_num']) < 2:
            errors['ref_number'] = "Please enter a valid product ref_number"
        ref_number_in_db = self.filter(ref_number = postData['quote_ref_num'])        #ensure no duplicate ref_number exists
        if not ref_number_in_db:
            errors["ref_number"] = "This reference number does not exist in the database"
        return errors


class Quote(models.Model):
    # quote_product
    # quote_item
    # quote_adminitem
    quoted_by = models.ForeignKey(
        User, 
        related_name="user_quotes",
        on_delete=models.CASCADE
    )
    contact_info =  models.ForeignKey(
        ContactInfo, 
        related_name="quotes",
        on_delete = models.CASCADE,
        null=True, blank=True,
    )
    ref_number = models.CharField(max_length=10)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    status = models.CharField(max_length=27)
    # status choices = {open, pending, in process, completed, archived }
    special_instructions = models.TextField(null=True, blank=True)
    office_notes = models.TextField(null=True, blank=True)
    placed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

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
    combined_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
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
    combined_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuoteAdminItem(models.Model):
    adminitem_on_quote = models.ForeignKey(
        AdminItem,
        related_name="quote_of_adminitem",
        on_delete=models.CASCADE
    )
    quote = models.ForeignKey(
        Quote,
        related_name="quote_adminitem",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    combined_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    is_discount = models.BooleanField(default=False)
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

