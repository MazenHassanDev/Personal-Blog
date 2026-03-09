from flask import Flask, request, redirect, render_template, url_for, session
import json
import os
from datetime import datetime


# ===========================================================================
# 1) Flask app & File Handling
# ===========================================================================


app = Flask(__name__)

app.secret_key = 'Mizo121104@'

ARTICLES_FILE = os.path.join(os.path.dirname(__file__), 'data/articles.json')

articles = []

def load_articles():
    global articles

    if not os.path.exists(ARTICLES_FILE):
        articles = []
        with open(ARTICLES_FILE, 'w') as f:
            json.dump(articles, f, indent=4)
        # Created new ARTICLES_FILE. Starting with an empty list.
        return
    
    try:
        with open(ARTICLES_FILE, 'r') as f:
            articles = json.load(f)
    except json.JSONDecodeError:
        articles = []
        with open(ARTICLES_FILE, 'w') as f:
            json.dump(articles, f, indent=4)

def save_articles():
    
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=4)


# DATE FORMATTER
# ===========================================================================
@app.template_filter('format_date')
def format_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%B %d, %Y')
    except (ValueError, TypeError):
        return date_str


# ===========================================================================
# MAIN ROUTES
# ===========================================================================


@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    load_articles()
    return render_template('home.html', articles=articles)

@app.route('/article/<int:article_id>', methods=['GET'])
def article(article_id):
    load_articles()

    article = next((a for a in articles if a['id'] == article_id), None)
    if article:
        return render_template('article.html', article=article)
        
    return redirect(url_for('home'))


# ===========================================================================
# ADMIN ROUTES
# ===========================================================================


# ADMIN LOGIN & LOGOUT
# ===========================================================================
@app.route('/login', methods= ['GET', 'POST'])
def login():

    if session.get('logged_in'):
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin123' and password == 'Admin123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# ADMIN DASHBOARD
# ===========================================================================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    load_articles()
    return render_template('admin_dashboard.html', articles=articles)


# ADMIN CREATE NEW ARTICLE
# ===========================================================================
@app.route('/new', methods=['GET', 'POST'])
def add_article():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':

        load_articles()

        title = request.form.get('title')
        date = request.form.get('publishing_date')
        content = request.form.get('content')
        article_id = len(articles) + 1

        if title and date and content:
            article = {
                "id": article_id,
                "title": title,
                "date": date,
                "content": content
            }
            articles.append(article)
            save_articles()
            return redirect(url_for('admin'))
        
    return render_template('add_article.html')


# ADMIN EDIT ARTICLE
# ===========================================================================
@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    load_articles()
    
    article = next((a for a in articles if a['id'] == article_id), None)
    
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('publishing_date')
        content = request.form.get('content')

        if article:
            article['title'] = title
            article['date'] = date
            article['content'] = content
            save_articles()
            return redirect(url_for('admin'))
        
    
    return render_template('edit_article.html', article=article)


# ADMIN DELETE ARTICLE
# ===========================================================================
@app.route('/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    load_articles()

    article = next((a for a in articles if a['id'] == article_id), None)
    
    if article:
        articles.remove(article)
        save_articles()
        return redirect(url_for('admin'))
    
    return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run(debug=True)