# DTI412 Lab 02 — CoursePortal (Django MVT)

IT Department Course Catalog & Inquiry Portal built with **Django 5.x** and **Bootstrap 5**,
following *Lab Assignment 2: Django Core Architecture, MVT Pattern & Dynamic Request Handling*.

## Project structure

```
DTI412-Lab02/              <-- Project root
├── manage.py
├── requirements.txt
├── courseportal/          <-- Main configuration package (settings, root urls, asgi, wsgi)
└── catalog/               <-- Application package
    ├── urls.py            <-- App-level URL routing (app_name = 'catalog')
    ├── views.py           <-- Function-based views + in-memory COURSES_DATA
    ├── tests.py           <-- Automated verification checklist
    └── templates/catalog/
        ├── base.html
        ├── home.html
        ├── course_list.html
        ├── course_detail.html
        └── inquiry.html
```

## Setup & run

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m django --version
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Routes

| URL | View | Result |
|-----|------|--------|
| `/` | `home_view` | Homepage with course metrics and featured course |
| `/courses/` | `course_list_view` | All course cards |
| `/courses/?q=react` | `course_list_view` | **Extension challenge**: filter by code or title |
| `/courses/101/` | `course_detail_view` | Syllabus detail for DTI412 |
| `/courses/999/` | `course_detail_view` | HTTP 404 |
| `/inquiry/` | `inquiry_view` | Inquiry form: GET render, POST validation, CSRF protected |

## Tests

```bash
python manage.py test catalog
```

Covers every route in the Step 7.1 checklist, form validation, CSRF rejection, and the Step 7.2 search filter.
