from typing import List, Optional


from pydantic import BaseModel




class ItemBase(BaseModel):

    title: str

    description: Optional[str] = None




class ItemCreate(ItemBase):

    pass



class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):

    email: str




class UserCreate(UserBase):

    password: str



class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class ItemUpdate(ItemBase):
    title:str
    class Config:
        orm_mode=True

class ItemDelete(ItemBase):
    title:str
    class Config:
        orm_mode=True


