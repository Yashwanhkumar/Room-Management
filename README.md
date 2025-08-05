Bachelor Room Management App
A collaborative web application built with Django to help roommates manage shared services and track expenses within their living space.

Description
This application provides a centralized platform for bachelors or roommates living together to manage common tasks and costs. A user can create a "Room," which generates a unique invite code to share with their roommates. Once members join a room, they share a common dashboard where they can add services (like "Buy Groceries" or "Pay Wi-Fi Bill"), log the costs associated with those services, and view a collective list of tasks.

The application also features a special dashboard for the room's creator (the "Owner") to view monthly expense summaries and an admin panel for site administrators to oversee all activity.

Key Features
User Authentication System: Secure user registration with email verification, login, and logout.

Room Creation & Management:

Users can create a "Room" for their living space.

Each room has a unique, automatically generated invite code.

Roommates can join a room easily using the invite code.

Shared Room Dashboard:

A collaborative dashboard for each room, visible to all its members.

Members can add new services to the room.

All services added to the room are visible to all members.

Service & Expense Tracking:

For each service, members can add detailed records, including a description and cost.

Costs are tracked in Indian Rupees (₹).

Owner-Specific Dashboard:

The creator of a room has access to an exclusive "Owner Dashboard."

This dashboard displays key statistics, including total members, total services logged, and a summary of the current month's total expenses.

Admin Panel:

A comprehensive admin dashboard for site administrators (staff users).

View summary statistics for the entire application (total users, total services, etc.).

Search, filter, edit, and delete any service record across all rooms.

Technology Stack
Backend: Django, Python

Frontend: HTML, Bootstrap 5, CSS

Database: SQLite 3 (default for development)

Setup and Installation
Follow these steps to set up the project locally.

Clone the repository:

git clone <your-repository-url>
cd <project-directory>

Create and activate a virtual environment:

python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`

Install the required dependencies:

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt)

Apply database migrations:

python manage.py makemigrations
python manage.py migrate

Create a superuser account to access the Django admin and the custom admin panel:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

The application will be available at http://127.0.0.1:8000/.

Usage
Register a new user: Go to the registration page, fill in your details, and verify your email using the link sent to you.

Create or Join a Room:

After logging in, you'll be on the "Dashboard Hub."

Navigate to "My Rooms" to either create a new room or join an existing one using an invite code.

Manage Your Room:

Once in a room, you'll see the shared Room Dashboard.

Add new services using the "Add Service" button.

Click "Manage Service" on any service card to add cost records.

Owner Features: If you are the owner of the room, you will see an "Owner Dashboard" button to view monthly expenses and other statistics.

Admin Panel: If your user account has "Staff status," you will see an "Admin Panel" button on the main hub to access the site-wide admin dashboard.==========
