from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))
    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        return '<User %s>'.format(self.nickname)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index= True, nullable=False)
    history = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(100), unique=True)


    def __repr__(self):
        return '<Post %s >'.format(self.history)