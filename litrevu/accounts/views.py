from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse, HttpRequest

from .forms import SignupForm
def signup_view(request):
    # If the user is already authenticated, redirect them to the feed
    if request.user.is_authenticated:
        return redirect('feed')

    # Process the form data if it is a POST request
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            messages.success(request, "Compte créé avec succès ! Connectez-vous pour continuer.")
            return redirect('login')
    else:
        form = SignupForm()

    # Render the signup page with the form
    return render(request, 'accounts/signup.html', {'form': form})



class CustomLoginView(LoginView):
    """
    Custom login view that handles user login with success and error messages.

    :param template_name: Path to the login template.
    :type template_name: str
    """        
    template_name = 'accounts/login.html'

    def form_valid(self, form) -> HttpResponse:
        """
        Handles the form validation and displays a success message upon successful form submission.

        :param form: The form instance that is being validated.
        :type form: Form
        :return: The HTTP response indicating the form was valid.
        :rtype: HttpResponse
        """
        messages.success(self.request, f"Bienvenue, {form.get_user().username} !")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        """
        Handles the case when a form is invalid by displaying specific error messages.

        :param form: The form instance that is invalid.
        :type form: django.forms.Form
        :return: The response from the superclass's form_invalid method.
        :rtype: django.http.HttpResponse
        """
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)  # Display each error message
        return super().form_invalid(form)

@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Redirects to the login page after logout.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: An HTTP response redirecting to the login page.
    :rtype: HttpResponse
    """
    logout(request)
    return redirect('login')  # redirect after logout

def csrf_failure(request: HttpRequest, reason: str = "") -> HttpResponse:
    """
    Handles CSRF failure by rendering a failure page with the given reason.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param reason: The reason for the CSRF failure, defaults to an empty string.
    :type reason: str, optional
    :return: An HTTP response rendering the CSRF failure page.
    :rtype: HttpResponse
    """
    return render(request, 'csrf_failure.html', {"reason": reason})