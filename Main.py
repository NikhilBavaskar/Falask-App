from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from urllib.parse import unquote_plus
import json
from flask_mail import Mail
import slugify

from datetime import timedelta
import os
import re
from werkzeug.utils import secure_filename


with open('config.json', 'r') as c:
    param = json.load(c)["param"]
local_server = "True"
app = Flask(__name__)
mail = Mail(app)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = param['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = param['prod_uri']
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = param['upload_location']
app.secret_key = 'qcpekyzqhrihsuwg'


def slugify(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces with underscores
    text = re.sub(r'\s+', '_', text)
    return text

class Contact(db.Model):
    ID = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    subj = db.Column(db.String(20), nullable=False)
    msd = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True ,default=datetime.utcnow)
    email = db.Column(db.String(50), nullable=False)
class Tag(db.Model):
    ID = db.Column(db.Integer, nullable=False, primary_key=True)
    headline = db.Column(db.String(20), nullable=False)
    cont = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(12), nullable=True)
class Blog(db.Model):
    ID = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sub = db.Column(db.String(100), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True)
    cont = db.Column(db.Text(2000), nullable=False , default=1+1)
    slug = db.Column(db.String(30), nullable=True)
    date = db.Column(db.String(12), nullable=False ,default=datetime.utcnow)
    def __init__(self, title, content,image_filename ):
        self.title = title
        self.cont = content
        self.slug = slugify(title)
        self.image_filename=image_filename


class Comments(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True , auto_increment=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=False ,default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True,autoincrement=True)
    user = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    passw = db.Column(db.String(50), nullable=False , unique=True)

class client_lead(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True , auto_increment=True)
    name = db.Column(db.String(45), nullable=False)
    requirement = db.Column(db.String(200), nullable=False)
    Business = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    technology = db.Column(db.String(45), nullable=False)
    Service = db.Column(db.String(100), nullable=False)
    client_Address = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(19), nullable=False ,default=datetime.utcnow)

    def __init__(self, name, requirement, Business, email, phone_number, technology,Service,client_Address,pincode):
        self.name = name
        self.requirement = requirement
        self.Business = Business
        self.email = email
        self.phone_number = phone_number
        self.technology = technology
        self.Service = Service
        self.client_Address = client_Address
        self.pincode = pincode
app.config.update(dict(
    DEBUG = True,
    MAIL_USE_SSL = False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT= "9150",
    #MAIL_PORT= "587",
    MAIL_USE_TLS=True,
    MAIL_USERNAME=param['gmail-user'],
    MAIL_PASSWORD=param['gmail-password']
))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


