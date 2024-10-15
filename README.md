```md
# Dream Book - Django Project

This is a Django-based project that allows users to create, view, and manage dreams. Users can upload dream details, including images, and manage their visibility as public or private. Admin users can view all active dreams, while normal users can only manage their own dreams. Users can also like, dislike, and comment on dreams.

## Features

- User authentication (JWT-based login and signup)
- Create, view, update, and delete dreams
- Upload dream images
- Public and private dreams management
- Like, dislike, and comment on dreams
- Admin users can manage all active dreams

## Tech Stack

- Python 3.8+
- Django 4.x
- Django REST Framework (DRF)
- PostgreSQL or SQLite (for local development)
- JWT Authentication (using `djangorestframework-simplejwt`)

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed.
2. **Django** and **Django REST Framework** installed.
3. **PostgreSQL** (or SQLite for local development).
4. **Pipenv** or **virtualenv** (for virtual environment).

### Clone the Repository

```bash
git clone https://github.com/rj001-10/dream-book-django
cd dream-book-django
```

### Virtual Environment Setup

Create and activate a virtual environment:

```bash
# Using virtualenv
python -m venv venv
source venv/bin/activate

# Using Pipenv
pipenv shell
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database Setup

1. Configure your database in `settings.py`:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-db-name',
        'USER': 'your-db-user',
        'PASSWORD': 'your-db-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

2. Run migrations to set up the database schema:

```bash
python manage.py migrate
```

### Create a Superuser

To access the admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

The project will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

| Method | Endpoint               | Description                              | Auth Required |
|--------|------------------------|------------------------------------------|---------------|
| POST   | `/auth/login/`      | User login (JWT)                            | No            |
| POST   | `/auth/signup/`     | User signup                                 | No            |
| GET    | `/dream/`          | List all dreams                              | Yes           |
| POST   | `/dream/`          | Create a new dream                           | Yes           |
| GET    | `/dream/{id}/`     | Retrieve a dream by ID                       | Yes           |
| PATCH  | `/dream/{id}/`     | Update an existing dream                     | Yes           |
| DELETE | `/dream/{id}/`     | Delete a dream                               | Yes           |
| POST   | `/dream/{id}/like/`| Like a dream                                 | Yes           |
| POST   | `/dream/{id}/dislike/`| Dislike a dream                           | Yes           |
| POST   | `/dream/{id}/comment/`| Add a comment to a dream                  | Yes           |
| GET    | `/dream/{id}/comments/`| Get all comments on a dream              | Yes           |

### Authentication

The project uses JWT (JSON Web Token) authentication. You can obtain a token by logging in with valid credentials:

- **Login**: `/auth/login/`
- **Signup**: `/auth/signup/`

Once you have a token, include it in the headers of protected API requests:

```
Authorization: Bearer <your-token>
```

### Testing

To run the tests for the project, use:

```bash
python manage.py test
```

Ensure your test environment is set up correctly with the necessary test database configurations.

## Uploading Images

Images for dreams are handled via multipart form uploads. You can use DRF's `ImageField` to upload images when creating or updating dreams.

### Example of Image Upload in API Request

```bash
POST /dreams/
Content-Type: multipart/form-data
Authorization: Bearer <token>

{
  "title": "My Dream",
  "description": "A vivid dream about the future.",
  "image": <image_file>,
  "is_public": true
}
```


## License

This project is licensed under the MIT License. See the LICENSE file for more information.
```
