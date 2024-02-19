## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/IshuNirwal/attendance.git

    Create a virtual environment:

    bash

python -m venv venv

Activate the virtual environment:

bash

source venv/bin/activate   # For Linux/Mac
# or
.\venv\Scripts\activate   # For Windows

Install the required dependencies:

bash

pip install -r requirements.txt

Run the migrations:

bash

python manage.py migrate

Start the development server:

bash

    python manage.py runserver

Usage

    Visit http://localhost:8000/ in your web browser.
    Explore the API endpoints using a tool like Postman or curl.

Contributing

We welcome contributions to this project. To contribute:

    Fork the repository.
    Make your changes.
    Create a pull request.

License

This project is licensed under the MIT license. See LICENSE for more details.
Additional Information

    This project is based on the Django REST framework (DRF).
    Technologies used:
        Python 3.x
        Django
        PostgreSQL
