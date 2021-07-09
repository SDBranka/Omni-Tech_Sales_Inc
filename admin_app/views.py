from decimal import Decimal
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from imgfield_app.models import ContactInfo, User, Product, Photo, Quote, QuoteProduct, QuoteItem, Order, OrderProduct, OrderItem, Category
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
                    price = Decimal(request.POST['price']),
                    desc = request.POST['desc'],
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
                # errors = Wish.objects.wish_validator(request.POST)
                # if len(errors) > 0:
                #     for error in errors.values():
                #         messages.error(request, error)
                #     return redirect(f"/wishes/edit_wish/{ wish_id }")
                # else:

                product_to_edit.name = request.POST['name']
                product_to_edit.part_number = request.POST['part_number']
                product_to_edit.price = Decimal(request.POST['price'])
                product_to_edit.desc = request.POST['desc']
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
        
            context = {
                'logged_user': logged_user,
                'quote': quote,
                'products': all_quoteproducts,
                'items': all_quoteitems,
            }
            return render(request, "view_quote.html", context)
    return redirect("/")


def view_order(request, order_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if logged_user.security_level > 4:
            order = Order.objects.get(id=order_id)
            all_orderproducts = OrderProduct.objects.filter(order=order)
            all_orderitems = OrderItem.objects.filter(order=order)

            context = {
                'logged_user': logged_user,
                'order': order,
                'products': all_orderproducts,
                'items': all_orderitems,
            }
            return render(request, "view_order.html", context)
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
                    status = "open",
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
        # status choices = {open, pending, in process, completed, archived }
            all_active_orders= Order.objects.exclude(status = "archived").order_by('-created_at')
            # all_active_orders = Order.objects.all()

            # quote = Quote.objects.all()
            # print(f"ContactInfo_id: {quote.contact_info.id}")
            order = Order.objects.get(id=1)
            # print(f"##### { quote}")
            # print(f"#### {quote.contact_info}")
            # print(f"#### {order.contact_info.user.first_name}")<---no attrib

            

            # quote = Quote.objects.get(id = 2)
            # print(f"#### { quote.total_price }")
            
            # ClassName.objects.first()


            quote = Quote.objects.first()
            q_item = QuoteItem.objects.first()
            
            print("#############")
            # print(quote.total_price + q_item.combined_price)


            
            
            
            
            # order = Order.objects.all()
            # print(f"ContactInfo_id: {order.contact_info.id}")
            # print(f"##### { order}")


            context = {
                'logged_user': logged_user,
                'all_active_orders': all_active_orders
                # 'test': 
            }
        return render(request, "orders_display.html", context)
    return redirect("/")



