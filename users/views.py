from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # flash message is a one time alert displayed only once
            messages.success(request, f'YOUR ACCOUNT HAS BEEN CREATED! YOU ARE NOW ABLE TO LOGIN')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# message.debug
# message.info
# message.success
# message.warning
# message.error

@login_required
def profile(request):
    if request.method == 'POST':
        # we need to pass in the post data, request.files for image data 
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
    # we have to check if post route or not and then check if form is valid and thus save info
    # we populate fields of the form by passing an instance of the object
    # context used to pass to template
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'YOUR ACCOUNT HAS BEEN UPDATED!')
            return redirect('profile')
        # redirect better than sending to render because of post-get redirect pattern
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
    # to ensure user is logged in before viewing profile, import login_required
    # decorators add functionality to an existing function