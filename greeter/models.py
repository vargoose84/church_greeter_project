from django.db import models
from django.contrib.auth.models import User

class greeterRecord(models.Model):
    trainerID = models.ForeignKey('greeterID')
    churchGoer = models.ForeignKey('churchGoer')
    flag = models.BooleanField(default=False)
    
class churchGoer(models.Model):
    gender_choices = (('male', 'male'),('female','female'),)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    gender = models.CharField(max_length=128, choices=gender_choices, default="Male")
    children = models.ManyToManyField('self',  symmetrical=False, related_name="myParents", blank =True)
    parents = models.ManyToManyField('self',  symmetrical=False, related_name="myChildren", blank =True)
    spouse = models.ManyToManyField('self', related_name = "spouse", blank =True)
    siblings = models.ManyToManyField('self', related_name="siblings" blank =True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    occupation = models.CharField(max_length=128, blank=True)
    def __unicode__(self):
   
        return self.first_name + " " + self.last_name 
        
class greeterID(models.Model):
    # This line is required. Links UserProfi    le to a User model instance.
    user = models.OneToOneField(User)
    churchGoer =  models.OneToOneField(churchGoer) 

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
       
# def populateGreeter(churchGoer):
    # for g in greeterRecord.objects.all():
        # greeterRecord.objects.get_or_create(churchGoer=churchGoer, trainerid=g.churchGoer)
        