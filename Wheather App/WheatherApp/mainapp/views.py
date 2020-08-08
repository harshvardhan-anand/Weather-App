# Handling Cookies in django
# https://bit.ly/2EIq8xu

# we can use request.session after we have migrated our database by python manage.py migrate
# it is better than cookies in speed and security both.

# if we want to transfer data between views then we have to use either cookies or request.session

from django.shortcuts import render,redirect
from django.http import HttpResponse
from mainapp import forms
from mainapp.resources import fetch
import json

# Create your views here.
def homepage(request):
    form = forms.UserParam() # our form
    # creating this session as we will check weather a request is ajax or not
    request.session['is_ajax'] = 0
    try:
        alert = request.session['alert']
        context={'form':form,'alert':alert}
    except:
        context={'form':form}
    return render(request,'homepage/homepage.html',context=context)

def weather(request):
    alert = {
        'status':0,
        'msg':'No alert'
    }
    try:
        # this exception block is required to block 404 error if user directly goes to 
        # http://127.0.0.1:8000/weather/ because then is_ajax session wont be set as he skipped 
        # homepage.
        request.session['is_ajax'] = 0
    except:
        redirect('/')

    if request.method=='POST' and request.session['is_ajax']==0:
        # Here it is required to check is_ajax because if user creates a post request from console 
        # then our program will try to grab the data from the site(city populated) which is not 
        # possible
        if request.is_ajax():
            # if request is ajax the automatically redirect to the weather link.
            # Since the location is sent through ajax and we have to modify the api call so we need to
            # check weather the request is ajax or not.
            request.session['is_ajax'] = 1
            access = fetch.API(request.POST, is_location_set=1)
            access.api_key = 'ef9bfadddd3a930acfa7d1ee64fc0bef'
        else:
            form = forms.UserParam(request.POST)
            # checking whether form is valid or not
            if form.is_valid():
                user_preference = form.cleaned_data
                access = fetch.API(user_preference,is_location_set=0)
                access.api_key = 'ef9bfadddd3a930acfa7d1ee64fc0bef' #your API key
            else:
                # form is invalid then redirect them to
                # home page with alert fill city properly
                alert['status'] = 1
                alert['msg'] = 'Fill the prefered information properly'
                request.session['alert'] = alert
                return redirect('/')
                
        # access the link and fetch the data 
        # wdata is a dictionary
        try:
            wdata = access.weather_data()
        except:
            # if provided city is incorrect then invalid url will be returned
            # redirect to main page with alert no such city found
            alert['status'] = 1
            alert['msg'] = 'It seems you have misspelled your city. Please try once again.'
            request.session['alert'] = alert
            return redirect('/')
        else:
            if request.session['is_ajax']:
                # Trigger this if ajax is used.
                request.session['wdata']=wdata
                return HttpResponse()
            else:
                # Return this if city is used
                return render(request, 'mainapp/mainapp.html',context={'wdata':wdata})
    else:
        # if request is a get request then check weather ajax is active or not as it is redirected 
        # from javascript code. If no ajax, then redirect them to home page.
        # This will occur if person want directly goes to homepage/weather/
        if request.session['is_ajax']:
            request.session['is_ajax']=0
            wdata = request.session['wdata']
            return render(request, 'mainapp/mainapp.html',context={'wdata':wdata})
        else:
            alert['status'] = 1
            alert['msg'] = 'Hey man!! What are you tring to do? Follow the procedure.'
            request.session['alert'] = alert
            return redirect('/')