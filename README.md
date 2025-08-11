# MealDonor

MealDonor is a Flask-based web application that enables wedding hosts to register surplus food donations and allows charity organizations to browse, request, and collect these donations. The platform helps reduce food waste while supporting community welfare.

## Application Workflow

### User Registration & Authentication
- Users register as either Wedding Host or Charity Organizer
- Secure login with password hashing and session management
- Role-based dashboards and routing

### Hosts
- Add, update, and delete food donations with details (type, quantity, expiration date, city)
- Manage donation status (available → requested → donated)
- View donation history

### Charity Organizers
- Browse and filter available donations by city and organizer
- Request and cancel donation requests
- Track requested and received donations

### System Features
- Status workflow with real-time updates
- Data integrity via foreign keys and cleanup on deletion
- Flash messages and form validation for user feedback

## Installation and Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Initialize and migrate the database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

2. Run the application:

   ```bash
   python run.py
   ``` 
