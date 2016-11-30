from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items = relationship("CategoryItem", back_populates="category")

    @property
    def serialize(self):
      """
      Return object data in easily serializeable format
      """
      return {
        'name'   : self.name,
        'id'     : self.id,
        'items'  : self.serialize_items
      }

    @property
    def serialize_items(self):
      """
      Return object's relations in easily serializeable format.
      """
      return [ item.serialize for item in self.items]

class CategoryItem(Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key = True)
    title =Column(String(80), nullable = False)
    description = Column(String(250))
    cat_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category, back_populates="items")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
      """
      Return object data in easily serializeable format
      """
      return {
        'cat_id'      : self.cat_id,
        'title'       : self.title,
        'description' : self.description,
        'id'          : self.id,
      }



engine = create_engine('sqlite:///categoryitem.db')


Base.metadata.create_all(engine)
