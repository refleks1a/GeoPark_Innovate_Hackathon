from django.contrib.auth import login, authenticate, logout, forms, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView, DetailView

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser

from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='main:home', login_url='custom_auth:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.Info('Your password was successfully updated!')
            return redirect('custom_auth:change_password')
        else:
            messages.Error('Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'custom_auth/change_password.html', {
        'form': form
    })


def verify_email_complete(request):
    request.user.email_is_verified = True
    request.user.is_active = True
    return render(request, 'custom_auth/verify_email_complete.html')


def verify_email_success(request):
    return render(request, 'custom_auth/verify_email_success.html')


def verify_email_confirm(request, uidb64, token):
    context = {
        'fail': '',
        'success': '',
    }
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.is_active = True
        user.save()
        context['success'] = 'Your email has been verified.'
        return redirect('custom_auth:verify_email_complete')
    else:
        context['fail'] = 'The link is invalid..'

    return render(request, 'custom_auth/verify_email_confirm.html', context)


def verify_email(request):
    if request.method == "POST" and not request.user.email_is_verified:
        if not request.user.email_is_verified:
            current_site = get_current_site(request)
            user = request.user
            user.is_active = False
            email = request.user.email
            subject = 'Verify your email!'
            message = render_to_string('custom_auth/verification_email.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                subject=subject,
                body=message, to=[email],
                from_email='fhbxdfh.dhncdtb@gmail.com'
            )

            email.content_subtype = 'html'
            email.send()

            return redirect('custom_auth:verify_email_success')
        else:
            redirect('custom_auth:signup')

    return render(request, 'custom_auth/verify_email.html')


class CustomUserCreationView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'custom_auth/signup.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        user.is_active = False
        login(self.request, user)

        if not user.email_is_verified:
            return redirect(reverse_lazy('custom_auth:verify_email'))

        if user is not None and user.is_active:
            return redirect(reverse_lazy('main:home'))

        return super().form_valid(form)

    def clean_email(self):
        email_input = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email_input).exists():
            raise forms.ValidationError('Email already exists! Please other email.')

        return email_input


class CustomUserLoginView(FormView):
    form_class = CustomUserLoginForm
    template_name = 'custom_auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        credentials = form.cleaned_data

        if not CustomUser.objects.filter(email=credentials['email']).exists():
            return redirect('custom_auth:login')

        credentials['username'] = CustomUser.objects.get(email=credentials['email']).username

        user = authenticate(username=credentials['username'], email=credentials['email'],
                            password=credentials['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            return redirect('main:home')
        else:
            return redirect('custom_auth:login')


class CustomUserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'custom_auth/user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def LogoutView(request):
    logout(request)
    return redirect(reverse_lazy('main:home'))
