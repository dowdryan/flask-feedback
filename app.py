from flask import Flask, render_template, url_for, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback_exercise"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "thesupersupersupersecretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

Bootstrap(app)
toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

# ====================================================================================
@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        with app.app_context():
            user = User.register(username, password, email, first_name, last_name)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
    else:
        return render_template('users/register.html',
                               form=form)


# ====================================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm()
    if form.validate_on_submit():
        print("validated")
        username = form.username.data
        password = form.password.data
        user = User.verify(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{session['username']}")
        else:
            form.password.errors = ["Invalid username/password."]
            return render_template("users/login.html", 
                                   form=form)
    print(form.errors)
    return render_template('users/login.html', 
                               form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/login')


# ====================================================================================
# GET /users/<username>
@app.route('/users/<username>')
def show_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    feedbacks = Feedback.query.filter_by(username=username).limit(10).all()
    return render_template('/users/show.html',
                           user=user,
                           feedbacks=feedbacks)

# POST /users/<username>/delete
@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username', None)
    return redirect('/')

# GET /users/<username>/feedback/add
# POST /users/<username>/feedback/add
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    form = FeedbackForm()
    user = User.query.get(username)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(
            title=title,
            content=content,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/new.html", 
                               form=form,
                               user=user)

# GET /feedback/<feedback-id>/update
# POST /feedback/<feedback-id>/update
@app.route('/users/<username>/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(username, feedback_id):
    user = User.query.get(username)
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    return render_template('/feedback/edit.html',
                           user=user,
                           feedback=feedback,
                           form=form)

# POST /feedback/<feedback-id>/delete
@app.route('/users/<username>/feedback/<feedback_id>/delete', methods=['GET', 'POST'])
def delete_feedback(username, feedback_id):
    user = User.query.get(username)
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f"/users/{user.username}")
    

# ====================================================================================
@app.route('/secret', methods=['GET']) # Change to /users/<username>
def secret():
    return "You made it!"

if __name__ == "__main__":
    app.run(debug=True)
