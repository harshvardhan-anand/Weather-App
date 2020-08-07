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
    # creating this session as we will check wheather a request is ajax or not
    request.session['is_ajax'] = 0
    return render(request,'homepage/homepage.html',context={'form':form})

def wheather(request):
    alert = {
        'status':0,
        'msg':'No alert'
    }
    try:
        # this exception block is required to block 404 error if user directly goes to 
        # http://127.0.0.1:8000/wheather/ because then is_ajax session wont be set as he skipped 
        # homepage.
        request.session['is_ajax']
    except:
        redirect('/')

    if request.method=='POST' and request.session['is_ajax']==0:
        # Here it is required to check is_ajax because if user creates a post request from console 
        # then our program will try to grab the data from the site(city populated) which is not 
        # possible
        if request.is_ajax():
            # if request is ajax the automatically redirect to the wheather link.
            # Since the location is sent through ajax and we have to modify the api call so we need to
            # check wheather the request is ajax or not.
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
                return redirect('/', context={'alert':alert})
                
        # access the link and fetch the data         
        try:
            wdata = access.wheather_data()
        except:
            # if provided city is incorrect then invalid url will be returned
            # redirect to main page with alert no such city found
            alert['status'] = 1
            alert['msg'] = 'It seems you have misspelled your city. Please try once again.'
            return redirect('/', context={'alert':alert})
        else:
            if request.session['is_ajax']:
                # Trigger this if ajax is used.
                request.session['wdata']=wdata
                return HttpResponse()
            else:
                # Return this if city is used
                return HttpResponse("<h1>Triggered due to city populated</h1>")
    else:
        # if request is a get request then check wheather ajax is active or not as it is redirected 
        # from javascript code. If no ajax, then redirect them to home page.
        # This will occur if person want directly goes to homepage/wheather/
        if request.session['is_ajax']:
            request.session['is_ajax']=0
            wdata = request.session['wdata']
            return HttpResponse('<h1>Triggered due to location is set</h1>')
        else:
            alert['status'] = 1
            alert['msg'] = 'Hey man!! What are you tring to do? Follow the procedure.'
            return redirect('/', context={'alert':alert})