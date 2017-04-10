from flask import Flask, render_template, request, make_response, redirect
from flask_migrate import Migrate
from models import db,User,Post



app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/',methods=['GET','POST'])
def index():
    user_id = request.cookies.get('userID')

    if user_id:
        user = User.query.filter_by(id=user_id).first()
        name = user.nickname if user else 'Anonimous'
        posts_count = Post.query.filter_by(user_id=user_id).count()

    else:
        name = 'Anonimous'
        posts_count = 0


    return render_template('form.html',name=name,posts_count=posts_count)

@app.route('/post',methods=['POST'])
def post():
    user_id = request.cookies.get('userID')

    if user_id :
        user = User.query.filter_by(id=user_id).first()
    else:
        name = request.form['signature']
        new_user = User(nickname=name)
        db.session.add(new_user)
        db.session.flush()
        user_id = new_user.id

    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('userID',value=str(user_id))

    new_post = Post(title=request.form['header'],
                    history=request.form['body'],
                    user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return response


if __name__ == "__main__":
    app.run()
