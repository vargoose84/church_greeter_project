from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import *

class greeterRecord(models.Model):
    trainerID = models.ForeignKey('greeterID')
    churchGoer = models.ForeignKey('churchGoer')
    flag = models.BooleanField(default=False)
    quizScore = models.IntegerField(default=0)
    
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
    # def add_familyRelation(self, goer, symm=True):
        # familyRelation, created = familyRelation.objects.get_or_create(from_person = self, to_person = goer)
        # if symm:
            # goer.add_familyRelation(self
        # return familyRelation
    # def remove_familyRelation(self, person, symm=True ):
        # familyRelation.objects.filter(from_person=self,to_person=person).delete()
    # def get_parents(self):
        # return self.parents.filter(from_people__to_person=self)
    # def get_children(self):
        # return self.children.filter(from_people__to_person=self)
    
        
    
    
class familyRelation(models.Model):
    from_person = models.ForeignKey(churchGoer, related_name='from_people')
    to_person = models.ForeignKey(churchGoer, related_name='to_people')

    
        
class greeterID(models.Model):
    # This line is required. Links UserProfi    le to a User model instance.
    user = models.OneToOneField(User)
    churchGoer =  models.OneToOneField(churchGoer) 

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


def connect_child(sender, instance, action, reverse, model, pk_set, **kwargs):
    # print "connect.child called with action '%s'" %action
    # print "reverse?", reverse
    # print "Instance=",instance.id
    # print "primary_key=", pk_set
    if not reverse:
        if action == "post_clear":   
            instance.myparents.clear()
            print "removed parents in all children"
            for child in instance.children.all():
                instance.myparents.add(child)
                print "Removing ", instance, " a parent of ", parent
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
    # print "connect.parent called with action '%s'" %action
    # print "reverse?", reverse
    # print "Instance=",instance.id
    # print "primary_key=", pk_set
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
                # when you add Bob as parent, them bob meeds his list of children updated to match this. 
                if not reverse:
                    instance.mychildren.add(child)
                    cg = churchGoer.objects.get(pk=child)
                    print "Making ", cg, " a parent of ", instance
                    # cg.myparents.add(instance)
                    # print "Making ", cg, " a child of ", instance
                
m2m_changed.connect(connect_child, sender=churchGoer.children.through, weak=False)
m2m_changed.connect(connect_parent, sender=churchGoer.parents.through, weak=False)
