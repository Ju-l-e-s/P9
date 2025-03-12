# reviews/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Review, Ticket, UserFollows
from django.http import HttpRequest, HttpResponse
from .forms import ReviewForm, TicketForm

from itertools import chain
from django.db.models import CharField, Value
from django.core.paginator import Paginator
from django.db.models import Q


def redirect_to_feed(request):
    return redirect('feed')

@login_required
def create_ticket(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a new Ticket.

    Checks if the request method is POST to process the form submission,
    otherwise, it displays the ticket creation page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: An HTTP response with the rendered ticket creation page or a redirect to the feed.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = TicketForm()

    context = {
        'form': form,
    }
    return render(request, 'reviews/create_ticket.html', context)



@login_required
def edit_ticket(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Allows a user to edit their own ticket. If the user is not the owner of the ticket, they are redirected to the feed.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param ticket_id: The ID of the ticket to be edited.
    :type ticket_id: int
    :return: An HTTP response object.
    :rtype: HttpResponse
    """
    ticket = Ticket.objects.get(id=ticket_id)

    if request.user != ticket.user:
        print("Accès refusé : vous ne pouvez modifier que vos propres tickets !")
        return redirect('feed')

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            print("Ticket modifié avec succès !")
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
        'ticket': ticket,
    }
    return render(request, 'reviews/edit_ticket.html', context)


@login_required
def delete_ticket(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Deletes a ticket if the current user is the owner of the ticket.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param ticket_id: The ID of the ticket to be deleted.
    :type ticket_id: int
    :return: An HTTP response redirecting to the feed page or rendering the delete confirmation page.
    :rtype: HttpResponse
    """
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.user != ticket.user:
        print("Action refusée : vous ne pouvez supprimer que vos propres tickets.")
        return redirect('feed')

    if request.method == 'POST':
        ticket.delete()
        print("Ticket supprimé avec succès !")
        return redirect('feed')

    context = {
        'ticket': ticket,
    }
    return render(request, 'reviews/delete_ticket.html', context)



@login_required
def create_review(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    View to create a review in response to an existing ticket.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param ticket_id: The ID of the ticket for which the review is being created.
    :type ticket_id: int
    :return: An HTTP response object.
    :rtype: HttpResponse
    """
    
    print(f"Tentative de création de critique pour le billet ID : {ticket_id}")
    ticket = get_object_or_404(Ticket, id=ticket_id)
    print(f"Billet trouvé : {ticket.title}")

    if request.method == 'POST':
        print("Formulaire soumis par l'utilisateur")
        form = ReviewForm(request.POST)
        if form.is_valid():
            print("Formulaire valide, enregistrement de la critique...")
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            print("Critique enregistrée avec succès")
            return redirect('feed')  # Redirection après création
        else:
            print("Formulaire invalide")
            print(form.errors)  # Affiche les erreurs du formulaire dans la console
    else:
        print("Affichage du formulaire de création de critique")
        form = ReviewForm()

    context = {
        'form': form,
        'ticket': ticket,
    }
    return render(request, 'reviews/create_review.html', context)

@login_required
def edit_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """
    Handles the editing of a review by a user.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param review_id: The ID of the review to be edited.
    :type review_id: int
    :return: An HTTP response redirecting to the feed or rendering the edit review page.
    :rtype: HttpResponse
    """

    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'reviews/edit_review.html', context)


@login_required
def create_review(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Handles the creation of a review for a specific ticket.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param ticket_id: The ID of the ticket for which the review is being created.
    :type ticket_id: int
    :return: An HTTP response redirecting to the feed page after review creation or rendering the review creation form.
    :rtype: HttpResponse
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')  # Redirige vers le feed après création
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'ticket': ticket,
    }
    return render(request, 'reviews/create_review.html', context)


# reviews/views.py

@login_required
def create_ticket_and_review(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a ticket and its associated review.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: An HTTP response redirecting to the feed or rendering the form.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        print(request.POST)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            # 1) Create the ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # 2) Create the review associated with the ticket
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('feed')  # Redirect to the feed after creation
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_ticket_and_review.html', context)

def delete_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """
    Deletes a review if the requesting user is the author of the review.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param review_id: The ID of the review to be deleted.
    :type review_id: int
    :return: A redirect to the 'feed' page if the review is deleted or the user is not the author, otherwise renders the delete review confirmation page.
    :rtype: HttpResponse
    """

    review = get_object_or_404(Review, id=review_id)

    # Check if the user is the author of the review
    if request.user != review.user:
        print("Action refusée : vous ne pouvez supprimer que vos propres critiques.")
        return redirect('feed')

    if request.method == 'POST':
        review.delete()
        print("Critique supprimée avec succès !")
        return redirect('feed')

    context = {
        'review': review,
    }
    return render(request, 'reviews/delete_review.html', context)

@login_required
def feed(request: HttpRequest) -> HttpResponse:
    """
    Displays the feed of tickets and reviews for the logged-in user. Admin users see all tickets and reviews,
    while normal users see their own and those of the users they follow.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The HTTP response object with the rendered feed page.
    :rtype: HttpResponse
    """
def feed(request):
    # Check if the user is an admin
    if request.user.is_superuser:
        # The admin sees all tickets and reviews
        user_tickets = Ticket.objects.all().annotate(content_type=Value('TICKET', CharField()))
        user_reviews = Review.objects.all().annotate(content_type=Value('REVIEW', CharField()))
    else:
        # Normal user: get the users they follow
        followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

        # Get tickets of the logged-in user and followed users
        user_tickets = Ticket.objects.filter(user=request.user).annotate(content_type=Value('TICKET', CharField()))
        followed_users_tickets = Ticket.objects.filter(user__in=followed_users).annotate(
            content_type=Value('TICKET', CharField()))

        # Get reviews of the logged-in user and followed users
        user_reviews = Review.objects.filter(user=request.user).annotate(content_type=Value('REVIEW', CharField()))
        followed_users_reviews = Review.objects.filter(user__in=followed_users).annotate(
            content_type=Value('REVIEW', CharField()))

        # Concatenate datas
        user_tickets = chain(user_tickets, followed_users_tickets)
        user_reviews = chain(user_reviews, followed_users_reviews)

    # Combine and sort all posts
    posts = sorted(
        chain(user_tickets, user_reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    # Pagination
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'reviews/feed.html', context)

User = get_user_model()

@login_required
def search_users(request: HttpRequest) -> HttpResponse:
    """
    Handles the search and follow/unfollow functionality for users.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The HTTP response with the search results and follow status.
    :rtype: HttpResponse
    """
    from django.db.models import Q

    query = request.GET.get('q', '')
    results = []
    followed_users = UserFollows.objects.filter(user=request.user)

    # Search for users
    if query:
        results = User.objects.filter(
            Q(username__icontains=query)
        ).exclude(id=request.user.id)  # Exclude the logged-in user

    if request.method == 'POST':
        followed_user_id = request.POST.get('followed_user_id')
        action = request.POST.get('action')

        if followed_user_id:
            followed_user = User.objects.get(id=followed_user_id)

            if action == 'follow':
                if not UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                    UserFollows.objects.create(user=request.user, followed_user=followed_user)
            elif action == 'unfollow':
                UserFollows.objects.filter(user=request.user, followed_user=followed_user).delete()

            return redirect('search_users')

    # Add an indicator for each user, indicating if they are followed or not
    results_with_follow_status = [
        {
            'user': user,
            'is_followed': UserFollows.objects.filter(user=request.user, followed_user=user).exists(),
        }
        for user in results
    ]

    context = {
        'results_with_follow_status': results_with_follow_status,
        'followed_users': followed_users,  # List of users followed by the logged-in user
        'query': query,
    }
    return render(request, 'reviews/search_users.html', context)

