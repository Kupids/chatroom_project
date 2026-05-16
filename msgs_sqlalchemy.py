from sqlalchemy import ForeignKey , String , Integer , delete , create_engine
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column , relationship , sessionmaker , Session
from pydantic import BaseModel , Field , ConfigDict
from typing import Annotated
engine = create_engine("postgresql+psycopg2://matan:matan123@localhost:5432/backend_stuff")
Session = sessionmaker(bind = engine)

#def hasher(pass : str) -> str:
    
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'User'
    id : Mapped[int] = mapped_column(autoincrement = True , primary_key = True)
    username : Mapped[str] = mapped_column(String(10) , nullable = False)

    password : Mapped[str] = mapped_column(String(10) , nullable = False)

    user_relation : Mapped[list['msgs']] = relationship(back_populates = 
    'msg_relation')
class Messages(Base):
    __tablename__ = 'Messages'

    msg_id : Mapped[int] = mapped_column(autoincrement = True , primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("User.id"))

    msg : Mapped[str] = mapped_column(String(50))

    msg_date : Mapped[str] = mapped_column() 

class Auth(BaseModel):
    username : str = Field(max_length=10)

    password : str = Field(max_length=10)
    
    @classmethod
    def get_string(cls , auth_string : str) -> str:
        if ":" not in auth_string:
            raise ValueError("type it as username:password")
        username , password = auth_string.split(":" , 1)
        return cls(username = username.strip() , password = password.strip())
class msg(BaseModel):
    username : str = Field(max_length=10)
    msg : str = Field(max_length=50)

Base.metadata.create_all(engine)
