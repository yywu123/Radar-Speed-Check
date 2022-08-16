from django.db import models

# Create your models here.


class CheckItem(models.Model):
    date = models.DateField(blank=False)
    speed = models.IntegerField()
    weather = models.CharField(max_length=30)
    surveyor = models.CharField(max_length=30)
    borough = models.CharField(max_length=30)
    location = models.CharField(max_length=100)

    class Meta :
        ordering = ['id']

    def __str__(self):
        return str(self.date) + ', Speed: ' + str(self.speed) + ', Weather: ' + str(self.weather) + ', Location: ' + str(self.location) + ', Surveyor: ' + str(self.surveyor)




class TimeSheet(models.Model):
    item = models.ForeignKey(to='CheckItem', on_delete=models.CASCADE)
    time = models.TimeField(blank=False)
    carrier = models.CharField(max_length=10)
    mph = models.IntegerField()
    remarks_list = (
        (1, "Away"),
        (2,"Towards"),
        (3, "Left Lane"),
        (4, "Middle Lane"),
        (5, "Right Lane"),
        (6, "Northbound"),
    )

    #remarks = models.CharField(max_length=100)
    remarks = models.SmallIntegerField(choices=remarks_list)
    bus = models.IntegerField()
    route = models.IntegerField(blank=True, default= None, null=True)
