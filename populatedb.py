import os

def populate():
    a = add_churchGoer(fn="bob", ln="vila", bd="2015-05-15", pic='media/profile_images/rango.jpg')
    print "Created BobVila"
    b = add_greeter(un="vila", gid=a)
    print "made him a greeter"
    a= add_churchGoer(fn="Larry", ln="Bird", bd="2015-05-15")
    b = add_greeter(un="LarryB", gid=a)
    add_churchGoer(fn="Bob", ln="vila", bd="2015-05-15")
    add_churchGoer(fn="Trisha", ln="Peterson", bd="2015-05-15")
    add_churchGoer(fn="Mike", ln="Costanza", bd="2015-05-15")
    add_churchGoer(fn="Elliott", ln="Erickson", bd="2015-05-15")
    a=add_churchGoer(fn="Bob", ln="Hagie", bd="2015-05-15")
    b = add_greeter(un="BobH", gid=a)

def add_churchGoer(fn,ln,bd,pic=None):
    c = churchGoer.objects.create(first_name=fn, last_name=ln, birthdate=bd)
    if pic:
        c.picture = pic
        c.save()
        print "added Pic"
        
    populateGreeter(churchGoer=c)
    return c
def add_greeter(un,gid,pw="ooblec"):
    from django.contrib.auth.models import User
    u , created = User.objects.get_or_create(username = un, password = pw)
    if created:
        g, result = greeterID.objects.get_or_create(user=u, churchGoer=gid)
        populateList(greeter=g)
        return g
def populateList(greeter):
    for c in churchGoer.objects.all():
        greeterRecord.objects.get_or_create(churchGoer=c, trainerid=greeter)

        
        
    
def populateGreeter(churchGoer):
    for g in greeterID.objects.all():
        greeterRecord.objects.get_or_create(churchGoer=churchGoer, trainerid=g)
        
        
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_greeter_project.settings')
    from greeter.models import greeterID, churchGoer, greeterRecord
    populate()