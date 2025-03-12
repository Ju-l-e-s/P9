
# Litrevu

Litrevu is a Django web application designed for managing book and article reviews. The application provides the following features:

- **Ticket Management**: Users can create and manage tickets to request reviews for books or articles.
- **Review Management**: Users can create reviews in response to tickets or create standalone reviews with a ticket.
- **Feed**: Users can view a personalized feed containing tickets and reviews from the users they follow.
- **User Following**: Users can follow or unfollow others to customize their feed.
- **Authentication**: Secure user registration, login, and logout functionalities.

---

## Prerequisites

- Python 3.8 or higher installed on your machine.
- Python dependencies listed in `requirements.txt`.

---

## Installation

### Clone the project repository:
```bash
git clone <REPOSITORY_URL>
```

### Navigate to the project directory:
```bash
cd litrevu
```

### Create a virtual environment:
```bash
python -m venv env
```

#### Activate the virtual environment:
- On Windows:
  ```bash
  env\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source env/bin/activate
  ```

### Install the dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

### Run the server:
Navigate to the project directory where `manage.py` is located and execute the following command:
```bash
python manage.py runserver
```

Open your browser and visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

---

## Features

- **Authentication**:
  - Sign up for a new account.
  - Log in to an existing account.
  - Log out securely.
- **Feed**:
  - View tickets and reviews from followed users and your own contributions.
  - Sort feed items in reverse chronological order.
- **Ticket Creation**:
  - Create a ticket to request reviews for a book or article.
  - Upload an image with the ticket.
- **Review Creation**:
  - Post a review in response to a ticket or create a standalone review with a ticket.
  - Add ratings between 1 and 5.
- **User Following**:
  - Search for users to follow.
  - View and manage your list of followed users.

---

## General Instructions

- **Menu Navigation**: Use the navigation bar to explore different sections of the application.
- **Form Submission**: Fill out the required fields and submit forms for creating tickets and reviews.
- **Image Upload**: Ensure images for tickets are in supported formats (JPEG, PNG, etc.).
- **Error Handling**: User-friendly messages are displayed for invalid actions, such as incorrect login credentials or invalid form inputs.

---

## Project Structure:

```
litrevu/
├── accounts/
│    ├── templates/accounts/
│    │   ├── login.html
│    │   ├── signup.html
│    └── views.py
├── reviews/
│    ├── templates/reviews/
│    │   ├── feed.html
│    │   ├── create_ticket.html
│    │   ├── create_review.html
│    │   └── search_users.html
│    ├── models.py
│    ├── views.py
│    ├── forms.py
│    └── urls.py
├── litrevu/
│    ├── settings.py
│    ├── urls.py
│    ├── wsgi.py
│    └── asgi.py
├── media/  # Directory for user-uploaded images
├── static/  # Directory for static files (CSS, JS)
│    ├── css/
│    │   └── styles.css
│    └── js/
│         └── scripts.js
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

---

## Future Improvements

- Enhance the UI for a better user experience.
- Add advanced search and filtering options in the feed.
- Implement notifications for new reviews or tickets from followed users.

---

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.
