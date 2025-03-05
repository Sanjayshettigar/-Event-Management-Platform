# Event Management Platform

A comprehensive event management solution built with Flask, offering features for event creation, ticketing, RSVP management, vendor coordination, and analytics.

## Features

- Event Creation and Management
- Ticketing and Registration System
- RSVP and Attendee Management
- Vendor Coordination
- Analytics and Reporting
- QR Code Generation
- Email Notifications
- Calendar Integration

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///event_management.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
STRIPE_SECRET_KEY=your_stripe_secret_key
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## Project Structure

```
event_management_platform/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── migrations/
├── instance/
├── requirements.txt
├── .env
└── README.md
```
