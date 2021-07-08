from re import U
from django.shortcuts import render, redirect
from .models import User, Product, EnteredItem, Photo, Category, Order, Quote, QuoteProduct, QuoteItem, ContactInfo, Review
from django.contrib import messages
from django.core.paginator import Paginator
import uuid
from datetime import datetime


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


# Build to display individual product pages
# def view_product(request, product_id):
#     product = Product.objects.get(id=product_id)
#     if 'user_id' in request.session:    
#         logged_user = User.objects.get(id=request.session['user_id'])
#         context = {
#             'logged_user' : logged_user,
#             'product': product
#         }
#     context = {
#         'product': product
#     }
#     return render(request, "services.html", context)


def process_add_service_to_quote(request):
    if not 'user_id' in request.session:    
        return redirect("/")

    if request.method == "POST":
        orderer = User.objects.get(id=request.session['user_id'])
        product = Product.objects.get(id=request.POST['product_id'])
        page_num = request.POST['page_num']
        quantity = int(request.POST['quantity'])

        combined_price = product.price * quantity

        if not 'open_quote' in request.session:
            new_quote = Quote.objects.create(
            quoted_by = orderer,
            ref_number = uuid.uuid4().hex[:9],
            total_price = combined_price,
            status = "open",
            placed_at = datetime.now()
            )
            QuoteProduct.objects.create(
                product_on_quote = product,
                quote = new_quote,
                quantity = quantity,
                combined_price = combined_price
            )

            request.session['open_quote'] = new_quote.id
        else:
            quote = Quote.objects.get(id=request.session['open_quote'])

            is_on_quote = QuoteProduct.objects.filter(quote=quote).filter(product_on_quote = product)
            if is_on_quote:
                this_quote = is_on_quote[0]
                this_quote.quantity += quantity
                print(f"#### {this_quote.combined_price }")
                this_quote.combined_price += combined_price
                this_quote.save() 
            else:
                QuoteProduct.objects.create(
                    product_on_quote = product,
                    quote = quote,
                    quantity = quantity,
                    combined_price = combined_price
                )
            quote.total_price += combined_price
            quote.save()
        return redirect(f"/services/{ page_num }")
    return redirect("/services/1")


def user_account(request):
    if 'user_id' in request.session:    
        logged_user = User.objects.get(id=request.session['user_id'])

        context = {
            'logged_user': logged_user,
            'most_recent_quotes': Quote.objects.exclude(status="open")[:6],
            'most_recent_orders': Order.objects.all()[:6],
            'my_contacts': ContactInfo.objects.filter(user=logged_user)
        }
        return render(request, "user_account.html", context)
    return render(request, "user_account.html")
    

