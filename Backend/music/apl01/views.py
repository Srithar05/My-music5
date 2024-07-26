from django.shortcuts import render

# Create your views here.
def temp(request):
    return render(request, 'sri.html')

def sri(request):
    return render(request,'sri.html')


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from .models import Customer
from django.views import View
#from .views import cart    
    
class Categories(View):
    return_url = None
    def get(self , request):
        Categories.return_url = request.GET.get('return_url')
        return render(request , 'categories.html')

class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_username(username)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('sri')
            else:
                error_message = 'Invalid Password'
        else:
            error_message = 'Invalid Username'

        print(username, password)
        return render(request, 'login.html', {'error': error_message})



class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        phone = postData.get('phone')
        email = postData.get('email')
        
        # validation
        value = {
            'username': username,
            'password': password,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(username=username,
                            phone=phone,
                            email=email,
                            password=password)
                           
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(username, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('sri')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.username):
            error_message = "First Name Required !!"
        elif len(customer.username) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
    
 