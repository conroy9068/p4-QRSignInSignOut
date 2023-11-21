# QR Clock In/Out App

## Screenshot of finished project responsivness

## Emplyee/Subcontractor Clock In/Out App

> This is a simple app that allows employees to clock in and out of work using a QR code or by manual selection. The app enables the user to view their clock in/out history and also allows the admin to view all users clock in/out history. Admin have the ability to add project and the location associated with the project.

Required technologies for this project:

- HTML, CSS, JavaScript, Python+Django
- Relational database

# Live App

- https://qrsigninoutapp-c6f4e2915b2d.herokuapp.com/

## Table of Contents

<a name="contents">Back to top</a>

1. [UX]
2. [Features]
3. [Technologies Used]
4. [Testing]
5. [Deployment]
6. [Credits]

## UX

<a name="ux"></a>

### User Demographic

<a name="user-demographic"></a>
This application is designed for employees and subcontractors to clock in and out of project locations. The app is designed to be used on a mobile device. It will enable companies to track the time spent on projects and the location of the employee/subcontractor.

### Wireframes

<a name="wireframes"></a>

- Landing Page
  ![Landing Page](static/img/readme/landing-page.png)

- User Dashboard
  ![User Dashboard](static/img/readme/user-dashboard.png)

- Select Project
  ![Select Project](static/img/readme/select-project.png)

- Create Project
  ![Create Project](static/img/readme/create-new-project.png)

- View/Edit Project
  ![View/Edit Project](static/img/readme/edit-project.png)

- View/Edit Profile
  ![View/Edit Project](static/img/readme/view-edit-profile.png)

### Design

<a name="design"></a>

