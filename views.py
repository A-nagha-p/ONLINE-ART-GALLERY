from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser,Competition  # Assuming you have a CustomUser model
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import CustomUser
from django.http import HttpResponse
from .models import Product
from .models import Blog

from django.http import JsonResponse
from decimal import Decimal
from .models import Order
import razorpay
from .models import Bid
from .models import AuctionProduct
from django.utils import timezone

from django.db.models import Q





@never_cache
def index(request):
    return render(request,'index.html')
@never_cache
def blog(request):
    return render(request,'blog.html')
@never_cache
def about(request):
    return render(request,'about.html')
@never_cache
def contact(request):
    return render(request,'contact.html')
@never_cache
def exhibition(request):
    return render(request,'exhibition.html')
@never_cache
def competition(request):
    return render(request,'competition.html')
@never_cache
def artstore(request):
    return render(request,'artstore.html')
#@never_cache
#@login_required(login_url='login')
#def admindash(request):
    #return render(request,'admindash.html')


@never_cache
def compapply(request):
    return render(request,'compapply.html')
@never_cache
def blogone(request):
    return render(request,'blogone.html')

@never_cache
@login_required(login_url='login')
def userprofile(request):
    if 'username' in request.session:
        response = render(request,'userprofile.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')

@never_cache
@login_required(login_url='login')
def artistprofile(request):
    if 'username' in request.session:
        response = render(request,'artistprofile.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')


@never_cache
def register(request):
     if request.method == 'POST':
        first_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # Make sure this matches your form field name
        user_type = request.POST['user_type']

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type, phone=phone,first_name=first_name )
        # You may want to do additional processing here if needed

        return redirect('login')  # Redirect to login page after successful registration

     return render(request,'register.html')


from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

@never_cache
def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        password = request.POST.get('password')

        if loginusername and password:  # Use 'loginusername' here
            user = authenticate(request, username=loginusername, password=password)

            if user is not None:
                auth_login(request, user)
                request.session['username'] = user.username
                if user.user_type == 'user':
                    messages.success(request, 'Login successful')
                    return redirect('userprofile')
                elif user.user_type == 'artist':
                    messages.success(request, 'Login successful')
                    return redirect('artistprofile')
                else:
                    return redirect('admindash')
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = 'Username and password are required'
            return render(request, 'login.html', {'error_message': error_message})

    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response

@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@never_cache
def logout(request):
    auth.logout(request)
    return redirect("/")


@never_cache
@login_required(login_url='login')
def admindash(request):
    if request.user.is_superuser:
        # Get the count of users with user_type='user'
        user_count = CustomUser.objects.filter(user_type='user').count()

        # Get the count of users with user_type='artist'
        artist_count = CustomUser.objects.filter(user_type='artist').count()

        # Get the list of users excluding superusers
        users = CustomUser.objects.exclude(is_superuser=True)

        return render(request, "admindash.html", {"users": users, "user_count": user_count, "artist_count": artist_count})

    return redirect("home")
#@never_cache
#@login_required(login_url='login')
#def admindash(request):
 #   if request.user.is_superuser:
  #      users = CustomUser.objects.exclude(is_superuser=True)
   #     return render(request, "admindash.html", {"users": users})
    #return redirect("home")

@never_cache
def addproduct(request):
    return render(request,'addproduct.html')

@never_cache
def blogupload(request):
    return render(request,'blogupload.html')

@never_cache
def editprofile(request):
    # Your edit profile logic here
    return render(request, 'editprofile.html')  # Replace with your template and logic

@never_cache
@login_required(login_url='login')
def regusers(request):
    if request.user.is_superuser:
        # Fetch users with user_type 'user' and exclude superusers
        users = CustomUser.objects.filter(user_type='user', is_superuser=False)

        return render(request, 'regusers.html', {'users': users})
    else:
        return redirect('home')


