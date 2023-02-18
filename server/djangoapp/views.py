from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.template.loader import render_to_string
from .models import CarModel, CarMake

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contactus.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/8cc9c51c-fd9c-4d76-847a-40b2e5f2a978/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        return render(request, 'djangoapp/index.html', {'dealerships': dealerships})
        


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        revurl = "https://us-east.functions.appdomain.cloud/api/v1/web/8cc9c51c-fd9c-4d76-847a-40b2e5f2a978/dealership-package/get-review"
        dlrurl = "https://us-east.functions.appdomain.cloud/api/v1/web/8cc9c51c-fd9c-4d76-847a-40b2e5f2a978/dealership-package/get-dealership"

        reviews = get_dealer_reviews_from_cf(revurl, dealer_id)
        dealer = get_dealers_from_cf(dlrurl, dealerId=dealer_id)

        return render(request, 'djangoapp/dealer_details.html', {'reviews': reviews, 'dealer_id': dealer_id, 'dealer': dealer})
       
        

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    context = {}
    
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            cars = CarModel.objects.all()
            url = "https://us-east.functions.appdomain.cloud/api/v1/web/8cc9c51c-fd9c-4d76-847a-40b2e5f2a978/dealership-package/get-dealership"
            dealership = get_dealer_by_id(url, dealer_id)

            context["dealer_id"] = dealer_id
            context["cars"] = cars
            context['dealer'] = dealership

            return render(request, 'djangoapp/add_review.html', context)
        else: 
            return redirect("djangoapp:index")
        
    if request.method == 'POST':
        user = request.user
        #if user.is_authenticated:
        #    pass
        #else: return {}

        post_review_url = "https://us-east.functions.appdomain.cloud/api/v1/web/8cc9c51c-fd9c-4d76-847a-40b2e5f2a978/dealership-package/post-review"       

        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["id"] = user.id
        review["dealership"] = dealer_id
        review["review"] = request.POST["review"]
        review["name"] = user.first_name + " " + user.last_name
        
        if "purchasecheck" in request.POST:
            print("yes, they checked the box")
            review["purchase"] = True
            print("POST's 'car' = ", request.POST["car"])
            if ("car" in request.POST) & (request.POST["car"] != "none"):
                print("Yes, there was a car submitted. It was >>> ", request.POST["car"])
                car = get_object_or_404(CarModel, pk=request.POST["car"])
                review["car_year"] = car.year.strftime("%Y")
                review["car_make"] = car.make.name
                review["car_model"] = car.name
            if "purchasedate" in request.POST:
                review["purchase_date"] = request.POST["purchasedate"]
        else:
            print("No, they didn't check the box.")
            review["purchase"] = False
               
        json_payload = {}
        json_payload["review"] = review

        response = post_request(post_review_url, json_payload, dealerId=dealer_id)
        print(response.text)

    
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

