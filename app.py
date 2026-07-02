from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'berkeley_secret_key_for_session_management'

# Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Mock Database for Users
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "student": {"password": "student123", "role": "student"}
}

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id, USERS[user_id]['role'])
    return None

# --- ROUTES ---

@app.route('/')
def dashboard():
    metrics = {
        "total_collection": "Live from Registry",
        "available_shelves": "Ready for checkout",
        "currently_borrowed": "Due date tracking active"
    }
    announcements = [
        {"date": "July 02, 2026", "title": "Library Inventory Update", "desc": "Real-time spreadsheet parsing sync module deployment completed."},
        {"date": "June 09, 2026", "title": "Literacy Coaching Service", "desc": "Students within the Needed Intermediate Intervention Group will be invited to our reading session."}
    ]
    return render_template('dashboard.html', metrics=metrics, announcements=announcements)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            user_obj = User(username, USERS[username]['role'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)