@app.route("/", methods=['GET', 'POST'])
def contactus():
    blog = Blog.query.order_by(Blog.ID.asc()).all()
    tag = Tag.query.order_by(Tag.ID.asc()).all()
    sr = 1  # Replace with the desired sr value
    tag1 = Tag.query.filter_by(ID=sr).first()
    print(tag1)
    sr2 = 2  # Replace with the desired sr value
    tag2 = Tag.query.filter_by(ID=sr2).first()
    sr3 = 3  # Replace with the desired sr value
    tag3 = Tag.query.filter_by(ID=sr3).first()
    sr4 = 4  # Replace with the desired sr value
    tag4 = Tag.query.filter_by(ID=sr4).first()
    sr5 = 5  # Replace with the desired sr value
    tag5 = Tag.query.filter_by(ID=sr5).first()
    sr6 = 6  # Replace with the desired sr value
    tag6 = Tag.query.filter_by(ID=sr6).first()
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name2 = unquote_plus(request.form.get('user'))
        email2 = unquote_plus(request.form.get('email'))
        subject3 = unquote_plus(request.form.get('subject'))
        msg = unquote_plus(request.form.get('msg'))
        entry = Contact(name=name2, email=email2, subj=subject3, msd=msg, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        #mail.send_message('New message from ' + name2,
                         # sender=email2,
                        #  recipients=[param['gmail-user']],
                         # body=subject3 + "\n" + msg + "\n" + email2
                        #  )
        return render_template('index.html',param=param ,tag=tag, tag1=tag1,tag2=tag2 , tag3=tag3, tag4=tag4, tag5=tag5, tag6=tag6, blog=blog)
    return render_template('index.html',param=param ,tag=tag, tag1=tag1,tag2=tag2 , tag3=tag3, tag4=tag4, tag5=tag5, tag6=tag6,blog=blog )

@app.route("/blogs/<string:blog_slug>", methods=['GET', 'POST'])
def blog(blog_slug):
    tag = Tag.query.filter_by(slug=blog_slug).first()
    blog = Blog.query.order_by(Blog.ID.asc()).all()
    cont = Blog.query.filter_by(slug=blog_slug).first()
    Comment = Comments.query.filter_by(slug=blog_slug).all()
    data = Comments.query.filter_by(slug=blog_slug).first()
    # footers
    sr = 1  # Replace with the desired sr value
    tag1 = Tag.query.filter_by(ID=sr).first()
    sr2 = 2  # Replace with the desired sr value
    tag2 = Tag.query.filter_by(ID=sr2).first()
    sr3 = 3  # Replace with the desired sr value
    tag3 = Tag.query.filter_by(ID=sr3).first()
    sr4 = 4  # Replace with the desired sr value
    tag4 = Tag.query.filter_by(ID=sr4).first()
    sr5 = 5  # Replace with the desired sr value
    tag5 = Tag.query.filter_by(ID=sr5).first()
    sr6 = 6  # Replace with the desired sr value
    tag6 = Tag.query.filter_by(ID=sr6).first()
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name2 = unquote_plus(request.form.get('name'))
        email2 = unquote_plus(request.form.get('email'))
        comment1 = unquote_plus(request.form.get('comment'))
        slug1 = blog_slug
        entry = Comments(name=name2, email=email2, comment=comment1,slug=slug1, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        return render_template('index.html', param=param, Comment=Comment, tag1=tag1, tag2=tag2, tag3=tag3, tag4=tag4,
                               tag5=tag5, tag6=tag6, blog=blog)
    # footer ends here
    return render_template('post.html', blog=blog,param=param,tag1=tag1,tag2=tag2 , tag3=tag3, tag4=tag4, tag5=tag5, tag6=tag6 ,cont=cont , Comment=Comment,)


@app.route("/pricing", methods=['GET', 'POST'])
def pricing():
    blog = Blog.query.order_by(Blog.ID.asc()).all()
    cont = Blog.query.filter_by().first()
    tag = Tag.query.order_by(Tag.ID.asc()).all()
    sr = 1  # Replace with the desired sr value
    tag1 = Tag.query.filter_by(ID=sr).first()
    sr2 = 2  # Replace with the desired sr value
    tag2 = Tag.query.filter_by(ID=sr2).first()
    sr3 = 3  # Replace with the desired sr value
    tag3 = Tag.query.filter_by(ID=sr3).first()
    sr4 = 4  # Replace with the desired sr value
    tag4 = Tag.query.filter_by(ID=sr4).first()
    sr5 = 5  # Replace with the desired sr value
    tag5 = Tag.query.filter_by(ID=sr5).first()
    sr6 = 6  # Replace with the desired sr value
    tag6 = Tag.query.filter_by(ID=sr6).first()
    return render_template('pricing.html', param=param ,tag=tag, tag1=tag1,tag2=tag2 , tag3=tag3, tag4=tag4, tag5=tag5, tag6=tag6, blog=blog)

@app.route("/logIN", methods=['GET', 'POST'])
def login():
    blog = Blog.query.order_by(Blog.ID.asc()).all()
    cont = Blog.query.filter_by().first()
    tag = Tag.query.order_by(Tag.ID.asc()).all()
    if "user" in session:
        return redirect("/Blog_post")
    if request.method == "POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        cont = User.query.filter_by(email=username).first()
        if username == cont.email and userpass == cont.passw:
            # Set the session variable
            session['user'] = username
            return redirect("/Blog_post")
        else:
            flash("Invalid login Credentials")  # Display flash message for invalid login
    return render_template("login.html", title="Login", param=param)
@app.route('/Blog_post', methods=['POST' , "GET"])
def Blog_post():
    blog = Blog.query.order_by(Blog.ID.asc()).all()
    tag = Tag.query.order_by(Tag.ID.asc()).all()
    if "user" in session:
        if request.method == "POST":
            if request.method == "POST":
                if 'file1' in request.files:
                    f = request.files['file1']
                    if f.filename != '':
                        # Securely save the uploaded file
                        filename = secure_filename(f.filename)
                        Headline = unquote_plus(request.form.get('Headline'))
                        Blog1 = unquote_plus(request.form.get('Blog'))
                        entry = Blog(title=Headline, content=Blog1,image_filename=filename)
                        db.session.add(entry)
                        db.session.commit()
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        f.save(filepath)
                        flash("Post added successfully")
                        flash("File uploaded successfully!", 'success')

                        return redirect('/Blog_post')  # Redirect to the uploader page
                    else:
                        flash("No file selected", 'error')
                else:
                    flash("No file part", 'error')

            else:
                flash("Please log in to add a comment")
        return render_template("Blog_post.html", param=param, blog=blog)
    else:
        flash("Log In First")  # Display flash message for invalid login
        return redirect("logIN")
@app.route('/edit')
def edit():
    blog = Blog.query.order_by(Blog.ID.asc()).all()
    if "user" in session:
        if request.method == "POST":
            db.session.delete(blog)
            db.session.commit()
        return render_template("edit.html", param=param , blog=blog)
    else:
        flash("Log In First")  # Display flash message for invalid login
        return redirect("/logIN")
    return render_template("edit.html", param=param , blog=blog)
@app.route('/edits/<string:blog_slug>', methods=['GET', 'POST'])
def blog_slug(blog_slug):
    post = Blog.query.filter_by(slug=blog_slug).first()
    if "user" in session:
        if request.method == 'POST':
            # Update the post with new data from the form
            new_title = request.form.get('headline')
            new_content = request.form.get('blog')
            post.title = new_title
            post.cont = new_content
            db.session.commit()
            flash('Post updated successfully', 'success')
            return redirect(url_for('edit'))
        return render_template("users-profile.html", param=param, post=post)
    else:
        flash("Log In First")  # Display flash message for invalid login
        return redirect("/logIN")
@app.route('/delete_post/<string:blogslug>', methods=['POST', 'GET'])
def delete_post(blogslug):
    post =  Blog.query.filter_by(slug=blogslug).first()
    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('edit'))
@app.route('/mail' ,  methods=['GET', 'POST'])
def mail():
    mail = Contact.query.filter_by().all()
    if "user" in session:
        if request.method == 'POST':
            # Update the post with new data from the form
            new_title = request.form.get('headline')
            new_content = request.form.get('blog')
            flash('Post updated successfully', 'success')
            return redirect(url_for('edit'))
        return render_template("mail.html", param=param, mail=mail)
    else:
        flash("Log In First")  # Display flash message for invalid login
        return redirect("/logIN")
@app.route('/newuser', methods=['POST','GET'])
def newuser():
    if "user" in session:
        if request.method == "POST":
            user = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            passw = request.form.get('password')
            entry = User(user=user, email=email ,username=username, passw=passw)
            db.session.add(entry)
            db.session.commit()
        return render_template("register.html",param=param)
    else:
        flash("Log In First")  # Display flash message for invalid login
        return redirect("/logIN")
@app.route('/buy', methods=['POST','GET'] )
def lead():
    

    return render_template('buyNow.html')
@app.route('/lead', methods=['POST'])
def handle_form_submission():
    if request.method == 'POST':
        name = request.form.get('first_name')
        Requirement = request.form.get('Requirement')
        Business = request.form.get('Business')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        technology = request.form.get('technology')
        Service = request.form.get('Service')
        Your_Address = request.form.get('Your_Address')
        Pincode = request.form.get('Pincode')
        entry = client_lead(name=name, requirement=Requirement, Business=Business, email=email,
                            phone_number=phone_number, technology=technology, Service=Service,
                            client_Address=Your_Address, pincode=Pincode)
        db.session.add(entry)
        db.session.commit()
        flash('We Contact with You Soon', 'success')
        return redirect("/buy")
    else:
        flash('Something Wrong Try Again ', 'Try Again')
        return redirect("/buy")
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect('logIN')
from waitress import serve
serve(app, host="0.0.0.0", port=8080)
