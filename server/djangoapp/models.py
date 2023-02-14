from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
# - Name
    name = models.CharField(max_length=40)
# - Description
    description = models.CharField(max_length=100)
# - Any other fields you would like to include in car make model
    country = models.CharField(max_length=30)
# - __str__ method to print a car make object
    def __str__(self):
        return "Name: " + self.name 

class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
# - Name
    name = models.CharField(max_length=40)
# - Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField()
# type choices
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    CONVERTIBLE = "convertible"
    COUPE = "coupe"
    SPORTSCAR = "sports_car"
    TYPE_CHOICES=[
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (CONVERTIBLE, "Convertible"),
        (COUPE, "Coupe"),
        (SPORTSCAR, "Sports Car")
    ]       
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
# - Year (DateField)
    year = models.DateField()
# - Any other fields you would like to include in car model
    description = models.CharField(max_length=100)
# - __str__ method to print a car make object
    def __str__(self):
        return "Name: " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer state abbreviation
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name


    def __str__(self):
        return "Dealer name: " + self.full_name   

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, purchase_date, review, car_make, car_model, car_year, sentiment):
        # Review Id
        #self.id = id
        # Dealership Id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Purchased?
        self.purchase = purchase
        # Purchase date
        self.purchase_date = purchase_date
        # Review
        self.review = review
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Review's sentiment
        self.sentiment = sentiment

    def __str__(self):
        return "Dealer name: " + self.name   