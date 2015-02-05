from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from greeter.models import churchGoer, greeterID, greeterRecord
from django.contrib.auth.decorators import login_required
from greeter.forms import UserForm, UserProfileForm, churchGoerForm, QuizForm, SuggestionForm
from django.db.models import Max, Min
from random import randint, shuffle
def index(request):
    context = RequestContext(request)
    churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
    context_dict = {'churchGoers' : churchGoer_list}
    return render_to_response('greeter/index.html',context_dict, context)

@login_required
def addGoer(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = churchGoerForm(request.POST, request.FILES)
        if form.is_valid():
            goer = form.save()
            #add this new churchgoer to all Greeters list of people to learn
            for t in greeterID.objects.all():
                greeterRecord.objects.get_or_create(churchGoer=goer, trainerID=t)
            churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
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
            goer.save()
            form.save_m2m()
            form.save(commit=True)
            churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
            context_dict = {'churchGoers' : churchGoer_list, 'goer' : goer}
            return render_to_response('greeter/bio.html',context_dict, context)
        else:
            print churchGoerForm.errors

    else:
        form = churchGoerForm(instance=goer)
        churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
    return render_to_response(
            'greeter/add_goer.html',
            {'form': form, 'goer' : goer},
            context)
#This function returns all fields of a churchGoer and presents them
def getBio(request, goerID):
    context = RequestContext(request)
    goer = churchGoer.objects.get(pk=goerID)
    churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
    context_dict = {'churchGoers' : churchGoer_list, 'goer' : goer}
    return render_to_response('greeter/bio.html',context_dict, context)



#This function lists all churchgoers of a certain type in a table
#It also persists that type after clicking anywhere in the site
#meaning the sidebar will hold it's "learned,unlearned, all value"
def getChurch(request,  listType='all'):
    context = RequestContext(request)
    request.session['listType']=listType
    print request.user, listType
    context_dict = []
    churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
    context_dict = {'churchGoers' : churchGoer_list}
    return render_to_response('greeter/getChurch.html', context_dict, context)
#this function registers a new trainer
#some of this is a copy paste of the website training functions
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            #After saving the new Greeter, we need to populate his list of people to learn
            for c in churchGoer.objects.all():
                greeterRecord.objects.get_or_create(churchGoer=c, trainerID=profile)
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
            'greeter/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
#this is another copy pasted function from the training app
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/greeter/')

#this is another copy pasted and modified function from the training app
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['listType'] = 'unlearned'
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/greeter/')
            else:
                context_dict = {'bold_message': "Whooops your account is disabled"}
                return render_to_response('greeter/ERROR.html', context_dict, context)
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict = {'bold_message': "WRONG Details DUUUUUDE"}
            return render_to_response('greeter/ERROR.html', context_dict, context)
    else:
        return render_to_response('greeter/login.html', {}, context)
#This function returns a list based on the type variable: learned, unlearned, all
#This list queries the database based on the signed in user
def churchGoerListCreator(quest, type):
    churchGoer_list=[]

    if quest.user.is_authenticated:
        greeter=[]
        greeter = greeterID.objects.filter(user_id=quest.user.pk)
        if type == 'learned':
            for record in greeterRecord.objects.filter(trainerID=greeter, flag=True):
                churchGoer_list.append(record.churchGoer)

        elif type == 'unlearned':
            for record in greeterRecord.objects.filter(trainerID=greeter, flag=False):
                churchGoer_list.append(record.churchGoer)

        elif type == 'reset':
            for record in greeterRecord.objects.filter(trainerID=greeter, flag=True):
                record.flag = False
                record.save()
    else:
        churchGoer_list = churchGoer.objects.all()
    return churchGoer_list
#if the user wishes to change the goerID to learned status, or if through the quiz the user succeeds in memorizing the goerID ,
#we'll mark the flag as true
@login_required
def greeterRecordChange(request, goerID):
    context = RequestContext(request)

    curTrainerID=greeterID.objects.filter(user_id=request.user.pk)
    goer = churchGoer.objects.get(pk=goerID)
    currentRecord = greeterRecord.objects.get(trainerID=curTrainerID, churchGoer=goer)
    currentRecord.flag = True
    currentRecord.save()
    churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
    context_dict = {'churchGoers' : churchGoer_list}
    return render_to_response('greeter/getChurch.html', context_dict, context)
#This is the quiz code it's complicated:
#   Whenever the "Take my Quiz", or quiz Submit button is pressed
#   We are going to get a random person who is unlearned to the user for testing
#       and then also grab 3 other randomly selected church goers to create the multiple choice field
#   If the user answers correctly increment the quiz score property,
#       otherwise decrease it
@login_required
def quiz(request):
    context = RequestContext(request)
    message = ''
    Answer = None
    curTrainerID = greeterID.objects.filter(user_id=request.user.pk)
    churchGoer_list = churchGoerListCreator(quest=request, type=request.session.get('listType'))
    myMax = churchGoer.objects.aggregate(Max('id'))['id__max']
    toLearnList =churchGoerListCreator(quest=request, type='unlearned')
    myTestSubject = getRandom(toLearnList)
    myMultipleChoiceField = [myTestSubject.pk,]
    myPopulation = [(myTestSubject.pk ,myTestSubject),]

    while len(myMultipleChoiceField) < 4 and len(myMultipleChoiceField) < churchGoer.objects.count():
        candidate = randint(0,myMax)
        if candidate not in myMultipleChoiceField:
            if churchGoer.objects.filter(pk=candidate):
                myMultipleChoiceField.append(candidate)
                myPopulation += (candidate, churchGoer.objects.get(pk=candidate)),
    shuffle(myPopulation)
    data = {'Answer' : (myTestSubject.pk, myTestSubject)}
    if request.method =='POST':
        form = QuizForm(request.POST)
        temp = request.POST.getlist('Answer')[0]
        temp = temp[1]
        Answer = churchGoer.objects.get(pk=temp)
        gr=greeterRecord.objects.get(trainerID_id=curTrainerID, churchGoer=Answer)
        if temp == request.POST.getlist('population')[0]:
            gr.quizScore += 1
            if gr.quizScore >=3:
                gr.flag = True
            message = "Correct!"
        else:
            gr.quizScore -= 1
            message =  'Incorrect! '
        gr.save()
    form = QuizForm(initial=data, extra=myPopulation)
    context_dict = {'form': form, 'goer' : myTestSubject, 'message' : message, 'incorrectAnswer': Answer, 'churchGoers':churchGoer_list}
    return render_to_response('greeter/quiz.html', context_dict, context)
#mini function to return a random object in a list
def getRandom(liste):
    rv = liste[randint(0,len(liste)-1)]
    return rv

def postSuggestion(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        print form
        if form.is_valid():
            mySuggestion = form.save(commit=False)
            
            if mySuggestion.category:
                mySuggestion.save()
                form.save()
            else:
                mySuggestion.category = form.add_category
            return HttpResponseRedirect('greeter/index.html')
            
        else:
            print form.errors
    else:
        curTrainerID = greeterID.objects.get(user_id=request.user.pk)
        form = SuggestionForm(greeter=curTrainerID)
    return render_to_response('greeter/GiveSuggestion.html',{'form': form}, context)
        
        