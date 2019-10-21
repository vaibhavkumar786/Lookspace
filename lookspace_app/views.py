from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User
from django.contrib.auth import login
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import PartnerSignUpForm, CustomerSignUpForm , SpaceDetailsForm
from django.contrib.auth.decorators import login_required
from .models import SpaceDetails , BookedSeats
from datetime import *

# Create your views here..

def home_page(request):
    return render(request, 'lookspace_app/home_page.html')

# def index(request):
#     return render(request, 'lookspace_app/index.html', {})

class SignUpView(TemplateView):
    template_name = 'lookspace_app/signup.html'


# def home(request):
#     if request.user.is_authenticated:
#         if request.user.is_partner:
#             return redirect('partners:quiz_change_list')
#         else:
#             return redirect('customers:quiz_list')
#     return render(request, 'lookspace_app/home.html')

def index(request):
    if request.user.is_authenticated:
        if request.user.is_partner:
            return redirect('partners:quiz_change_list')
        else:
            return redirect('customers:quiz_list')
    return render(request, 'lookspace_app/html/index.html')

def user_signup(request):
    return render(request, 'lookspace_app/html/user_signup.html')

def user_signin(request):
    return render(request, 'lookspace_app/html/user_signin.html')

def partner_signup(request):
    return render(request, 'lookspace_app/html/partner_signup.html')

def partner_signin(request):
    return render(request, 'lookspace_app/html/partner_signin.html')


class PartnerSignUpView(CreateView):
    model = User
    form_class = PartnerSignUpForm
    template_name = 'lookspace_app/html/user_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'partner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        print("Hello")
        login(self.request, user)
        print("Hello3")
        return redirect('partners:quiz_change_list')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'lookspace_app/html/user_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        print("Hello3")

        login(self.request, user)
        print("Hello4")
        return redirect('customers:quiz_list')

def space_details_subsriptions(request):
    if request.method == "POST":
        space = SpaceDetails(user = request.user, space_type = request.POST.get("space_type"), seater = request.POST.get("seater"), total_quantity = request.POST.get("total_quantity"), time = request.POST.get("time"), price = request.POST.get("price"))
        space.save()
    return render(request, 'lookspace_app/register_space_details.html', { })

@login_required
def all_space_details(request):
    current_user = request.user
    print("current ================", current_user.id)
    all_data = SpaceDetails.objects.filter(user=current_user.id)
    return render(request, 'lookspace_app/space_details.html', {'all_data':all_data} )

@login_required
def edit_space_details(request, id):
    all_data = SpaceDetails.objects.get(id=id)

    if request.method == "POST" :
        all_data.space_type = request.POST.get("space_type")
        all_data.total_quantity = request.POST.get("total_quantity")
        all_data.seater = request.POST.get("seater")
        all_data.time = request.POST.get("time")
        all_data.price = request.POST.get("price")
        all_data.save()

    return render(request, 'lookspace_app/edit_details.html', {'all_data':all_data} )

@login_required
def delete_space_details(request, id):
    SpaceDetails.objects.filter(id=id).delete()

    return render(request, 'lookspace_app/space_details.html', {} )

@login_required
def all_unique_space(request):
    all_data = SpaceDetails.objects.all()
    return render(request, 'lookspace_app/unique_space.html', {'all_data':all_data})

@login_required
def all_available_spaces(request, id):
    all_data = SpaceDetails.objects.get(id=id)
    if request.method == "POST":
        book_space = BookedSeats(space=all_data ,user = request.user, start_date = request.POST.get("start_date"), end_date = request.POST.get("end_date"), start_time = request.POST.get("start_time"), end_time = request.POST.get("end_time"))
        book_space.save()
    return render(request, 'lookspace_app/book_space.html', {'all_data':all_data} )

@login_required
def all_user_booking_details(request):
    all_data = BookedSeats.objects.filter(user = request.user)
    return render(request, 'lookspace_app/my_booking_details.html', {'all_data':all_data} )

@login_required
def partner_space_booked_details(request):
    all_data = BookedSeats.objects.filter(user = request.user)
    return render(request, 'lookspace_app/partner_space_booked.html', {'all_data':all_data} )

@login_required
def check_availability_spaces(request, id):
    booked_data = BookedSeats.objects.filter(space__id = id)
    first_date=request.GET.get("start_date")
    second_date=request.GET.get("end_date")
    first_time=request.GET.get("start_date")
    second_time=request.GET.get("end_date")

    first_date = str(first_date).split('-')
    second_date = str(second_date).split('-')
    first_time = str(first_time).split('-')
    second_time = str(second_time).split('-')

    if first_date == ['None']:
        date_today = str(date.today()).split('-')
        first_date = date_today
        second_date = date_today
        first_time = date_today
        second_time = date_today

    print(first_date)

    comment = ""
    check = False
    for dates in booked_data:
        st_date= str(dates.start_date).split('-')
        en_date = str(dates.end_date).split('-')
        st_time = str(dates.start_time).split('-')
        en_time = str(dates.end_time).split('-')

        y1, m1, d1 = st_date
        y2, m2, d2 = first_date

        y3, m3, d3 = en_date
        y4, m4, d4 = second_date
        print(st_date,en_date,first_date,second_date)
        b1 = date(int(y1), int(m1), int(d1))
        b2 = date(int(y2), int(m2), int(d2))

        if int(y2) == int(y1) and int(y3) == int(y4):
            if int(m2) == int(m1) and int(m3) == int(m4):
                if int(d2) == int(d1) and int(d3) == int(d4):
                    check = True
                elif (d1 >= d2 and d3 <= d2) or (d1 >= d4 and d3 <= d2) or (d2 >= d1 and d4 <= d1) or (d2 >= d3 and d4 <= d3) :
                    check = False
                else:
                    check = True
            elif (m1 >= m2 and m3 <= m2) or (m1 >= m4 and m3 <= m2) or (m2 >= m1 and m4 <= m1) or (m2 >= m3 and m4 <= m3):
                check = False
            else:
                check= True
        elif (y1 >= y2 and y3 <= y2) or (y1 >= y4 and y3 <= y2) or (y2 >= y1 and y4 <= y1) or (y2 >= y3 and y4 <= y3):
            check = False
        else:
            check = True

        if check == True:
            break

    if check == False:
        comment = "Sorry, Please choose another date and time"
    else:
        comment = "Your date is available"

    return render(request, 'lookspace_app/availabilities.html', {'booked_data':booked_data, 'comment':comment} )



