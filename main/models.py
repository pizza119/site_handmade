from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class EnableDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

class ComeMenber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(200), nullable=False, unique=True)
    comeuser = db.Column(db.String(500), nullable=True)
    not_comeuser = db.Column(db.String(500), nullable=True)

class EnableDay_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(200), nullable=False)

    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    a_user = db.relationship('User', backref=db.backref('comment_user_set', ))
    
    Title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)

class Each_snack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(200), nullable=False)
        
    id_user = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    a_user = db.relationship('User', backref=db.backref('snack_user_set', ))

    content = db.Column(db.Text(), nullable=False)