@never_cache
@login_required(login_url='login')
def regartist(request):
    if request.user.is_superuser:
        # Fetch users with user_type 'user' and exclude superusers
        users = CustomUser.objects.filter(user_type='artist', is_superuser=False)

        return render(request, 'regartist.html', {'users': users})
    else:
        return redirect('home')

@never_cache
def add_product(request):
    if request.method == 'POST':
        # Extract form data from the request
        product_name = request.POST['productName']
        theme = request.POST['theme']
        art_type = request.POST['artType']
        # quantity = request.POST['quantity']
        description = request.POST['description']
        price = request.POST['price']
        status = request.POST['status']
        
        # Assuming you have a file input with name "productImage"
        product_image = request.FILES['productImage']

        # Create a new Product object and save it to the database
        product = Product(
            product_name=product_name,
            theme=theme,
            art_type=art_type,
            # quantity=quantity,
            description=description,
            price=price,
            status=status,
            product_image=product_image,
            author=request.user
        )
        product.save()

        # Redirect to a success page or do something else
        return redirect('addproduct')

    # If the request method is not POST, render the form page
    return render(request, 'addproduct.html')



@never_cache
def viewproduct(request):
    # Query your products from the database
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'viewproduct.html', context)


@never_cache
def base(request):
    return render(request,'base.html')



@never_cache  
def product_list(request):
    # Query your products from the database
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'exhibition.html', context)

@never_cache
def product_details(request, id):
    # Retrieve the product details from the database
    product = get_object_or_404(Product, id=id)

    # Calculate the price multiplied by 100
    price_times_100 = product.price * 100

    # Render the product details template with the product data
    return render(request, 'productdetails.html', {
        'product': product,
        'price_times_100': price_times_100,
        'user': request.user,
    })



@never_cache
@login_required(login_url='login')
def add_competition(request):
    if request.method == 'POST':
        competition_name = request.POST['competition_name']
        description = request.POST['description']
        date = request.POST['date']
        time = request.POST['time']
        am_pm = request.POST['ampm']
        location = request.POST['location']
        fee = request.POST['fee']
        image = request.FILES['productImage']  # Change 'image' to 'productImage'

        competition = Competition(
            competition_name=competition_name,
            description=description,
            date=date,
            time=time,
            am_pm=am_pm,
            location=location,
            fee=fee,
            image=image,
            author=request.user
        )
        competition.save()

        return redirect('competition')

    return render(request, 'addcompetition.html')

@never_cache
@login_required
def competition(request):
    # Fetch a list of competitions from the database
    competitions = Competition.objects.all()
    
    return render(request, 'competition.html', {'competitions': competitions})


@never_cache
def viewcompetition(request):
    return render(request,'viewcompetition.html')


@never_cache

def viewcompetition(request):
    # Query competitions from the database
    competitions = Competition.objects.all()

    context = {
        'competitions': competitions,
    }

    return render(request, 'viewcompetition.html', context)

@never_cache
def adminviewproduct(request):
    return render(request,'adminviewproduct.html')

@never_cache
def adminviewproduct(request):
    # Query your products from the database
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'adminviewproduct.html', context)




   


@never_cache
@login_required
def blogupload(request):
    if request.method == 'POST':
        title = request.POST['title']
        publishingDate = request.POST['publishingDate']
        description = request.POST['description']
        image = request.FILES.get('image', None)

        # Validate form data
        if not title or not publishingDate or not description:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('blogupload')

        # Check if the logged-in user is an artist
        if request.user.user_type != 'artist':
            messages.error(request, 'Only artists can upload blogs.')
            return redirect('blogupload')

        # Create and save the blog
        new_blog = Blog(
            title=title,
            publishingDate=publishingDate,
            description=description,
            image=image,
            author=request.user
        )
        new_blog.save()

        messages.success(request, 'Blog uploaded successfully!')
        return redirect('blog')  # Redirect to the blog list page

    return render(request, 'blogupload.html')
@never_cache
def blog(request):
    # Fetch all blogs from the database
    blogs = Blog.objects.all()

    return render(request, 'blog.html', {'blogs': blogs})

