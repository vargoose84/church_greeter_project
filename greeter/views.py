from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from greeter.models import churchGoer, greeterID, greeterRecord
from django.contrib.auth.decorators import login_required
from greeter.forms import UserForm, UserProfileForm, churchGoerForm

def index(request):
    context = RequestContext(request)        
    churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
    context_dict = {'churchGoers' : churchGoer_list}
    return render_to_response('greeter/index.html',context_dict, context)

@login_required
def addGoer(request):
    context = RequestContext(request)
    
    print request.FILES
    if request.method == 'POST':
        form = churchGoerForm(request.POST, request.FILES)
        if form.is_valid():
            
            goer = form.save()
            print request.FILES
            for t in greeterID.objects.all():
                greeterRecord.objects.get_or_create(churchGoer=goer, trainerID=t)
            for s in goer.sons.all():
                s.parents.add(goer)
                s.save()
            for d in goer.daughters.all():
                d.parents.add(goer)
                d.save()
            for spouse in goer.spouse.all():
                spouse.spouse.add(goer)
                spouse.save()
            for sibling in goer.siblings.all():
                sibling.siblings.add(goer)
                sibling.save()
            c = form.save()
            churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
            context_dict = {'churchGoers' : churchGoer_list, 'goer' : c, 'add' : True}
            return render_to_response('greeter/bio.html',context_dict, context)
                
        else:
            print form.errors

    else:
        form = churchGoerForm()
    return render_to_response('greeter/add_goer.html', {'form':form}, context)
@login_required
def modifyGoer(request,goerID):
    context = RequestContext(request)
    goer = churchGoer.objects.get(pk=goerID)
    print request.FILES
    if request.method == 'POST':
        form = churchGoerForm(request.POST, request.FILES)
        goer = form.save()
        for o in  churchGoer.objects.filter(parents=goer):
            o.parents.remove(goer)
            o.save()
        for o in  churchGoer.objects.filter(sons = goer):
            o.sons.remove(goer)
            o.save()
        for o in  churchGoer.objects.filter(daughters = goer ):
            o.daughters.remove(goer) 
            o.save()            
        for o in  churchGoer.objects.filter(siblings = goer):
            o.siblings.remove(goer)
            o.save()
        for o in  churchGoer.objects.filter(spouse = goer):
            o.spouse.remove(goer)
            o.save()
            
        for s in goer.sons.all():
            s.parents.add(goer)
            s.save()
        for d in goer.daughters.all():
            d.parents.add(goer)
            d.save()
        for spouse in goer.spouse.all():
            spouse.spouse.add(goer)
            spouse.save()
        for sibling in goer.siblings.all():
            sibling.siblings.add(goer)
            sibling.save()
        
        if  form.is_valid():
            c = form.save()
            churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
            context_dict = {'churchGoers' : churchGoer_list, 'goer' : c}
            return render_to_response('greeter/bio.html',context_dict, context)
        else:
            print churchGoerForm.errors

    else: 
        form = churchGoerForm(instance=goer)
        churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
    return render_to_response(
            'greeter/add_Goer.html',
            {'form': form, 'goer' : goer},
            context)

def getBio(request, goerID):
    context = RequestContext(request)
    c = churchGoer.objects.get(pk=goerID)
    churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
    sons = c.sons.all()
    daughters = c.daughters.all()
    parents = c.parents.all()
    siblings = c.siblings.all()
    
    context_dict = {'churchGoers' : churchGoer_list, 'goer' : c, 'sons' : sons, 'daughters' : daughters, 'parents' : parents, 'siblings' : siblings}
    return render_to_response('greeter/bio.html',context_dict, context)




def getChurch(request,  listType='all'):
    context = RequestContext(request)
    request.session['listType']=listType
    print request.user, listType
    context_dict = []
    if request.user.is_authenticated():
        curUser = greeterID.objects.get(id = request.user.id)
        churchGoer_list =churchGoerListCreator(type=request.session.get('listType'), goerID = curUser)
        context_dict = {'churchGoers' : churchGoer_list}
    return render_to_response('greeter/getChurch.html', context_dict, context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()
            for c in churchGoer.objects.all():
                greeterRecord.objects.get_or_create(churchGoer=c, trainerID=profile)
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'greeter/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/greeter/')


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        request.session['listType'] = 'unlearned'
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/greeter/')
            else:
                # An inactive account was used - no logging in!
                context_dict = {'bold_message': "Whooops your account is disabled"}
                return render_to_response('greeter/ERROR.html', context_dict, context)
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict = {'bold_message': "WRONG Details DUUUUUDE"}
            return render_to_response('greeter/ERROR.html', context_dict, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('greeter/login.html', {}, context)

def churchGoerListCreator(type, goerID=None):
    churchGoer_list=[]  
    if type == 'learned':
        for record in greeterRecord.objects.filter(trainerID=goerID, flag=True):
            churchGoer_list.append(record.churchGoer)
        
    elif type == 'unlearned':
        for record in greeterRecord.objects.filter(trainerID=goerID, flag=False):
            churchGoer_list.append(record.churchGoer)
    elif type == 'reset':
        for record in greeterRecord.objects.filter(trainerID=goerID, flag=True):
            record.flag = False
            record.save()
        
        
    else:
        churchGoer_list = churchGoer.objects.all()
    return churchGoer_list
def greeterRecordChange(request, goerID):
    context = RequestContext(request)
    
    curTrainerID=greeterID.objects.get(id = request.user.id)
    goer = churchGoer.objects.get(pk=goerID)
    currentRecord = greeterRecord.objects.get(trainerID=curTrainerID, churchGoer=goer)
    currentRecord.flag = True
    currentRecord.save()
    curUser = greeterID.objects.get(id = request.user.id)
    churchGoer_list =churchGoerListCreator(type=request.session.get('listType'), goerID = curUser)
    context_dict = {'churchGoers' : churchGoer_list}
    return render_to_response('greeter/getChurch.html', context_dict, context)
    
    