- Color Palette

  Charcoal Grey (#2a2a2a): Provides a strong, neutral base for text and key elements, ensuring excellent readability and a modern aesthetic.
  Vibrant Yellow (#FFD700): Used strategically for interactive elements and call-to-actions, this color stands out against the dark tones and captures user attention.

  This color scheme is professionalism with visual appeal, ensuring a clean and engaging user interface that reflects the efficiency and precision.

- Typography

  The typography choices reflect clarity and contemporary design, featuring:

  Montserrat: Chosen for headings due to its geometric simplicity and modern character, it enhances the visual impact of titles and section headers.
  Open Sans: Selected for body text, Open Sans is clean and legible, making reading seamless and comfortable across all devices.

  The fonts are selected not only for their visual harmony but also for their high readability, contributing to a user-friendly experience.

### User Stories

<a name="user-stories"></a>

### Database Schema

<a name="database-schema"></a>
![Database Schema dbdiagram.io](static/img/readme/database-schema.png)

#### User Model (django.contrib.auth.models.User)

| id       | Field         |
| -------- | ------------- |
| username | OneToOneField |
| email    | Charfield     |

#### UserProfile Model

| id            | Field         |
| ------------- | ------------- |
| user          | OneToOneField |
| role          | ForeignKey    |
| company_name  | Charfield     |
| date_of_birth | Datefield     |
| phone_number  | Charfield     |
| created_at    | DateTimeField |
| updated_at    | DateTimeField |

#### Role Model

| id          | Field     |
| ----------- | --------- |
| name        | Charfield |
| description | Charfield |

#### Project Model

| id                    | Field         |
| --------------------- | ------------- |
| name                  | Charfield     |
| project_code          | Charfield     |
| project_status        | Charfield     |
| project_url           | Charfield     |
| site_manager_name     | Charfield     |
| site_manager_email    | Charfield     |
| project_manager_name  | Charfield     |
| project_manager_email | Charfield     |
| created_at            | DateTimeField |
| updated_at            | DateTimeField |

#### Location Model

| id          | Field         |
| ----------- | ------------- |
| name        | Charfield     |
| project     | ForeignKey    |
| address     | Charfield     |
| description | Charfield     |
| is_active   | BooleanField  |
| qr_code     | FileField     |
| created_at  | DateTimeField |
| updated_at  | DateTimeField |

#### SignInOut Model

| id            | Field         |
| ------------- | ------------- |
| user          | ForeignKey    |
| location      | ForeignKey    |
| sign_in_time  | DateTimeField |
| sign_out_time | DateTimeField |
| created_at    | DateTimeField |
| updated_at    | DateTimeField |

## Features

<a name="features"></a>

### Existing Features

<a name="existing-features"></a>
Landing Page
![Landing Page](static/img/readme/app-landing-page.png)

Login
![Login](static/img/readme/app-login.png)

Logout Confirmation
![Logout](static/img/readme/app-logout.png)

Nav Bar
![Nav Bar](static/img/readme/app-navbar.png)

Footer
![Footer](static/img/readme/app-footer.png)

User Dashboard
![User Dashboard](static/img/readme/app-user-dashboard.png)

Select Project
![Select Project](static/img/readme/app-select-project.png)

Clocked Out
![Clock Out](static/img/readme/app-clocked-out.png)

Clocked In
![Clock In](static/img/readme/app-clocked-in.png)

Admin Panel (Projects)
![Admin Panel](static/img/readme/app-admin-panel-projects.png)

Admin Panel (Clock In/Out)
![Admin Panel](static/img/readme/app-clockin-register.png)

Create Project
![Create Project](static/img/readme/app-create-project.png)

Edit Project and Locations
![Edit Project](static/img/readme/app-edit-project.png)

Delete Project
![Delete Project](static/img/readme/app-delete-project.png)

Add Location
![Add Location](static/img/readme/app-add-location.png)

Location Active & Delete Checkbox and QR Download
![Location Active & Delete Checkbox](static/img/readme/app-location-active-checkbox-and-delete-checkbox.png)

View Profile
![View Profile](static/img/readme/app-view-profile.png)

Edit Profile
![Edit Profile](static/img/readme/app-edit-profile.png)

### Features Left to Implement

<a name="features-left-to-implement"></a>

- Add a clock in/out button to the user dashboard that will allow the user to open the clock out view of the current clocked in project to save them from having to navigate to the project selection page.

- Admin panel to allow the admin to view all users clock in/out history. This view would have a date filter range and allow the user to filter by subcontractor or company. This dashboard would have charts to display the data in a visual way.

- Subcontractor register, this would allow user to select/search a subcontractor name and set that as their company name.

- Ability to add multiple locations to a project at once.

- When user is registering i would like to have them redirected to a new form to complete their profile information.

- Allow the user to edit their name and email address in the edit profile view.

- Ability to the user to download a csv file of their clock in/out history.

- Ability to the admin user to download a csv file of all users clock in/out history.

- I would like to break down the app into smaller apps to make it easier to maintain and to add new features. As the app was developed needs changed and the app grew in complexity.

- Geo location, i would like to add the ability to track the users location when they clock in/out. This would allow the admin to see where the user was when they clocked in/out.

## Technologies Used

<a name="technologies"></a>
Languages Used

- HTML5

- CSS3

- JavaScript

- Python

Frameworks, Libraries & Programs Used

- Django:

  - The Django web framework was used to create the full-stack web application.

- QR Code Generator:

  - The QR Code Generator was used to generate the QR codes for the locations.

- PostgreSQL:

  - PostgreSQL was used as the object-relational database system.

- ElephantSQL:

  - ElephantSQL was used to host the database.

- Git:

  - Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.

- GitHub:

  - GitHub is used to store the projects code after being pushed from Git.

- Heroku:

  - Heroku was used for the deployed application.

- Gunicorn

  - A Python WSGI HTTP server for UNIX, used to run Python web applications.

- Whitenoise

  - A library for serving static files directly from Django, optimizing content delivery.

- Django Debug Toolbar

  - A configurable set of panels displaying various debug information about the current request/response.

- ASGIRef

  - ASGI (Asynchronous Server Gateway Interface) tools, allowing Django to run asynchronously.

- DJ-Database-URL

  - A utility to help you load your database into your dictionary from the DATABASE_URL environment variable.

- Packaging

  - A core utility for version management and package compatibility.

- PEP 8

  - A tool to check Python code against some of the style conventions in PEP 8.

- Pypng

  - A library for creating PNG (Portable Network Graphics) image files with Python.

- Psycopg2-Binary

  - A PostgreSQL database adapter for Python, providing efficient and secure database connections.

- Sqlparse

  - A non-validating SQL parser for Python, providing support for parsing, splitting, and formatting SQL statements.

- Typing Extensions
  - Backported and experimental type hints for Python.

## Agile Development

Github projects was used for the agile development of this project. The purpose for this was to layout the tasks that needed to be completed and to track the progress of the project.

## Testing

<a name="testing"></a>

- Testing was completed manually and with automated testing using Django's built in testing framework.

### Manual Testing

- User registration
  - User registration was tested by creating a new user account and checking that the user was redirected to the user dashboard.

| **TEST**                      | **ACTION**                                                                                                                                                                                       | **EXPECTATION**                                                                                | **RESULT**              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ----------------------- |
| User Registration             | User registration was tested by creating a new user account and checking that the user was redirected to the user dashboard.                                                                     | User is redirected to the dashboard after successful registration                              | Works as expected       |
| User Login                    | User login was tested by logging in with a valid user account and checking that the user was redirected to the user dashboard.                                                                   | User is redirected to the dashboard after successful login                                     | Works as expected       |
| Navigation                    | Navigation was tested by clicking the nav links and checking that the user was redirected to the correct view. Admin link where not visable                                                      | User is redirected to the correct view after clicking the nav link                             | Works as expected       |
| Admin Navigation Links        | Admin navigation links were tested by logging in with a valid admin account and clicking the nav links and checking that the user was redirected to the correct view. Admin links where visable. | Admin is redirected to the correct view after clicking the nav link                            | Works as expected       |
| Project Selection             | Project selection was tested by selecting a project and location and checking that the user was redirected to the clock in/out view.                                                             | User is redirected to the clock in/out view after selecting a project                          | Works as expected       |
| Clocking In                   | After user is brought to the clock in/out view the user can clock in by clicking the clock in button.                                                                                            | The view is updated with the clock in time and the clock in button becomes a clock out button  | Works as expected       |
| Clocking Out                  | After user is brought to the clock in/out view the user can clock out by clicking the clock out button.                                                                                          | The view is updated with the clock out time and the clock out button becomes a clock in button | Works as expected       |
| Admin Panel                   | Admin panel was tested by logging in with a valid admin account and clicking the admin nav link to be redirected to the admin panel.                                                             | Admin is redirected to the admin panel successful                                              | Works as expected       |
| Admin Panel (Projects)        | Admin panel projects view was tested by logging in with a valid admin account and clicking the projects link to be redirected to the projects view.                                              | Admin is redirected to the projects view successful                                            | Works as expected       |
| Admin Panel (Clock In/Out)    | Admin panel clock in/out view was tested by logging in with a valid admin account and clicking the clock in/out link to be redirected to the clock in/out view.                                  | Admin is redirected to the clock in/out view successful                                        | Works as expected       |
| Create Project                | Create project was tested by logging in with a valid admin account and clicking the create project link to be redirected to the create project view.                                             | Admin is redirected to the create project view successful                                      | Works as expected       |
| Edit Project                  | Edit project was tested by logging in with a valid admin account and clicking the edit project link to be redirected to the edit project view.                                                   | Admin is redirected to the edit project view successful                                        | Works as expected       |
| Add Location                  | Add location was tested by logging in with a valid admin account and clicking the add location link to be redirected to the add location view.                                                   | Admin is redirected to the add location view successful                                        | Works as expected       |
| Flagging Location as Inactive | Flagging location as inactive was tested by logging in with a valid admin account and removing the check beside active and updating the project                                                  | Location is inactive and not visable in the select location dropdown                           | Not working as expected |
| Deleting Location             | Deleting location was tested by logging in with a valid admin account and checking the location to delete and then updating the project                                                          | Admin is redirected to the delete location view successful                                     | Works as expected       |
| Downloading Location QR Code  | Downloading location QR code was tested by logging in with a valid admin account and clicking the download QR code link to download the QR code for the location.                                | QR code is downloaded successful                                                               | Works as expected       |
| Clocking In with QR Code      | Clocking in with QR code was tested by logging in with a valid user account and scanning the QR code to be redirected to the clock in/out view for that location.                                | User is redirected to the correct location clock in/out view                                   | Works as expected       |
| Deleting Project              | Deleting project was tested by logging in with a valid admin account and selecting delete project                                                                                                | Project is deleted and admin is redirected to admin panel                                      | Works as expected       |
| View Profile                  | View profile was tested by logging in with a valid user account and clicking the view profile link to be redirected to the view profile view.                                                    | User is redirected to the view profile view successful                                         | Works as expected       |
| Edit Profile                  | Edit profile was tested by logging in with a valid user account and clicking the edit profile link to be redirected to the edit profile view.                                                    | User is redirected to the edit profile view successful                                         | Works as expected       |
| Logout                        | Logout was tested by logging in with a valid user account and clicking the logout link to be redirected to the logout view.                                                                      | User is redirected to the logout view successful                                               | Works as expected       |

### Automated Testing

- I tested some of my views but due to time constraints i was not able to test all of them. I would like to add more tests in the future.

| **TEST**             | **ACTION**                                    | **EXPECTATION**                                                                                      | **RESULT** |
| -------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------- |
| Home View            | GET request to home page                      | Status code is 200 and correct template is used                                                      | Passed     |
| Register View - GET  | GET request to register page                  | Status code is 200                                                                                   | Passed     |
| Register View - POST | POST request to register with new user data   | User count increases by 1 and redirects to user dashboard                                            | Passed     |
| No Access View       | GET request to no access page                 | Status code is 200 and correct template is used                                                      | Passed     |
| Admin Panel View     | GET request to admin panel as admin           | Status code is 200, correct template is used, and context contains 'projects' and 'clocked_in_users' | Passed     |
| Create Project       | POST request to create a new project as admin | Status code is 302, project count is 1, and redirects to edit project page                           | Passed     |

### CI Python Linter Validation Results

All Python files were validated using Pylint. All files passed.
![CI Python Linter Validation Results](static/img/readme/pylint.png)

## Bugs

- Landing page background image not displaying. Was using body tag but it was causing the css validation to fail test.

- Marking location as inactive is not working as expected. The location is not being removed from the select location dropdown.

## Credits

<a name="credits"></a>

- Extending user model
  https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
  https://stackoverflow.com/questions/42478191/how-to-add-extra-fields-in-user-model-and-display-them-in-django-admin
- QRCode generator
  https://www.geeksforgeeks.org/generate-qr-code-using-qrcode-in-python/
- Pylint for Django
- https://stackoverflow.com/questions/71986184/how-can-i-override-str-in-models-py
