from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import *

class suggestion(models.Model):
    greeterID = models.ForeignKey('greeterID')
    category = models.CharField(max_length=128)
    subject = models.CharField(max_length = 500)
    description = models.TextField()
    flag = models.BooleanField(default=False)
class greeterRecord(models.Model):
    trainerID = models.ForeignKey('greeterID')
    churchGoer = models.ForeignKey('churchGoer')
    flag = models.BooleanField(default=False)
    quizScore = models.IntegerField(default=0)
    def __unicode__(self):
        return self.trainerID.churchGoer.first_name + " " + self.trainerID.churchGoer.last_name + ": "  + self.churchGoer.first_name + " " + self.churchGoer.last_name
class churchGoer(models.Model):
    gender_choices = (('male', 'male'),('female','female'),)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    gender = models.CharField(max_length=128, choices=gender_choices, default="Male")
    children = models.ManyToManyField('self',  symmetrical=False, related_name='mychildren',blank =True)
    parents = models.ManyToManyField('self',  symmetrical=False,related_name='myparents', blank =True)
    spouse = models.ManyToManyField('self', related_name = "spouse", blank =True)
    siblings = models.ManyToManyField('self', related_name="siblings", blank =True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    occupation = models.CharField(max_length=128, blank=True)
    def __unicode__(self):
        return self.first_name + " " + self.last_name

class greeterID(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    churchGoer =  models.OneToOneField(churchGoer)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
        
#the following functions handle reverse relationships.  
#If someone is a child, then obviously another person is a parent
#if someone declares the he/she has children then go to each of those children, 
#clear the parents and re add the parent that we just connected

def connect_child(sender, instance, action, reverse, model, pk_set, **kwargs):
    if not reverse:
        if action == "post_clear":
            instance.myparents.clear()
            print "removed parents in all children"
            for child in instance.children.all():
                instance.myparents.add(child)
                print "Adding ", instance, " a parent of ", parent
                    # cg.mychildren.add(instance)
                    # print "Making ", cg, " a child of ", instance
    if pk_set:
        if action == "post_add":
            for parent in pk_set:
                print 'save parent', parent
                # when you add Bob as parent, them bob meeds his list of children updated to match this.
                if not reverse:
                    instance.myparents.add(parent)
                    cg = churchGoer.objects.get(pk=parent)
                    print "Making ", cg, " a child of ", instance
                    # cg.mychildren.add(instance)
                    # print "Making ", cg, " a child of ", instance

def connect_parent(sender, instance, action, reverse, model, pk_set, **kwargs):

    if not reverse:
        if action == "post_clear":
            instance.mychildren.clear()
            print "removed child in all parents"
            for parent in instance.parents.all():
                instance.mychildren.add(parent)
                print "Removing ", instance, " a parent of ", parent
                    # cg.mychildren.add(instance)
                    # print "Making ", cg, " a child of ", instance
    if pk_set:
        if action == "post_add":
            for child in pk_set:
                print 'save child', child
                if not reverse:
                    instance.mychildren.add(child)
                    cg = churchGoer.objects.get(pk=child)
                    print "Making ", cg, " a parent of ", instance
                    # cg.myparents.add(instance)
                    # print "Making ", cg, " a child of ", instance


m2m_changed.connect(connect_child, sender=churchGoer.children.through, weak=False)
m2m_changed.connect(connect_parent, sender=churchGoer.parents.through, weak=False)