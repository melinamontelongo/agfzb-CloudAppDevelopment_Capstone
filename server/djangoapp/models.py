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
        return "Name: " + self.name + "," + \
               "Description: " + self.description + \
                "Country: " + self.country 

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
        return "Name: " + self.name + "," + \
               "Description: " + self.description + \
                "Dealer ID: " + self.dealer_id + \
                "Type: " + self.type + \
                "Year: " + self.year + \
                "Description: " + self.description

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
    

# <HINT> Create a plain Python class `DealerReview` to hold review data