@never_cache
def viewblogs(request):
    blogs = Blog.objects.all()  # Fetch all blogs from the database
    return render(request, 'viewblogs.html', {'blogs': blogs})



@never_cache
def delete_competition(request, competition_id):
    # Get the competition object from the database
    competition = get_object_or_404(Competition, id=competition_id)

    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the competition
        competition.delete()
        # Redirect to the competition list page or any other appropriate page
        return redirect('competition')  # Replace 'competition_list' with the URL name of the page displaying the list of competitions

    # Render a confirmation page if the request method is GET
    return render(request, 'viewcompetition.html', {'competition': competition})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product.delete()

    messages.success(request, "Product deleted successfully.")
    return redirect('adminviewproduct')  

from django.utils import timezone


@never_cache
def payment_success(request):
    product_id = request.GET.get('product_id')
    user_id = request.GET.get('user_id')
    amount = request.GET.get('amount')

    # Convert the amount to a decimal number
    amount_decimal = Decimal(amount)

    # Create a new Order
    order = Order.objects.create(
        user_id=user_id,
        product_id=product_id,
        price=amount_decimal,
        payment_status='Completed',
        date=timezone.now().date(),
         # Assuming you have a 'status' field in your Order model
    )

    # Redirect to the user profile or any other desired page
    return redirect('userprofile')


@never_cache
def viewpayment(request):
    orders = Order.objects.all()
    return render(request, 'viewpayment.html', {'orders': orders})



#@never_cache
#def addauction(request):
 #   return render(request,'addauction.html')


@never_cache
def addauction(request):
    latest_auction_product = AuctionProduct.objects.latest('id')  # Assuming 'id' is the primary key
    if request.method == 'POST':
        # Extract form data from the request
        product_name = request.POST['product_name']
        about_product = request.POST['about_product']
        current_price = request.POST['current_price']
        product_image = request.FILES['product_image']
        auction_start_datetime=request.POST['auction_start_datetime']
        auction_end_datetime=request.POST['auction_end_datetime']
        print(auction_start_datetime,auction_end_datetime,"printeddddddddddddddddddddddddd")
        
        # Get the current date and time
        

        # Create a new AuctionProduct instance
        auction_product = AuctionProduct(
            product_name=product_name,
            about_product=about_product,
            auction_start_datetime=auction_start_datetime,  # Set the start datetime to current time
            auction_end_datetime=auction_end_datetime,  # Set the end datetime to current time
            current_price=current_price,
            product_image=product_image,
            author=request.user
        )
        auction_product.save()

        # Redirect to a success page or do something else
        messages.success(request, 'Product added successfully!')
        return redirect('addauction')  # Redirect to the same page after adding product

    # If the request method is not POST, render the form page
    context = {'latest_auction_product': latest_auction_product}
    return render(request, 'addauction.html', context)


@never_cache
def auction(request):
    # Exclude auction products with any null or empty fields
    auction_products = AuctionProduct.objects.exclude(
        Q(product_name='') | 
        Q(about_product='') | 
        Q(auction_start_datetime=None) | 
        Q(auction_end_datetime=None) | 
        Q(current_price=None) | 
        Q(product_image='')
    )

    # Render the auction.html template with the filtered auction products in the context
    return render(request, 'auction.html', {'auction_products': auction_products})





#@never_cache
#def adminauction(request):
 #   return render(request,'adminauction.html')


@never_cache
def adminauction(request):
    if request.method == 'POST':
        auction_start_datetime_str = request.POST.get('auction_start_datetime')
        auction_end_datetime_str = request.POST.get('auction_end_datetime')
        print("cccccccccccc")
        print(auction_start_datetime_str)
        print(auction_end_datetime_str)
        
        # Create AuctionProduct instance
        auction_product = AuctionProduct(
            auction_start_datetime=auction_start_datetime_str,
            auction_end_datetime=auction_end_datetime_str
        )
        auction_product.save()

        return redirect('adminauction')  # Redirect to the same page after submitting the form

    return render(request, 'adminauction.html')


