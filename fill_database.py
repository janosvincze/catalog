from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///categoryitem.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Add Category and its items
category1 = Category(name="Soccer",
                     user=User1)

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(title="Two shinguards",
                     description="Two shinguards to guard",
                     category=category1,
                     user=User1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(title="Jersey",
                     description="The shirt",
                     category=category1,
                     user=User1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(title="Soccer Cleats",
                     description="The shoes",
                     category=category1,
                     user=User1)
session.add(categoryItem3)
session.commit()

category2 = Category(name="Basketball",
                     user_id=User1.id,
                     user=User1)

session.add(category2)
session.commit()

categoryItem4 = CategoryItem(title="Basketball",
                     description="The ball",
                     category=category2,
                     user=User1)
session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(title="All Star",
                     description="The shirt",
                     category=category2,
                     user=User1)
session.add(categoryItem5)
session.commit()

category3 = Category(name="Baseball",
                     user=User1)

session.add(category3)
session.commit()

categoryItem6 = CategoryItem(title="Bat",
                     description="The bat",
                     category=category3,
                     user=User1)
session.add(categoryItem6)
session.commit()

category4 = Category(name="Frisbee",
                     user=User1)

session.add(category4)
session.commit()

categoryItem7 = CategoryItem(title="Frisbee",
                     description="The frisbee",
                     category=category4,
                     user=User1)
session.add(categoryItem7)
session.commit()


category5 = Category(name="Snowboarding",
                     user=User1)

session.add(category5)
session.commit()

categoryItem8 = CategoryItem(title="Snowboard",
                     description="Snowboard",
                     category=category5,
                     user=User1)
session.add(categoryItem8)
session.commit()


category6 = Category(name="Rock Climbing",
                     user=User1)

session.add(category6)
session.commit()

categoryItem9 = CategoryItem(title="Rope",
                     description="Rope",
                     category=category6,
                     user=User1)
session.add(categoryItem9)
session.commit()

categoryItem10 = CategoryItem(title="Carabiner",
                     description="Carabiner",
                     category=category6,
                     user=User1)
session.add(categoryItem10)
session.commit()

category7 = Category(name="Foosball",
                     user=User1)

session.add(category7)
session.commit()

category8 = Category(name="Skating",
                     user=User1)

session.add(category8)
session.commit()

category9 = Category(name="Hockey",
                     user=User1)

session.add(category9)
session.commit()

categoryItem11 = CategoryItem(title="Stick",
                     description="Stick",
                     category=category9,
                     user=User1)
session.add(categoryItem11)
session.commit()

categoryItem12 = CategoryItem(title="Helmet",
                     description="Helmet",
                     category=category9,
                     user=User1)
session.add(categoryItem12)
session.commit()

print "added category items!"