def request_quote(request):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        if not 'open_quote' in request.session:
            context = {
            'logged_user': logged_user,
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
            price = float(request.POST['price'])
            quantity = int(request.POST['quantity'])
            notes = request.POST['notes']

            combined_price = price * quantity

            new_item = EnteredItem.objects.create(
                name = name,
                part_number = part_number,
                manufacturer = manufacturer,
                price = price,
                notes = notes,
            )

        if not 'open_quote' in request.session:
            new_quote = Quote.objects.create(
            quoted_by = orderer,
            ref_number = uuid.uuid4().hex[:9],
            total_price = combined_price,
            status = "open",
            placed_at = datetime.now()
            )

            QuoteItem.objects.create(
                item_on_quote = new_item,
                quote = new_quote,
                quantity = quantity,
                combined_price = combined_price
            )

            request.session['open_quote'] = new_quote.id
        else:
            quote = Quote.objects.get(id=request.session['open_quote'])

            QuoteItem.objects.create(
                item_on_quote = new_item,
                quote = quote,
                quantity = quantity,
                combined_price = combined_price
            )
            quote.total_price += combined_price
            quote.save()
    return redirect("/request_quote")


def increase_product_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            product_to_increase = QuoteProduct.objects.get(id=request.POST['product_id'])
            product_to_increase.quantity += 1 
            product_to_increase.combined_price += product_to_increase.product_on_quote.price
            product_to_increase.save() 

            quote = Quote.objects.get(id=request.session['open_quote'])
            quote.total_price += product_to_increase.product_on_quote.price
            quote.save()
    return redirect("/request_quote")


def increase_item_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            item_to_increase = QuoteItem.objects.get(id=request.POST['item_id'])
            item_to_increase.quantity += 1   
            item_to_increase.combined_price += item_to_increase.item_on_quote.price
            item_to_increase.save() 

            quote = Quote.objects.get(id=request.session['open_quote'])
            quote.total_price += item_to_increase.item_on_quote.price
            quote.save()
    return redirect("/request_quote")


def decrease_product_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            product_to_decrease = QuoteProduct.objects.get(id=request.POST['product_id'])
            if product_to_decrease.quantity > 1:
                product_to_decrease.quantity -= 1
                product_to_decrease.combined_price -= product_to_decrease.product_on_quote.price
                product_to_decrease.save() 

                quote = Quote.objects.get(id=request.session['open_quote'])
                quote.total_price -= product_to_decrease.product_on_quote.price
                quote.save()
    return redirect("/request_quote")


def decrease_item_quantity(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            item_to_decrease = QuoteItem.objects.get(id=request.POST['item_id'])
            if item_to_decrease.quantity > 1:
                item_to_decrease.quantity -= 1  
                item_to_decrease.combined_price -= item_to_decrease.item_on_quote.price
                item_to_decrease.save()

                quote = Quote.objects.get(id=request.session['open_quote'])
                quote.total_price += item_to_increase.item_on_quote.price
                quote.save()
    return redirect("/request_quote")


def remove_product_from_quote(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            product_to_remove = QuoteProduct.objects.get(id=request.POST['product_id'])
            quote = Quote.objects.get(id=request.session['open_quote'])

            quote.total_price -+ product_to_remove.combined_price
            quote.save()
            
            product_to_remove.delete() 
    return redirect("/request_quote")


def remove_item_from_quote(request):
    if 'user_id' in request.session:    
        if 'open_quote' in request.session:
            item_to_remove = QuoteItem.objects.get(id=request.POST['item_id'])
            quote = Quote.objects.get(id=request.session['open_quote'])

            quote.total_price -+ item_to_remove.combined_price
            quote.save()

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
    if request.method == "POST":        
        if 'user_id' in request.session:    
            orderer = User.objects.get(id=request.session['user_id'])
            if 'open_quote' in request.session:
                quote = Quote.objects.get(id=request.session['open_quote'])
                if 'open_quote' in request.session:
                    quote = Quote.objects.get(id=request.session['open_quote'])
                    quote.delete()
                    request.session.flush()
                    request.session['user_id'] = orderer.id
    return redirect("/request_quote")


def select_contact_info(request):
    if 'user_id' in request.session:
        print("#!#!#!#! IN select_contact_info")
        if 'open_quote' in request.session:
            orderer = User.objects.get(id=request.session['user_id'])
            user_contacts = ContactInfo.objects.filter(user = orderer)
            
            context = {
                'logged_user': orderer,
                'user_contacts': user_contacts,
            }
        return render(request, "select_contact_info.html", context)
    return redirect("/")


def add_new_contact(request):
    if 'user_id' in request.session:
        orderer = User.objects.get(id=request.session['user_id'])
        if request.method == "POST":
            new_contact = ContactInfo.objects.create(
                address_1 = request.POST['address_1'],
                address_2 = request.POST['address_2'],
                city = request.POST['city'],
                zip_code = request.POST['zip_code'],
                state = request.POST['state'],
                country = request.POST['country'],
                phone = request.POST['phone'],
            )

            confirm_quote = request.POST["confirm_quote"]  
            if confirm_quote:
                new_contact.user.add(orderer)
                request.session['check_passed'] = new_contact.id
                return redirect("/submit_quote")
            return redirect("/user_account")    
    return redirect("/")


def submit_quote(request):
    if 'user_id' in request.session:
        orderer = User.objects.get(id=request.session['user_id'])
        if 'open_quote' in request.session: 
            quote = Quote.objects.get(id=request.session['open_quote'])
            if request.method == "POST": 
                contact = ContactInfo.objects.get(id=request.POST['contact_id'])
                contact.quotes.add(quote)  

                quote.placed_at = datetime.now()
                quote.status = "pending"
                quote.save()
                request.session.flush()
                request.session['user_id'] = orderer.id
                return redirect("/user_account")
            if 'check_passed' in request.session:
                contact = ContactInfo.objects.get(id=request.session['check_passed'])
                contact.quotes.add(quote)

                quote.placed_at = datetime.now()
                quote.status = "pending"
                quote.save()
                request.session.flush()
                request.session['user_id'] = orderer.id
                return redirect("/user_account")
    return redirect("/request_quote")


def delete_contact(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            redirect_to = request.POST['redirect_to']
            contact_to_delete = ContactInfo.objects.get(id=request.POST['contact_id'])
            contact_to_delete.delete()
            return redirect(f"/{ redirect_to }")
    return redirect("/")


def edit_contact(request, redirect_reference, contact_id):
    if 'user_id' in request.session:
        logged_user = User.objects.get(id=request.session['user_id'])
        contact_to_edit = ContactInfo.objects.get(id=contact_id)

        # redirect processing
        if redirect_reference == "sci":
            direct_to = "select_contact_info"
        if redirect_reference == "ua":
            direct_to = "user_account"

        context = {
            'logged_user': logged_user,
            'contact_to_edit': contact_to_edit,
            'direct_to': direct_to
        }
        return render(request, "edit_contact.html", context)
    return redirect("/")


def process_edit_contact(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            # errors handling
            # errors = Wish.objects.wish_validator(request.POST)
            # if len(errors) > 0:
            #     for error in errors.values():
            #         messages.error(request, error)
            #     return redirect(f"/wishes/edit_wish/{ wish_id }")
            # else:
            direct_to = request.POST['direct_to']

            contact_to_edit = ContactInfo.objects.get(id=request.POST['contact_id'])

            contact_to_edit.address_1 = request.POST['address_1']
            contact_to_edit.address_2 = request.POST['address_2']
            contact_to_edit.city = request.POST['city']
            contact_to_edit.zip_code = request.POST['zip_code']
            contact_to_edit.state = request.POST['state']
            contact_to_edit.country = request.POST['country']
            contact_to_edit.phone = request.POST['phone']
            contact_to_edit.save()
            return redirect(f"/{ direct_to }")
    return redirect("/")


def proces_edit_profile(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            # errors handling
            # errors = Wish.objects.wish_validator(request.POST)
            # if len(errors) > 0:
            #     for error in errors.values():
            #         messages.error(request, error)
            #     return redirect(f"/wishes/edit_wish/{ wish_id }")
            # else:

            logged_user = User.objects.get(id=request.session['user_id'])
            logged_user.first_name = request.POST['first_name']
            logged_user.last_name = request.POST['last_name']
            logged_user.email = request.POST['email']
            logged_user.save()
        return redirect("/user_account")
    return redirect("/")
    





def trial(request):
    product = Product.objects.get(id=2)
    two = product.price * 2

    context={

        'product': product,
        'two': two

    }

    return render(request, "Trial.html", context)








