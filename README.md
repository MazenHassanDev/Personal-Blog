# Personal Blog
A Python Flask web application that allows an admin to create and manage blog articles. Visitors can browse and read articles, while the admin can add, edit, and delete them through a protected dashboard.

## Features
- Browse and read all published articles
- Admin login with session-based authentication
- Add, edit, and delete articles from the admin dashboard
- Articles are stored and persisted in a local JSON file
- Dates are displayed in readable format (e.g. November 12, 2004)
- Built using only Python standard library modules and Flask

## How It Works
1. Articles are loaded from a local `data/articles.json` file on each request.
2. Visitors can browse articles on the home page and read them individually.
3. The admin logs in at `/login` to access the protected dashboard.
4. From the dashboard, the admin can add, edit, or delete articles.
5. All changes are saved back to `articles.json`.

## Installation
1. Clone the repository: https://github.com/MazenHassanDev/Personal-Blog.git
2. Install Flask:
```
pip install flask
```
3. Run the app:
```
python app.py
```

## Requirements
- Python 3.9+
- Flask

## Admin Credentials
- **Username:** admin123
- **Password:** Admin123

## Routes
| Route | Description |
|---|---|
| `/home` | Public article listing |
| `/article/<id>` | Read a single article |
| `/login` | Admin login |
| `/admin` | Admin dashboard (protected) |
| `/new` | Add a new article (protected) |
| `/edit/<id>` | Edit an article (protected) |
| `/delete/<id>` | Delete an article (protected) |

