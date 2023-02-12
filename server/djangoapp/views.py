from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        user_exist = False
        # Check if user exists
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, 
                                            last_name=last_name,password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/650772be-6b0d-416f-a9a5-2bae4e711b10/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = []
        for dealer in dealerships:
            dealer_names.append(dealer) 
        context["dealer_names"] = dealer_names
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/650772be-6b0d-416f-a9a5-2bae4e711b10/dealership-package/get-review.json"
        query = {"dealerId": dealer_id}
        # Get dealers from the URL and dealer id parameter
        reviews = get_dealer_by_id_from_cf(url, query)
        context["dealer_reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def get_review_form(request, **kwargs):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if user.is_authenticated:
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/650772be-6b0d-416f-a9a5-2bae4e711b10/dealership-package/post-review.json"
        review = dict()
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = User.objects.get(username=username)
        review["dealership"] = dealer_id
        review["review"] = request.body.review
        json_payload = dict()
        json_payload["review"] = review
        response = post_request(url, json_payload, dealer_id=dealer_id)
        print(response)
        return render(response, 'djangoapp/dealer_details.html')
