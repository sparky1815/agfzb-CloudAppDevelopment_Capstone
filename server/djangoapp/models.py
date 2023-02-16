from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return "Name: " + self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

MODEL_TYPES = (
    ("Sedan", "Sedan"),
    ("SUV", "SUV"),
    ("Wagon", "Wagon"),
    ("Coupe", "Coupe"),
)

class CarModel(models.Model):
    name = models.CharField(max_length=255)
    dealer_id = models.IntegerField()
    type = models.CharField(
        max_length = 20,
        choices = MODEL_TYPES,
        default = "Sedan"
    )
    year = models.DateField()
    make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Name: " + self.name



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
