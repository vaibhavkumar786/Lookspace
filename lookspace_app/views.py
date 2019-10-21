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

# Create your views here..

def home_page(request):
    return render(request, 'lookspace_app/home_page.html')

class SignUpView(TemplateView):
    template_name = 'lookspace_app/signup.html'


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
    print("current ================", current_user.id)
    all_data = SpaceDetails.objects.filter(user=current_user.id)
    return render(request, 'lookspace_app/space_details.html', {'all_data':all_data} )

@login_required
def edit_space_details(request, id):
    all_data = SpaceDetails.objects.get(id=id)
    all_data.save()
    return render(request, 'lookspace_app/edit_details.html', {'all_data':all_data} )

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

    for dates in booked_data:
        st_date= str(dates.start_date).split('-')
        en_date = str(dates.end_date).split('-')
        st_time = str(dates.start_time).split('-')
        en_time = str(dates.end_time).split('-')

        # st_date = str(st_date.datetime.now().date())
        print("dates-------=========",st_date)

        # y1, m1, d1 = st_date
        # print(first_date)
        # y2, m2, d2 = first_date
        # print(y2,m2,d2)

        # b1 = date(y1, m1, d1)
        # b2 = date(y2, m2, d2)

        # if b1 == b2:
        #     print("equal")
        # elif(b1 > b2):
        #     print("second person")
        # else:
        #     print("first")

    return render(request, 'lookspace_app/availabilities.html', {'booked_data':booked_data} )



