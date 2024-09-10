from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, EqualTo
from flask_wtf import FlaskForm
from DashApp import create_dash_application

# Initialize the Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "@exwhybaba"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
app.config["DEBUG"] = True

# Configuring Flask-Mail for Gmail
sq = 'wnoc ddnj djxy pial'  # Dummy password
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'seyeoyelayo@gmail.com'
app.config['MAIL_PASSWORD'] = sq  # Replace with your Gmail password or App Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


# Initialize extensions
mail = Mail(app)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# Serializer for generating tokens
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(128), nullable=True)


# Flask-WTF Forms
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[Length(min=5)])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=4, max=25)])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[Length(min=5)])
    repeat_password = PasswordField("Confirm Password", validators=[EqualTo('password')])


# Routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            if user.is_active:
                login_user(user)
                return redirect(url_for("index"))  # Correct endpoint name
            else:
                flash("Please verify your email before logging in.", "warning")
                return redirect(url_for("login"))
        
        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)




@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the email or username already exists
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()

        if existing_user:
            flash("Email or Username is already registered.", "danger")
            return render_template("register.html", form=form)

        # Generate a verification token
        token = s.dumps(form.email.data, salt='email-confirmation-salt')

        # Create new user but not yet active
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            verification_token=token
        )

        # Add user to the database
        db.session.add(user)
        db.session.commit()

        # Send verification email
        verification_url = url_for('confirm_email', token=token, _external=True)
        msg = Message('Confirm your Email', sender='your_email@gmail.com', recipients=[form.email.data])
        msg.body = f"Please confirm your email by clicking on the following link: {verification_url}"
        mail.send(msg)

        flash("A confirmation email has been sent. Please check your inbox.", "info")
        return render_template("check_email.html")

    return render_template("register.html", form=form)


@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        # Validate token
        email = s.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for('index'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.is_active:
        flash("Account already verified. Please log in.", "info")
    else:
        user.is_active = True
        user.verification_token = None
        db.session.commit()
        flash("Your account has been verified! You can now log in.", "success")

    return redirect(url_for('login'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# initialize the Dash app
dash_app = create_dash_application(app)

@app.route("/dash")
@login_required
def dash_app_route():
    return dash_app.index()


if __name__ == "__main__":
    app.run(debug=True)
