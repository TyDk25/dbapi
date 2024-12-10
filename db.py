from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///movies.db')

Base = declarative_base()

class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    movie = Column(String(250), nullable=False)
    year = Column(Integer, nullable=False)


Base.metadata.create_all(engine)