@never_cache
def editdateandtime(request):
    auction_products = AuctionProduct.objects.all()
    return render(request, 'editdateandtime.html', {'auction_products': auction_products})

@never_cache
@login_required
def auction_product_detail(request, product_id):
    # Assuming product_id is the primary key of the AuctionProduct model
    auction_product = AuctionProduct.objects.get(pk=product_id)
    bids = Bid.objects.filter(product_id=product_id).order_by('-bid_amount') 
    context={'auction_product': auction_product,'bids':bids}
    return render(request, 'auctiondetails.html',context)

from django.contrib.auth import get_user_model
User=get_user_model()

@never_cache
def place_bid(request, product_id):
    # Attempt to retrieve the product with the given ID from the database
    product = get_object_or_404(AuctionProduct, pk=product_id)

    if request.method == 'POST':
        # Assuming bid amount and name are sent via POST request
        bid_amount = request.POST.get('bidAmount')
        

        # Create a new bid object
        bid = Bid(
            user=request.user,
            product=product,
            name="null",
            bid_amount=bid_amount,
            timestamp=timezone.now()
        )
        bid.save()

        return redirect('auction_product_detail', product_id=product_id)  # Redirect to product detail view after placing bid
    else:
        # If the request method is not POST, render the template with the product details
        return render(request, 'auctiondetails.html', {'product': product})

@never_cache
def auctionwinner(request):
    # Retrieve all Bid objects
    all_bids = Bid.objects.all()

    # Create a dictionary to store the highest bid object for each product
    max_bid_per_product = {}

    # Iterate through all bid objects to find the maximum bid for each product
    for bid in all_bids:
        product_id = bid.product_id
        if product_id not in max_bid_per_product or bid.bid_amount > max_bid_per_product[product_id].bid_amount:
            max_bid_per_product[product_id] = bid

    # Get the highest bid objects for each product
    highest_bids = max_bid_per_product.values()

    # Pass the bid objects to the template context
    context = {
        'all_bids': all_bids,
        'highest_bids': highest_bids,
    }

    # Render the template with the context
    return render(request, 'auctionwinner.html', context)



@never_cache
def watermark(request):
    return render(request,'watermark.html')


@never_cache
def adminauctiondelete(request):
    # Exclude auction products with any null or empty fields
    auction_products = AuctionProduct.objects.exclude(
        Q(product_name='') | 
        Q(about_product='') | 
        Q(auction_start_datetime=None) | 
        Q(auction_end_datetime=None) | 
        Q(current_price=None) | 
        Q(product_image='') |
        Q(author=None)
    )

    # Render the adminauctiondelete.html template with the filtered auction products in the context
    return render(request, 'adminauctiondelete.html', {'auction_products': auction_products})



@never_cache
def search_products(request):
    if request.method == 'GET' and 'search_text' in request.GET:
        search_text = request.GET['search_text']
        # Perform filtering based on search_text
        products = Product.objects.filter(product_name__icontains=search_text)
        # Serialize the filtered products
        data = [{'product_name': product.product_name, 'product_image': product.product_image.url, 'theme': product.theme, 'art_type': product.art_type, 'description': product.description, 'price': product.price, 'status': product.get_status_display(), 'author': product.author.username} for product in products]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)









from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .utils import hide_text



from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageDraw, ImageFont
import io
import os

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        image = Image.open(uploaded_image)
        text = "ART WATERMARK"
        
        # Draw watermark text on the image
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), text, fill=(255, 255, 255))  # Draw white text at (10, 10)

        # Convert image to bytes
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            image_bytes = output.getvalue()

        # Return the watermarked image as a response
        response = HttpResponse(image_bytes, content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename="watermarked_image.png"'
        return response

    return render(request, 'upload.html')


def download_image(request, filename):
    fs = FileSystemStorage()
    image_path = fs.path(filename)
    with open(image_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response

def water(request):
    return render(request, 'water.html')







