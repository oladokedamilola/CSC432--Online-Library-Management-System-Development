# Book Management System

![Project Image](images/project-image.png)

## Overview

The **Book Management System** is a Django-based web application designed to help users manage and explore books in various genres and categories. Users can browse books, view details, and search for books by genre or category. Admins can manage books, categories, and genres via an easy-to-use interface.

This system allows users to:
- Browse books by genre or category
- View detailed information about each book
- Search for books across multiple categories or genres
- Enjoy a responsive and user-friendly interface

---

## Features

- **User Registration and Login**: Secure user authentication with registration and login functionality.
- **Books Management**: Admins can add, update, or delete books, genres, and categories.
- **Search Functionality**: Search for books by category or genre.
- **Pagination**: Pagination for book lists to ensure smooth navigation on large datasets.
- **Responsive Design**: Mobile-friendly layout using Bootstrap.

---

## Prerequisites

Before setting up the project, make sure you have the following installed:

- **Python** 3.x
- **Django** 3.x or higher
- **Pip** (for installing dependencies)
- **Git** (for version control)
- **SQLite** (for local database development)

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/book-management-system.git
cd book-management-system

```

### 2. Create a Virtual Environment

Create a virtual environment to keep your project dependencies isolated:

```bash
python -m venv venv
```

Activate the virtual environment:
- On **Windows**:

```bash
venv\Scripts\activate
```

- On **Mac/Linux**:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Run migrations to set up the database:

```bash
python manage.py migrate
```

### 5. Create a Superuser

Create a superuser to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

### 6. Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/` in your browser.

---

## Usage

- **Home Page**: Displays all available books along with a search feature.
- **Book Detail**: Click on a book title to view detailed information including author, genre, and description.
- **Admin Panel**: Use the Django admin panel to manage books, categories, and genres. Access the admin panel at `http://127.0.0.1:8000/admin/` after logging in with the superuser account.

---

## File Structure

```plaintext
book-management-system/
├── books/                    # Contains the book-related models, views, and templates
│   ├── migrations/           # Database migrations
│   ├── models.py             # Models for Book, Genre, Category
│   ├── views.py              # Views for book-related actions
│   └── templates/            # HTML templates for rendering book pages
│
├── static/                   # Static files (CSS, JavaScript, images)
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   └── images/               # Images used in the project
│
├── media/                    # Media files (book cover images, etc.)
│
├── manage.py                 # Django project management command
├── requirements.txt          # List of Python dependencies
├── settings.py               # Django settings
└── urls.py                   # URL routing configuration
```

---

## Contributing

Contributions to this project are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to your branch (`git push origin feature-branch`).
6. Create a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or suggestions, feel free to contact:

- **Your Name** - [your.email@example.com](mailto:your.email@example.com)
- **GitHub** - [https://github.com/yourusername](https://github.com/yourusername)

---

## Acknowledgments

- [Django](https://www.djangoproject.com/) - A high-level Python web framework.
- [Bootstrap](https://getbootstrap.com/) - A front-end framework for responsive web design.

```
