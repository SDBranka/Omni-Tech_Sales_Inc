from django.shortcuts import render, redirect
from .models import User, Product, EnteredItem, Photo, Category, Order, OrderProduct, OrderItem, Quote, QuoteProduct, QuoteItem, Review
from django.contrib import messages
from django.core.paginator import Paginator
import uuid


def index(request):
    if not 'user_id' in request.session:
        return render(request, "store_index.html")
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_user' : logged_user,
    }
    return render(request, "store_index.html", context)


def product_lines(request):
    if not 'user_id' in request.session:
        return render(request, "product_lines.html")
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_user' : logged_user,
    }
    return render(request, "product_lines.html", context)


def services(request, page_num):

    service_cat = Category.objects.get(name="Services")
    products_in_service = service_cat.product_in_category.all()

    p = Paginator(products_in_service, 6)
    page = p.page(page_num)
    num_of_pages = "a" * p.num_pages

    if not 'user_id' in request.session:
        context = {
            'all_services': page,
            'num_of_pages': num_of_pages,
            'n': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        return render(request, "services.html", context)
    
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_user' : logged_user,
        'all_services': page,
        'num_of_pages': num_of_pages,
        'n': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'current_page': page_num
    }
    return render(request, "services.html", context)


def view_product(request, product_id):

    product = Product.objects.get(id=product_id)
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])
        context = {
            'logged_user' : logged_user,
            'product': product
        }
    context = {
        'product': product
    }
    return render(request, "services.html", context)


def process_add_service_to_quote(request):
    if not 'user_id' in request.session:    
        return redirect("/")

    if request.method == "POST":
        orderer = User.objects.get(id=request.session['user_id'])
        product = Product.objects.get(id=request.POST['product_id'])
        page_num = request.POST['page_num']
        quantity = int(request.POST['quantity'])

        if not 'open_quote' in request.session:
            quote = Quote.objects.create(
            quoted_by = orderer,
            ref_number = uuid.uuid4().hex[:9],
            status = "open",
            )
            QuoteProduct.objects.create(
                product_on_quote = product,
                quote = quote,
                quantity = quantity
            )

            request.session['open_quote'] = quote.id
        else:
            quote = Quote.objects.get(id=request.session['open_quote'])

            is_on_quote = QuoteProduct.objects.filter(quote=quote).filter(product_on_quote = product)
            if is_on_quote:
                this_quote = is_on_quote[0]
                this_quote.quantity += quantity
                this_quote.save()
            else:
                QuoteProduct.objects.create(
                    product_on_quote = product,
                    quote = quote,
                    quantity = quantity
                )
        return redirect(f"/services/{ page_num }")
    return redirect("/services/1")


def user_account(request):
    if not 'user_id' in request.session:    
        return redirect("/")

    logged_user = User.objects.get(id=request.session['user_id'])

    context = {
        'logged_user': logged_user,
        'user_quotes': Quote.objects.filter(quoted_by = logged_user)    
    }
    return render(request, "user_account.html", context)


def request_quote(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if not 'open_quote' in request.session:
            context = {
            'logged_user': logged_user,
            # 'user_quotes': Quote.objects.filter(quoted_by = logged_user)    
        }
        else:
            open_quote = Quote.objects.get(id=request.session['open_quote'])
            all_quoteproducts = QuoteProduct.objects.filter(quote=open_quote)
            all_quoteitems = QuoteItem.objects.filter(quote=open_quote)

            context = {
                'logged_user': logged_user,
                'open_quote': open_quote,
                'products': all_quoteproducts,
                'items': all_quoteitems,
                # 'user_quotes': Quote.objects.filter(quoted_by = logged_user)    
            }
        return render(request, "request_quote.html", context)
    return render(request, "request_quote.html")


def process_add_item_to_quote(request):
    if 'user_id' in request.session:  
        if request.method == "POST":
            orderer = User.objects.get(id=request.session['user_id'])
            manufacturer = request.POST['manufacturer']
            part_number = request.POST['part_number']
            name = request.POST['name']
            price = request.POST['price']
            quantity = request.POST['quantity']
            notes = request.POST['notes']

            new_item = EnteredItem.objects.create(
                name = name,
                part_number = part_number,
                manufacturer = manufacturer,
                price = price,
                notes = notes,
            )

        if not 'open_quote' in request.session:
            quote = Quote.objects.create(
            quoted_by = orderer,
            ref_number = uuid.uuid4().hex[:9],
            status = "open",
            )

            QuoteItem.objects.create(
                item_on_quote = new_item,
                quote = quote,
                quantity = quantity
            )

            request.session['open_quote'] = quote.id
        else:
            quote = Quote.objects.get(id=request.session['open_quote'])

            QuoteItem.objects.create(
                item_on_quote = new_item,
                quote = quote,
                quantity = quantity
            )
    return redirect("/request_quote")


def increase_product_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            product_to_increase = QuoteProduct.objects.get(id=request.POST['product_id'])
            product_to_increase.quantity += 1   
            product_to_increase.save() 
    return redirect("/request_quote")


def increase_item_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            item_to_increase = QuoteItem.objects.get(id=request.POST['item_id'])
            item_to_increase.quantity += 1   
            item_to_increase.save() 
    return redirect("/request_quote")


def decrease_product_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            product_to_decrease = QuoteProduct.objects.get(id=request.POST['product_id'])
            if product_to_decrease.quantity > 1:
                product_to_decrease.quantity -= 1   
                product_to_decrease.save() 
    return redirect("/request_quote")


def decrease_item_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            item_to_decrease = QuoteItem.objects.get(id=request.POST['item_id'])
            if item_to_decrease.quantity > 1:
                item_to_decrease.quantity -= 1   
                item_to_decrease.save() 
    return redirect("/request_quote")


def remove_product_from_quote(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            product_to_remove = QuoteProduct.objects.get(id=request.POST['product_id'])
            product_to_remove.delete() 
    return redirect("/request_quote")


def remove_item_from_quote(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            item_to_remove = QuoteItem.objects.get(id=request.POST['item_id'])
            item_to_remove.delete() 
    return redirect("/request_quote")


def add_spec_inst(request):
    if not 'user_id' in request.session:    
        return redirect("/")

    if request.method == "POST":
        orderer = User.objects.get(id=request.session['user_id'])
        
        if 'open_quote' in request.session:
            quote = Quote.objects.get(id=request.session['open_quote'])
            quote.special_instructions = request.POST['special_instructions']
            quote.save()
    return redirect("/request_quote")


def delete_quote(request):
    if not 'user_id' in request.session:    
        return redirect("/")

    if request.method == "POST":        
        if 'open_quote' in request.session:
            orderer = User.objects.get(id=request.session['user_id'])
            quote = Quote.objects.get(id=request.session['open_quote'])
            quote.delete()
            request.session.flush()
            request.session['user_id'] = orderer.id
    return redirect("/request_quote")


def submit_quote(request):
    if 'user_id' in request.session:
        orderer = User.objects.get(id=request.session['user_id'])
        if 'open_quote' in request.session: 
            quote = Quote.objects.get(id=request.session['open_quote'])
            if request.method == "POST": 
                quote.status = "pending"
                quote.save()
                request.session.flush()
                request.session['user_id'] = orderer.id
        return redirect("/user_account")
    return redirect("/request_quote")



























