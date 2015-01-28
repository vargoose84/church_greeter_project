from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from greeter.models import churchGoer, greeterID, greeterRecord
from django.contrib.auth.decorators import login_required
from greeter.forms import UserForm, UserProfileForm, churchGoerForm, QuizForm
from django.db.models import Max, Min
from random import randint, shuffle
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

            goer = form.save(commit=False)
            # goer.save()
            # form.save_m2m()
            # form.save(commit=True)

            for t in greeterID.objects.all():
                greeterRecord.objects.get_or_create(churchGoer=goer, trainerID=t)

            churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
            context_dict = {'churchGoers' : churchGoer_list, 'goer' : goer, 'add' : True}
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
        form = churchGoerForm(request.POST, request.FILES,instance=goer)

        if  form.is_valid():
            goer = form.save(commit=False)
            print request.POST.getlist('parents')
            print request.POST.getlist('children')
            print form.cleaned_data.get('children')
            print form.cleaned_data.get('parents')
            print goer.mychildren.all()
            print goer.mychildren.clear()
            print goer.myparents.all()
            goer.save()
            form.save_m2m()
            form.save(commit=True)
            churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
            context_dict = {'churchGoers' : churchGoer_list, 'goer' : goer}
            return render_to_response('greeter/bio.html',context_dict, context)
        else:
            print churchGoerForm.errors

    else:
        form = churchGoerForm(instance=goer)
        churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
    return render_to_response(
            'greeter/add_goer.html',
            {'form': form, 'goer' : goer},
            context)

def getBio(request, goerID):
    context = RequestContext(request)
    goer = churchGoer.objects.get(pk=goerID)
    churchGoer_list = churchGoerListCreator(type=request.session.get('listType'), goerID = request.user.pk)
    context_dict = {'churchGoers' : churchGoer_list, 'goer' : goer}
    return render_to_response('greeter/bio.html',context_dict, context)




def getChurch(request,  listType='all'):
    context = RequestContext(request)
    curUser=None
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
def quiz(request):
    context = RequestContext(request)
    if request.method =='POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            bob = 5

    else:

        myMax = churchGoer.objects.aggregate(Max('id'))['id__max']
        toLearnList = greeterRecord.objects.filter(flag=False)
        myTestSubject = getRandom(toLearnList).churchGoer
        myMultipleChoiceField = [myTestSubject.pk,]
        myPopulation = [(myTestSubject.pk ,myTestSubject),]
        print myMultipleChoiceField
        while len(myMultipleChoiceField) < 4 and len(myMultipleChoiceField) < churchGoer.objects.count() :
            candidate = randint(0,myMax)
            if candidate not in myMultipleChoiceField:
                if churchGoer.objects.filter(pk=candidate):
                    myMultipleChoiceField.append(candidate)
                    myPopulation += ( candidate, churchGoer.objects.get(pk=candidate) ),
        shuffle(myPopulation)
        data = {'Answer' : myTestSubject.pk}
        form = QuizForm(data, extra=myPopulation)
        context_dict = {'population' : myPopulation,'form': form, 'goer' : myTestSubject }
        return render_to_response('greeter/quiz.html', context_dict, context)
def getRandom(liste):
    rv = liste[randint(0,len(liste)-1)]
    return rv