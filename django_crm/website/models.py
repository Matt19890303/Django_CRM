from django.db import models

# This is the Data(fields) we want to add to our CRM
class Record(models.Model):
    # Date when record was created
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)


# What we want to show on the screen when we access these records
# if you call one of these records it will return the first name and last name
    def __str__(self):
        return(f"{self.first_name} {self.last_name}")