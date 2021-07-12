from decimal import Decimal
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from imgfield_app.models import ContactInfo, User, Product, AdminItem, Photo, Quote, QuoteProduct, QuoteItem, QuoteAdminItem, Order, OrderProduct, OrderItem, OrderAdminItem, Category
from django.contrib import messages
from decimal import Decimal


def index(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
        # status choices = {open, pending, in process, completed, archived }
            context = {
                'logged_user' : logged_user,
                'all_products': Product.objects.all(),
                'new_quotes': Quote.objects.filter(status="pending"),
                'quote_in_process_count': Quote.objects.filter(status="in process").count(),
                'order_open_count': Order.objects.filter(status="open").count(),
                'order_pending_count': Order.objects.filter(status="pending").count(),
                'order_in_process_count': Order.objects.filter(status="in process").count(),
            }
            return render(request, "admin_index.html", context)
    return redirect("/")


def process_create_product(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                errors = Product.objects.new_item_validator(request.POST)
                if len(errors) > 0:
                    for error in errors.values():
                        messages.error(request, error)
                    return redirect("/admin_access/administrative")

                new_prod = Product.objects.create(
                    name = request.POST['name'],
                    part_number = request.POST['part_number'],
                    manufacturer = request.POST['manufacturer'],
                    price = Decimal(request.POST['price']),
                    desc = request.POST['desc'],
                    exp_desc = request.POST['exp_desc'],
                    quantity_in_stock = int(request.POST['quantity_in_stock'])
                )
                Photo.objects.create(
                    photo_of = new_prod,
                )
            return redirect("/admin_access/administrative")
    return redirect("/")


def select_product(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            context = {
                'logged_user' : logged_user,
                'all_products': Product.objects.all(),
            }
            return render(request, "select_product.html", context)
    return redirect("/")


def edit_product(request, product_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            context = {
                'logged_user': logged_user,
                'product_to_edit': Product.objects.get(id=product_id),
            }
            return render(request, "edit_product.html", context)        
    return redirect("/")


def process_product_edit(request, product_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            product_to_edit = Product.objects.get(id=product_id)
            if request.method == "POST":
                # errors handling
                errors = Product.objects.edit_product_validator(request.POST)
                if len(errors) > 0:
                    for error in errors.values():
                        messages.error(request, error)
                else:
                    product_to_edit.name = request.POST['name']
                    product_to_edit.part_number = request.POST['part_number']
                    product_to_edit.manufacturer = request.POST['manufacturer']
                    product_to_edit.price = Decimal(request.POST['price'])
                    product_to_edit.desc = request.POST['desc']
                    product_to_edit.exp_desc = request.POST['exp_desc']                
                    product_to_edit.quantity_in_stock = int(request.POST['quantity_in_stock'])        
                    product_to_edit.save()
            return redirect(f"/admin_access/edit_product/{ product_id }")
    return redirect("/")

def delete_product(request, product_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            product_to_delete = Product.objects.get(id=product_id)
            product_to_delete.delete()
            return redirect("/admin_access/select_product")
    return redirect("/")


def edit_product_img(request, product_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            product = Product.objects.get(id=product_id)
            context = {
                'logged_user': logged_user,
                'product': product,
                'all_product_categories': product.categories.all()
            }
            return render(request, "edit_product_img.html", context)
    return redirect("/")


def process_add_prod_photo(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                # errors handling
                # errors = Wish.objects.wish_validator(request.POST)
                # if len(errors) > 0:
                #     for error in errors.values():
                #         messages.error(request, error)
                #     return redirect(f"/wishes/edit_wish/{ wish_id }")
                # else:
                

                product = Product.objects.get(id=request.POST['product_id'])
                Photo.objects.create(
                    photo_of = product,
                    img = request.FILES['img'],
                    img_alt = request.POST['img_alt']
                )
                return redirect(f"/admin_access/edit_product_img/{ product.id }")
            return redirect("/admin_access")
    return redirect("/")


def delete_photo(request, photo_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            photo_to_delete = Photo.objects.get(id=photo_id)
            photo_to_delete.delete()
            return redirect(f"/admin_access/edit_product_img/{ photo_to_delete.photo_of.id }")
    return redirect("/")


def administrative(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            context = {
                'logged_user': logged_user
            }
            return render(request, "administrative.html", context)
    return redirect("/")


def edit_user(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            context = {
                'logged_user' : logged_user,
                'all_users': User.objects.all(),
            }
            return render(request, "edit_user.html", context)
    return redirect("/")


def edit_user_security(request, user_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            context = {
                'logged_user' : logged_user,
                'user_to_edit': User.objects.get(id=user_id),
            }
            return render(request, "edit_user_security.html", context)
    return redirect("/")


def process_edit_security(request, user_to_edit_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                user_to_edit = User.objects.get(id=user_to_edit_id)
                user_to_edit.security_level = request.POST['security_level']
                user_to_edit.save()
            return redirect("/admin_access/edit_user")
    return redirect("/")


def delete_user(request, user_id):
    if'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            user_to_delete = User.objects.get(id=user_id)
            user_to_delete.delete()
            return redirect("/admin_access/edit_user")
    return redirect("/")


def process_add_category(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                # errors = Product.objects.new_item_validator(request.POST)
                # if len(errors) > 0:
                #     for error in errors.values():
                #         messages.error(request, error)
                #     return redirect("/admin_access/create_product")

                Category.objects.create(
                    name = request.POST['name'],
                )
        return redirect("/admin_access/administrative")
    return redirect("/")


def edit_product_category(request, product_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            product = Product.objects.get(id=product_id)
            context = {
                'logged_user' : logged_user,
                'product': product,
                'all_categories': Category.objects.exclude(product_in_category = product ),
                'all_product_categories': product.categories.all() 
            }
            return render(request, "edit_product_category.html", context)
    return redirect("/")


def process_add_product_to_category(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            product = Product.objects.get(id=request.POST['product_id'])
            if request.method == "POST":
                # errors = Product.objects.new_item_validator(request.POST)
                # if len(errors) > 0:
                #     for error in errors.values():
                #         messages.error(request, error)
                #     return redirect("/admin_access/create_product")

                category = Category.objects.get(id=request.POST['category_id'])
                category.product_in_category.add(product)
            return redirect(f"/admin_access/edit_product_category/{ product.id }")
    return redirect("/")


def process_remove_product_to_category(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            product = Product.objects.get(id=request.POST['product_id'])
            if request.method == "POST":
                # errors handling
                # errors = Wish.objects.wish_validator(request.POST)
                # if len(errors) > 0:
                #     for error in errors.values():
                #         messages.error(request, error)
                #     return redirect(f"/wishes/edit_wish/{ wish_id }")
                # else:

                category = Category.objects.get(id=request.POST['category_id'])
                category.product_in_category.remove(product)
            return redirect(f"/admin_access/edit_product_category/{ product.id }")
    return redirect("/")


def view_quote(request, quote_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            quote = Quote.objects.get(id=quote_id)
            all_quoteproducts = QuoteProduct.objects.filter(quote=quote)
            all_quoteitems = QuoteItem.objects.filter(quote=quote)        
            all_quote_adminitems = QuoteAdminItem.objects.filter(quote=quote)


            context = {
                'logged_user': logged_user,
                'quote': quote,
                'products': all_quoteproducts,
                'items': all_quoteitems,
                'adminitems': all_quote_adminitems,
            }
            return render(request, "admin_view_quote.html", context)
    return redirect("/")


def view_order(request, order_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            order = Order.objects.get(id=order_id)
            all_orderproducts = OrderProduct.objects.filter(order=order)
            all_orderitems = OrderItem.objects.filter(order=order)
            all_order_adminitems = OrderAdminItem.objects.filter(order=order)

            context = {
                'logged_user': logged_user,
                'order': order,
                'products': all_orderproducts,
                'items': all_orderitems,
                'adminitems': all_order_adminitems,
            }
            return render(request, "admin_view_order.html", context)
    return redirect("/")


def edit_off_notes(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                quote = Quote.objects.get(id=request.POST['quote_id'])
                quote.office_notes = request.POST['office_notes']
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote.id }")
    return redirect("/")


def begin_processing_quote(request):
    if 'user_id' in request.session:
        print("###begin_processing_quote1")
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            print("###begin_processing_quote2")
            if request.method == "POST":
                print("###begin_processing_quote3")
                quote_id = request.POST['quote_id']
                quote = Quote.objects.get(id=quote_id)
                quote.status = "in process"
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote_id }")
        return redirect("/admin_access")
    return redirect("/")

def order_quote(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                quote = Quote.objects.get(id=request.POST['quote_id'])
                quote.status = "completed"
                quote.save()

                new_order = Order.objects.create(
                    ordered_by = quote.quoted_by,
                    contact_info = quote.contact_info,
                    ref_number = quote.ref_number,
                    total_price = 0,
                    status = "pending",
                    special_instructions = quote.special_instructions,
                    office_notes = quote.office_notes,
                )

                for product in quote.quote_product.all():
                    new_orderproduct = OrderProduct.objects.create(
                        product_on_order = product.product_on_quote,
                        order = new_order,
                        quantity = product.quantity,
                        combined_price = product.combined_price                        
                    )
                    new_order.total_price += new_orderproduct.combined_price
                    new_order.save()
                for item in quote.quote_item.all():
                    new_orderitem = OrderItem.objects.create(
                        item_on_order = item.item_on_quote,
                        order = new_order,
                        quantity = item.quantity,
                        combined_price = item.combined_price                        
                    )
                    new_order.total_price += new_orderitem.combined_price
                    new_order.save()
                for adminitem in quote.quote_adminitem.all():
                    new_orderadminitem = OrderAdminItem.objects.create(
                        adminitem_on_order = adminitem.adminitem_on_quote,
                        order = new_order,
                        quantity = adminitem.quantity,
                        combined_price = adminitem.combined_price,                        
                        is_discount = adminitem.is_discount,
                    )

                    if adminitem.is_discount:
                        new_order.total_price -= new_orderitem.combined_price
                    else:
                        new_order.total_price += new_orderitem.combined_price
                    new_order.save()
######Consider different redirect after changing quote to order
                return redirect("/admin_access/")
        return redirect("/admin_access")
    return redirect("/")


def quotes_display(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
        # status choices = {open, pending, in process, completed, archived }
            all_active_quotes= Quote.objects.exclude(status = "archived").order_by('-placed_at')

            context = {
                'logged_user': logged_user,
                'all_active_quotes': all_active_quotes
            }
        return render(request, "quotes_display.html", context)
    return redirect("/")


def orders_display(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
        # status choices = {pending, in process, completed, archived }
            all_active_orders= Order.objects.exclude(status = "archived").order_by('-created_at')
            context = {
                'logged_user': logged_user,
                'all_active_orders': all_active_orders
            }
        return render(request, "orders_display.html", context)
    return redirect("/")


def confirm_delete_quote(request, quote_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            context = {
                'logged_user': logged_user,
                'quote': Quote.objects.get(id=quote_id),
            }
            return render(request, "confirm_delete_quote.html", context)
    return redirect("/")


def delete_quote(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                quote = Quote.objects.get(id=request.POST['quote_id'])
                quote.delete()
        return redirect("/admin_access")        
    return redirect("/")


def find_quote(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                quote_ref_num = request.POST['quote_ref_num']
#add validation here in case ref number doesn't exist

                quote = Quote.objects.get(ref_number=quote_ref_num)
                return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")        
    return redirect("/")

def find_order(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":
                order_ref_num = request.POST['order_ref_num']
#add validation here in case ref number doesn't exist
                order = Order.objects.get(ref_number=order_ref_num)
                return redirect(f"/admin_access/view_order/{ order.id }")
            return redirect("/admin_access")        
    return redirect("/")

def increase_product_quantity(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                product_to_increase = QuoteProduct.objects.get(id=request.POST['product_id'])
                product_to_increase.quantity += 1 
                product_to_increase.combined_price += product_to_increase.product_on_quote.price
                product_to_increase.save() 

                quote = Quote.objects.get(id=request.POST['quote_id'])
                quote.total_price += product_to_increase.product_on_quote.price
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")

def decrease_product_quantity(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                product_to_decrease = QuoteProduct.objects.get(id=request.POST['product_id'])
                if product_to_decrease.quantity > 1:
                    product_to_decrease.quantity -= 1
                    product_to_decrease.combined_price -= product_to_decrease.product_on_quote.price
                    product_to_decrease.save() 

                    quote = Quote.objects.get(id=request.POST['quote_id'])
                    quote.total_price -= product_to_decrease.product_on_quote.price
                    quote.save()
                    return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")

def increase_item_quantity(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                item_to_increase = QuoteItem.objects.get(id=request.POST['item_id'])
                item_to_increase.quantity += 1 
                item_to_increase.combined_price += item_to_increase.item_on_quote.price
                item_to_increase.save() 

                quote = Quote.objects.get(id=request.POST['quote_id'])
                quote.total_price += item_to_increase.item_on_quote.price
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")

def decrease_item_quantity(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                item_to_decrease = QuoteItem.objects.get(id=request.POST['item_id'])
                if item_to_decrease.quantity > 1:
                    item_to_decrease.quantity -= 1
                    item_to_decrease.combined_price -= item_to_decrease.item_on_quote.price
                    item_to_decrease.save() 

                    quote = Quote.objects.get(id=request.POST['quote_id'])
                    quote.total_price -= item_to_decrease.item_on_quote.price
                    quote.save()
                    return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")


def increase_adminitem_quantity(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                adminitem_to_increase = QuoteAdminItem.objects.get(id=request.POST['adminitem_id'])
                adminitem_to_increase.quantity += 1 
                adminitem_to_increase.combined_price += adminitem_to_increase.adminitem_on_quote.price
                adminitem_to_increase.save() 

                quote = Quote.objects.get(id=request.POST['quote_id'])
                if adminitem_to_increase.is_discount:
                    quote.total_price -= adminitem_to_increase.adminitem_on_quote.price
                else:
                    quote.total_price += adminitem_to_increase.adminitem_on_quote.price
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")


def decrease_adminitem_quantity(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                adminitem_to_decrease = QuoteAdminItem.objects.get(id=request.POST['adminitem_id'])
                adminitem_to_decrease.quantity -= 1 
                adminitem_to_decrease.combined_price -= adminitem_to_decrease.adminitem_on_quote.price
                adminitem_to_decrease.save() 

                quote = Quote.objects.get(id=request.POST['quote_id'])
                if adminitem_to_decrease.is_discount:
                    quote.total_price += adminitem_to_decrease.adminitem_on_quote.price
                else:
                    quote.total_price -= adminitem_to_decrease.adminitem_on_quote.price
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")


def remove_product_from_quote(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                    product_to_remove = QuoteProduct.objects.get(id=request.POST['product_id'])
                    quote = Quote.objects.get(id=request.POST['quote_id'])

                    quote.total_price -= product_to_remove.combined_price
                    quote.save()
                    
                    product_to_remove.delete() 
                    return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")

def remove_item_from_quote(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                    item_to_remove = QuoteItem.objects.get(id=request.POST['item_id'])
                    quote = Quote.objects.get(id=request.POST['quote_id'])

                    quote.total_price -= item_to_remove.combined_price
                    quote.save()
                    
                    item_to_remove.delete() 
                    return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")


def remove_adminitem_from_quote(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":  
                    adminitem_to_remove = QuoteAdminItem.objects.get(id=request.POST['adminitem_id'])
                    quote = Quote.objects.get(id=request.POST['quote_id'])

                    if adminitem_to_remove.is_discount:
                        quote.total_price += adminitem_to_remove.combined_price
                    else:
                        quote.total_price -= adminitem_to_remove.combined_price
                    quote.save()
                    
                    adminitem_to_remove.delete() 
                    return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")




def process_add_adminitem_to_quote(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            if request.method == "POST":                  
                # create AdminItem object
                name = request.POST['name']
                part_number = request.POST['part_number']
                manufacturer = request.POST['manufacturer']
                price = Decimal(request.POST['price'])
                if request.POST['is_discount'] == "discount":
                    is_discount = True
                else:
                    is_discount = False
                notes = request.POST['notes']

                new_adminitem = AdminItem.objects.create(
                    name = name,
                    part_number = part_number,
                    manufacturer = manufacturer,
                    price = price,
                    is_discount = is_discount,
                    notes = notes
                )

                if len(request.POST['quantity']):
                    quantity = int(request.POST['quantity'])
                else:
                    quantity = 1
                combined_price = new_adminitem.price * quantity

                # get quote
                quote = Quote.objects.get(id=request.POST['quote_id'])

                # create QuoteAdminItem
                qt_adminitem = QuoteAdminItem.objects.create(
                    adminitem_on_quote = new_adminitem,
                    quote = quote,
                    quantity = quantity,
                    combined_price = combined_price,
                    is_discount = new_adminitem.is_discount
                    )

                # checks to see if discount or charge and manipulates quote.total_price
                if qt_adminitem.is_discount:
                    quote.total_price -= qt_adminitem.combined_price
                else:
                    quote.total_price += qt_adminitem.combined_price
                quote.save()
                return redirect(f"/admin_access/view_quote/{ quote.id }")
            return redirect("/admin_access")
    return redirect("/")
