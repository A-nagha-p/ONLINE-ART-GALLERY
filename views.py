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
        full_name = request.POST['full_name']
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
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
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
        users = CustomUser.objects.exclude(is_superuser=True)
        return render(request, "admindash.html", {"users": users})
    return redirect("home")

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
        quantity = request.POST['quantity']
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
            quantity=quantity,
            description=description,
            price=price,
            status=status,
            product_image=product_image
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

    # Render the product details template with the product data
    return render(request, 'productdetails.html', {'product': product})




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
        image = request.FILES['productImage']  # Change 'image' to 'productImage'

        competition = Competition(
            competition_name=competition_name,
            description=description,
            date=date,
            time=time,
            am_pm=am_pm,
            location=location,
            image=image
        )
        competition.save()

        return redirect('competition')

    return render(request, 'addcompetition.html')

@never_cache
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






