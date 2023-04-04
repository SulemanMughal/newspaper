from .tokens import account_activation_token
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.urls import reverse
from django.core.mail import (send_mail, EmailMessage)

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import Article
from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import UpdateView, DeleteView  # new
from django.urls import reverse_lazy  # new
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView  # new
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import (
    loginForm,
    registerForm
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model


User = get_user_model()


class ArticleListView(LoginRequiredMixin, ListView):

    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(LoginRequiredMixin, DetailView):  # new

    model = Article
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # new

    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'

    def test_func(self):  # new

        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # new

    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):  # new

    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def UserLoginView(request):
    template_name = "login.html"
    if request.user.is_authenticated:
        return redirect("article_list")
    else:
        if request.method == "POST":
            form = loginForm(request.POST)
            valuenext = request.POST.get('next')
            if form.is_valid():
                try:
                    u = authenticate(
                        request,
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password"]
                    )
                    if u is not None:
                        if u.is_active:
                            login(request, u)
                            if len(valuenext) != 0 and valuenext is not None:
                                return redirect(valuenext)
                            else:
                                return redirect("article_list")
                        else:
                            messages.error(
                                request, "User does not verify himself or he has been blocked from using our services due to violation of our terms and conditions.")
                    else:
                        messages.error(
                            request, "Username or password has been entered incorrectly.")
                except Exception as e:
                    messages.error(
                        request, "Please login after sometimes. Requests are not processed at this time.")
            else:
                messages.error(
                    request, "Please entered correct information for respective required fields.")

    form = loginForm()
    context = {
        "form": form,
        "section": True
    }
    return render(request, template_name, context)


def UserLogoutView(request):
    logout(request)
    return redirect('article_list')


def UserRegistrationView(request):
    template_name = "registration.html"
    if request.user.is_authenticated:
        return redirect("article_list")
    else:
        if request.method != 'POST':
            form = registerForm()
        else:
            form = registerForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.active = False
                user.set_password(form.cleaned_data['password2'])
                user.email = form.cleaned_data['email']
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your account.'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, 'acc_active_email_confirm.html')
        context = {
            'form': form
        }
        return render(request, template_name, context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        login(request, user)
        try:
            n = request.GET.get("next", None)
            if n is not None:
                return redirect(n)
            else:
                return redirect('article_list')
        except:
            return redirect('article_list')
    else:
        messages.warning(request, "Invalid Activation Link")
        return redirect("user-login")


@login_required()
def change_password(request):
    template_name = "change_password.html"
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, "Password has been updated successfully.")
            return redirect(reverse('article_list'))
    context = {
        'form': form
    }
    return render(request, template_name, context)
