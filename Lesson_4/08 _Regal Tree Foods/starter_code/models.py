from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

# You will use this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self, expires=6000):
        s = TimedJSONWebSignatureSerializer(secret_key=secret_key, expires_in=expires)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token, expires=6000):
        s = TimedJSONWebSignatureSerializer(secret_key=secret_key, expires_in=expires)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user_id = data['id']
        return user_id

    # Add a method to generate auth tokens here

    # Add a method to verify auth tokens here


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'category': self.category,
            'price': self.price
        }


engine = create_engine('sqlite:///regalTree.db')

Base.metadata.create_all(engine)

