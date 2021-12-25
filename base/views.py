from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn Python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'

    #  If User is already logined, Prevent User to re-login
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            # Check if User existed in DB
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # If User existed,
        # Check Credential is correct
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log User in, also create SessionToken in Browser's Cookie and DB
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    # Logout User, also delete SessionToken in Browser's Cookie
    logout(request)
    return redirect('home')


def registerPage(request):
    # page = 'register'
    # Use built-in Django Form-Creation to create a Form
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)  #Passing Datas
        if form.is_valid():
            user = form.save(commit=False)   #Return User, But not Saving yet
            user.username = user.username.lower()   #Clean data
            user.save()     #Then, Save the User to DB
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'An Error occured during registration')
        
    return render(request, 'base/login_register.html', {'form':form})



def home(request):

    # Same with W ? T : F
    # q is either a topic or ''
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Dynamic Search
    # Search for item that found in topic's name OR name OR description
    #
    # icontains : atleast contains the given argument
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    room_count = rooms.count()

    #This var will be show in Recent Activity bar
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages,
        }
    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    # room_messages = room.message_set.all().order_by('-created')   #Order by the newest
    room_messages = room.message_set.all()  #Ordering in html's class
    participants = room.participants.all()  #For M2M relationship, No need "_set"

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room':room, 
        'room_messages':room_messages, 
        'participants':participants
        }
    return render(request, 'base/room.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user':user, 
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics
        }
    return render(request, 'base/profile.html', context)



"""
 Only Logined User can call these below functions (create, update, delete)
 If not yet Logined, Redirect to Login Page

"""
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        # Get user inputed Topic
        topic_name = request.POST.get('topic')
        # If the user inputed Topic existed in DB, get it.
        # Else create a new Topic to DB
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)   #Fill Form with the above Room's data
    topics = Topic.objects.all()

    # Block User who's not the Room owner from update Room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # Block User who's not the Room owner to delete Room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    # Block User who's not the Room owner to delete Room
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')

    if request.method == "POST":
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user) #Get User data

    if request.method == "POST":
        # Pass data from [request.POST] to [user]
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})