from django.shortcuts import render, RequestContext, render_to_response
from models import *
from forms import *
from django.http import HttpResponse
################ Import for login registration ###################
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
##################################################################

###################### IMPORT FOR SELENIUM #######################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
################### HTTP RESPONSE ################################
from django.http import Http404
##################################################################
############### URL DISPATCHER ###################################
from django.core.urlresolvers import resolve
##################################################################
##################### DJANGO WEBROWSER ###########################
import webbrowser
import urllib2, urllib
##################################################################

##################################################################


################################ USER REGISTRATION, LOGIN, LOGOUT ##############################################


def user_register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            #user.is_active=False
	    user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']
	    


            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
	    return HttpResponseRedirect('/user_login')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            return HttpResponse('Invalid Information For Registraion')

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'register.html', {'user_form':user_form, 'profile_form':profile_form})

#login

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST,QueryDict try to pull out the relevant information.
    if request.method == 'POST':
	form= loginForm(request.POST)
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:

                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
		
                return HttpResponseRedirect('/success')
            else:
                # An inactive account was used - no logging in!
                return HttpResponseRedirect('/user_login')
        else:
            # Bad login details were provided. So we can't log the user in.
            #print "Invalid login details: {0}, {1}".format(username, password)
	    	
	    message = "Get Back with a Valid Password and Username Fucker " + username
	    form = loginForm()
            return render(request,'login.html', {'form':form,'message':message})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
	form= loginForm()
        return render(request, 'login.html', {'form':form}, context)

#logout
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/user_login')
###################################################################################################################

def success(request):
	return render(request, 'success.html')


################################ Searching Using Selenium #########################################################

def search(request):
	if request.method =="POST":
		form = searchForm(request.POST)
		if form.is_valid():			
			f = form.save(commit=False)
			f.user = request.user.userprofile
			f.save()
			recentlink = f.sitesentered
			searchword = f.words
			inword = f.inwords
			splitword = re.split(',',str(inword))
			final_word = re.split(',',str(searchword))

			#remote server connection variables
			for var in final_word:
				browser = webdriver.Firefox()
				#openlink = webbrowser.open('http://'+recentlink)
				browser.get("http://"+ recentlink)
				new_link = browser.find_element_by_partial_link_text(var).click()
				url = browser.current_url
				
				for product in splitword:
					browser.get(url)
					newproduct = browser.find_element_by_partial_link_text(product).click()
					return JsonResponse({'message':'It Has been Found'})
			
			
				
			return render(request, 'success.html',{'new_link':new_link, 'url':url})
		else:
			return HttpResponse("Your Data Have Not Been Posted")		 
		
	form = searchForm()
	return render(request, 'search.html',{'form':form})









