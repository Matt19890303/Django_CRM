from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, RecordForm, UpdateOwnerForm
from .models import Record
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test


@login_required
def home(request):
    # This grabs everthing in the table and puts it into the records variable
    if request.user.is_authenticated:
        query = request.GET.get('q')
        owner_filter = request.GET.get('owner')
        records = Record.objects.all()
        if owner_filter:
            records = records.filter(owner__username=owner_filter)
        if query:
            records = Record.objects.filter(
                Q(owner=request.user) &
                (Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query) |
                Q(zipcode__icontains=query))
            )
        owners = User.objects.all()
        return render(request, 'home.html', {'records': records, 'owners': owners})
    else:
        return render(request, 'home.html', {})
    
def login_user(request):
    # return render(request, 'login.html')
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def logout_user(request):
    messages.success(request, 'Successfully logged out')
    logout(request)
    return redirect('login')

# Display records
def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'You must be logged in to view that page')
        return redirect('login')

# Delete record 
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record deleted successfully')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to delete a record')
        return redirect('home')

def add_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RecordForm(request.POST or None)
            if form.is_valid():
                record = form.save(commit=False)
                record.owner = request.user
                record.save()
                messages.success(request, 'Record added successfully')
                return redirect('home')
        else:
            form = RecordForm()
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to add a record')
        return redirect('home')

# Update record
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = RecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated!')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to update a record')
        return redirect('home')

# Adding columns

@user_passes_test(lambda u: u.is_superuser)
def staff_members(request):
    # users = User.objects.all()
    # return render(request, 'staff_members.html', {'users': users})
    if request.user.is_authenticated:
        query = request.GET.get('sm')
        users = User.objects.all()
        if query:
            users = User.objects.filter((
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                # Q(is_staff__icontains=query) |
                Q(is_superuser__icontains=query))
            )
        return render(request, 'staff_members.html', {'users': users})
    else:
        return render(request, 'staff_members.html', {})
    
def add_owner(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.is_superuser = request.POST.get('is_superuser') == 'on'
            user.save()
            return redirect('staff_members')
    else:
        form = UserCreationForm()
    return render(request, 'add_owner.html', {'form': form})


def update_owner(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UpdateOwnerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('staff_members')
    else:
        form = UpdateOwnerForm(instance=user)
    return render(request, 'update_owners.html', {'form': form})

def owner_record(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        return render(request, 'owners_record.html', {'user': user})
    else:
        messages.success(request, 'You must be logged in to view that page')
        return redirect('login')
    