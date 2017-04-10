from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for
from flask_migrate import Migrate
from models import db,User,Post



app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/', methods=['GET','POST'])
def index():
    user_id = request.cookies.get('userID')

    if user_id:
        user = User.query.filter_by(id=user_id).first()
        name = user.nickname if user else 'Anonimous'
        posts_count = Post.query.filter_by(user_id=user_id).count()
        posts = Post.query.filter_by(user_id=user_id).all()
    else:
        name = 'Anonimous'
        posts_count = 0
        posts = []

    return render_template('form.html',name=name,posts_count=posts_count,posts = posts)

@app.route('/post',methods=['POST','GET'])
def post():
    user_id = request.cookies.get('userID')
    post_id = request.args.get('id')

    if post_id and user_id and request.method=='GET':
        post = Post.query.filter_by(id=post_id).first()
        title = post.title
        history = post.history
        user_id = user_id
        name = User.query.filter(user_id).first().nickname
        posts_count = Post.query.filter_by(user_id=user_id).count()

        return jsonify (
            title=title,
            history=history,
            user_id=user_id,
            name=name,
            posts_count=posts_count,
            post_id=post_id)

    if request.form.get('id') and user_id :
        post = Post.query.filter_by(id=request.form.get("id")).first()
        post.history = request.form["body"]
        post.title = request.form["header"]
        post.user_id = user_id


    if not user_id :
        name = request.form['signature']
        new_user = User(nickname=name)
        db.session.add(new_user)
        db.session.flush()
        user_id = new_user.id

    if request.method=='POST' and user_id:
        new_post = Post(title=request.form['header'],
                        history=request.form['body'],
                        user_id=user_id)
        db.session.add(new_post)
        db.session.flush()
        new_post.url= url_for('index',_external=True) + "{0}-{1}".format(user_id,new_post.id)

    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('userID',value=str(user_id))


    db.session.commit()

    return response


if __name__ == "__main__":
    app.run()
