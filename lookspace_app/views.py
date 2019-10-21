from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import User
from django.contrib.auth import login
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import PartnerSignUpForm, CustomerSignUpForm , SpaceDetailsForm
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import *
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import Count
import  time
from datetime import datetime
from time import mktime
# Create your views here..

def home_page(request):
    return render(request, 'lookspace_app/home_page.html')

class SignUpView(TemplateView):
    template_name = 'lookspace_app/signup.html'


def error_404_view(request, exception):
    return render(request,'lookspace_app/html/404.html')

def schedule_visit(request):
    if request.method == 'POST':
        customer_name = request.POST.get("customer_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        company_name = request.POST.get("company_name")
        visit_date = request.POST.get("visit_date")
        visit_time = request.POST.get("visit_time")
        visit_info = ScheduleVisit(customer_name = customer_name, email = email, phone = phone_number,
        company_name = company_name, date = visit_date, time = visit_time)
        visit_info.save()
        send = customer_name+'\n' + email + '\n' + phone_number + '\n' + company_name + '\n' + visit_date + '\n' + visit_time
        send_mail(
        'Testing Email',
        send,
        'vaibhav.kumar@mountblue.io',
        ['vaibhav.at.kumar@gmail.com'],
        fail_silently = False
        )
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'lookspace_app/html/schedule_visit.html')

def thank_you(request):
     return render(request, 'lookspace_app/html/thankyou_page.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_info = ContactForm(contact_name = name, email = email, message = message)
        contact_info.save()
        send = name + '\n' + email + '\n' + message
        send_mail(
        'Testing Email',
        send,
        'vaibhav.kumar@mountblue.io',
        ['vaibhav.at.kumar@gmail.com'],
        fail_silently = False
        )
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'lookspace_app/html/contact.html')

def index(request):
    if request.user.is_authenticated:
        if request.user.is_partner:
            return redirect('partners:quiz_change_list')
        else:
            return redirect('customers:quiz_list')
    return render(request, 'lookspace_app/html/index.html')


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
    # all_data = BookedSeats.objects.filter(user = request.user)
    # data = BookedSeats.objects.values('space_id').annotate(count=Count('space_id'))
    space = SpaceDetails.objects.filter(user_id=request.user.id)

    final = []
    count =0
    for data in space:
        for d in data.bookedseats_set.all():
            data_value = {}
            count +=1
            data_value['start_date'] = d.start_date
            data_value['start_time'] = d.start_time
            data_value['end_date'] = d.end_date
            data_value['end_time'] = d.end_time
            data_value['space'] = d.space
            c = User.objects.get(id=d.user_id)

            data_value['username'] = c.username
            final.append(data_value)

    return render(request, 'lookspace_app/partner_space_booked.html', {'space':space,'final':final,}  )

@login_required
def check_availability_spaces(request, id):
    booked_data = BookedSeats.objects.filter(space__id = id)
    first_date=request.GET.get("start_date")
    second_date=request.GET.get("end_date")
    first_time=request.GET.get("start_time")
    second_time=request.GET.get("end_time")

    if first_date == None:
        date_today = date.today()
        first_date = date_today
        second_date = date_today
        first_time = time.localtime()
        second_time = time.localtime()

        first_time = datetime.fromtimestamp(mktime(first_time)).time()
        second_time = datetime.fromtimestamp(mktime(second_time)).time()

    comment = ""
    check = False
    for dates in booked_data:
        st_date= dates.start_date
        en_date = dates.end_date
        st_time = dates.start_time
        en_time = dates.end_time

        if type(first_date) == str :
            print("hello")
            first_date = datetime.strptime(first_date, '%Y-%m-%d').date()
            second_date = datetime.strptime(second_date, '%Y-%m-%d').date()

        if type(first_time) == str:
            first_time = time.strptime(first_time, "%H:%M")
            second_time = time.strptime(second_time, "%H:%M")
            first_time = datetime.fromtimestamp(mktime(first_time)).time()
            second_time = datetime.fromtimestamp(mktime(second_time)).time()

        print("+++++++++++++++ ================== ",st_date,first_date,en_date)
        print(type(st_date), type(first_date))
        if st_date <= first_date <= en_date:
            print('in between')
            check =True
        elif st_date <= second_date <= en_date:
            print('in between')
            check =True
        else:
            print("No")
            pass

        print(type(st_time))

        if st_time <= first_time <= en_time:
            print('in between time')
            check =True
        elif st_time <= second_time <= en_time:
            print('in between time')
            check =True
        else:
            print("No ....")
            pass

        if check == True:
            break

    if check == True:
        comment = "Sorry, Please choose another date and time"
    else:
        comment = "Your date is available"

    return render(request, 'lookspace_app/availabilities.html', {'booked_data':booked_data, 'comment':comment} )



