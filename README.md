# FavouriteMistake
FavouriteMistake is a web platform designed to facilitate the reporting, search, and recovery of lost and found property around campus. The platform leverages image recognition technology to match lost and found items, making it easier for users to recover their belongings.

## Have a glimpse 👇👇

**Try it here:** [DEMO](https://favouritemistake.onrender.com)  
*Please wait for the project to spin up.*


## Features

- **User Registration and Authentication**: Users can sign up, log in, and manage their profiles.
- **Report Lost Items**: Users can report lost items by providing details and uploading images.
- **Report Found Items**: Users can report found items by providing details and uploading images.
- **Automated Matching**: The platform uses Google Cloud Vision API to analyze images and match lost items with found items.
- **Email Notifications**: Users receive email notifications when a potential match is found for their reported lost items.
- **Admin Interface**: Admins can manage users, items, and matches through the Django admin interface.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Image Recognition**: Google Cloud Vision API
- **Email Service**: SMTP (Gmail)
- **Deployment**: WSGI, ASGI

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/TaffCodes/FavouriteMistake.git
    cd FavouriteMistake
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a [.env](http://_vscodecontentref_/0) file in the project root and add the following:
    ```env
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432

    SERVICE_KEY=path_to_your_google_cloud_service_key.json

    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_password
    DEFAULT_FROM_EMAIL=your_email@example.com

    BASE_URL=http://127.0.0.1:8000
    ```

5. **Apply database migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

1. **Sign Up**: Create an account on the platform.
2. **Report Lost Items**: Navigate to the "Report Lost" page and fill in the details of the lost item.
3. **Report Found Items**: Navigate to the "Report Found" page and fill in the details of the found item.
4. **Dashboard**: View potential matches for your reported items on the dashboard.
5. **Admin Interface**: Access the admin interface at `/admin` to manage users, items, and matches.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes ([git commit -m 'Add some feature'](http://_vscodecontentref_/1)).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.



## Contact

For any inquiries or support, please contact [me](mailto:basweti.dev@gmail.com).
