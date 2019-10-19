from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User
from django.contrib.auth import login
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import PartnerSignUpForm, CustomerSignUpForm , SpaceDetailsForm
from django.contrib.auth.decorators import login_required
from .models import SpaceDetails
# Create your views here..

def home_page(request):
    return render(request, 'lookspace_app/home_page.html')

def index(request):
    return render(request, 'lookspace_app/index.html', {})

class SignUpView(TemplateView):
    template_name = 'lookspace_app/signup.html'



def home(request):
    if request.user.is_authenticated:
        if request.user.is_partner:
            return redirect('partners:quiz_change_list')
        else:
            return redirect('customers:quiz_list')
    return render(request, 'lookspace_app/home.html')

def index(request):
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
    template_name = 'lookspace_app/signup_form.html'

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
    template_name = 'lookspace_app/signup_form.html'

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
