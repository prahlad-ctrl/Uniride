from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.paginator import Paginator 
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from .models import *

def sign_up(request):

    if request.method == 'POST':

        data = request.POST

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        student_id = data.get('university_id')
        phone_number = data.get('phone_number')
        year = data.get('year')
        sem = data.get('Semester')
        college_name = data.get('college_name', '')
        branch_name = data.get('branch_name', '')
        personal_address = data.get('personal_address', '')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'User already exists'
            })
        elif confirm_password!=password:
            return render(request, 'signup.html', {
                'error': 'Password doesnt matches'
            })
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
        except IntegrityError:
            return render(request, 'signup.html', {
                'error': 'User already exists'
            })
        Account.objects.create(
            user=user,
            college_name=college_name,
            branch_name=branch_name,
            student_id=student_id,
            phone_number=phone_number,
            year=year,
            sem=sem,
            personal_address=personal_address
        )

        return redirect('login')

    return render(request, 'signup.html')
     
def login_page(request):
    if request.method=='POST':
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None and "@" in username:
            matched_user = User.objects.filter(email__iexact=username).first()
            if matched_user is not None:
                user = authenticate(request, username=matched_user.username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard") 
        else:
            error='Incorrect Credentials '
            return render(request,'login.html',{'error':error})
    return render(request, "login.html")

@login_required
def dashboard(request):
    user_account = request.user.account
    context = {
        'user': request.user,
        'account': user_account,
    }
    return render(request, "dashboard.html",context)

@login_required
def show_rides(request):
    queryset = PublishRide.objects.all()

    from_location = request.GET.get('from_location')
    to_location = request.GET.get('to_location')
    date = request.GET.get('travel_date')
    time = request.GET.get('travel_time')

    if from_location and to_location and date and time:
        queryset = queryset.filter(
            from_where=from_location,
            to_where=to_location,
            date=date,
            time=time
        )

    paginator = Paginator(queryset, 10)
    pg_no = request.GET.get('page', 1)
    pg_obj = paginator.get_page(pg_no)

    return render(request, 'dashboard.html', {
        'page_obj': pg_obj,
        'user': request.user,
        'account': request.user.account,
        'from_location': from_location,
        'to_location': to_location,
        'travel_date': date,
        'travel_time': time,
    })

@login_required
def post_ride(request):
    msg=None 
    if request.method=='POST':
        try:
            vehicle = request.user.account.vehicle
        except ObjectDoesNotExist:
            msg='Please Register your Vehicle first'
            return redirect('register_vehicle')
        if vehicle:
            from_where = request.POST.get("from_where")
            to_where = request.POST.get("to_where")
            travel_date = request.POST.get("travel_date")
            travel_time = request.POST.get("travel_time")
            PublishRide.objects.create(
                from_where=from_where,
                rider_account=request.user.account,
                to_where=to_where,
                date=travel_date,
                time=travel_time,
            )
            msg='ride Published'
            return render(request,'post_ride.html',{'msg':msg})   
    return render(request,'post_ride.html')

@login_required 
def publish_vehicle(request):
    msg=None 
    if request.method=='POST':
        try:
            existing_vehicle = request.user.account.vehicle
            msg='You have already registered your vehicle'
            return render(request,'register_vehicle.html',{'msg':msg})
        except ObjectDoesNotExist:
            vehicle_model = request.POST.get("vehicle_model")
            vehicle_number = request.POST.get("vehicle_number")
            Vehicle.objects.create(
                account_id=request.user.account,
                vehicle_model=vehicle_model,
                vehicle_number=vehicle_number
            )
            msg='vehicle registered'
            return render(request,'register_vehicle.html',{'msg':msg})
    return render(request,'register_vehicle.html')



@login_required
def profile(request):
    user_account = request.user.account
    context = {
        'user': request.user,
        'account': user_account
    }
    return render(request,'profile.html',context=context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def rider_profile(request, ride_id):
    ride = get_object_or_404(PublishRide, id=ride_id)
    rider_account = ride.rider_account
    back_query = request.GET.urlencode()
    return render(request, 'rider_profile.html', {
        'ride': ride,
        'rider': rider_account,
        'back_query':back_query
    })
