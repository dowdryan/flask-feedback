from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()
default_email = "default@email.com"


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False,
                         unique=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      default=default_email)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls (
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email)
        # db.session.add(user)
        # db.session.commit()
        return user
    @classmethod
    def verify(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer(),
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False)

    
def connect_db(app):
    db.app = app
    db.init_app(app)