# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Allow signed-in teachers to register or remove students
- Allow students to view activities and participants without signing in

## Teacher access

Teacher usernames and PBKDF2-SHA256 password hashes are stored in `teachers.json`.
Create an account from the repository root with `python src/add_teacher.py`.
The script prompts for a username and password, stores only the password hash,
and restricts the local credentials file to its owner. `teachers.json` is ignored
by Git; do not commit credentials or their hashes. To keep sessions valid across
restarts, set a strong `SESSION_SECRET`. Set `SESSION_HTTPS_ONLY=true` when
serving the site over HTTPS.

The teacher login and session endpoints are `/auth/login`, `/auth/session`, and
`/auth/logout`. Activity registration and removal endpoints require a signed-in
teacher session.

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Teacher registers a student for an activity                         |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Teacher removes a student from an activity                         |
| POST   | `/auth/login`                                                      | Sign in as a teacher                                                |
| GET    | `/auth/session`                                                    | Check the current teacher session                                   |
| POST   | `/auth/logout`                                                     | Sign out                                                            |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

Activity data is stored in memory, which means it will be reset when the server restarts.
