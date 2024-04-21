from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self,key,name):
        if len(name) < 1:
            raise ValueError("Failed name validation")

        all_authors_names = [author.name for author in Author.query.all()]

        if name in all_authors_names:
            raise ValueError("Failed name uniqueness validation")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number)>10:
            raise ValueError("Failed phone number length validation")

        elif len(number)<10:
            raise ValueError("Failed phone number length validation")

        elif type(int(number))!= int:
            raise ValueError("Failed phone number numer validation")

        return number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self,key,content):
        if len(content)<250 :
            raise ValueError("Content length validation failed")
        
        return content

    @validates('title')
    def validates_title(self,key,title):
        if len(title)<1:
            raise ValueError("Failed title length validation")

        click_bait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        in_title = False
        for word in click_bait_words:
            if word in title:
                in_title = True

        if in_title == False:
            raise ValueError("Failed clickbait-y test")

        return title

    @validates('summary')
    def validates_summary(self,key,summary):
        if len(summary)>250:
            raise ValueError("Failed summary length validation")

        return summary

    @validates('category')
    def validates_categoy(self,key,category):
        if 'Fiction' not in category:
            raise ValueError('Failed category type validation')
        elif 'Non-Fiction' not in category:
            raise ValueError('Failed category type validation')

        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
