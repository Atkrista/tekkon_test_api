# Instructions

## Project Setup
- Install `pipenv` from your Os's package manager.
- Activate your virtual env and spawn a shell using `pipenv shell`.
- Install requirements using `pipenv install`.
- Alternatively: Install python dependencies inside your virtualenv using `pip install -r requirements.txt`.
- Apply initial database migrations using `./manage.py migrate`.
- A park with 4 bays and 4 customers will be added with the initial migration. 
- Run the preliminary test suite using `./manage.py test`.
- Start the development server using `./manage.py runserver`.
- Access the server via `http://localhost:8000`.

## Solution Rationale
- Since this is an api for a single car park, only database tables for bays, bookings, and customers is required.
- sqlite is used instead of a full-featured database for demo and testing purposes.
- django and django-rest-framework is used to speed up development.
- Tests for early reservation, customer daily limit, and for the `/valid_bookings` endpoint.

## API description
- Navigate to `http://localhost:8000` to browse the api.
- `/customers` and `/bookings` endpoints are CRUD.
- `/bays` endpoint is Readonly.
- Valid bookings can be retrieved from the endpoint `/bookings/valid_bookings/?date=YYYY-MM-DD`. A valid date of fromat `YYYY-MM-DD` needs to be passed as a query param date.

