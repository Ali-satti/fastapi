from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import sql_app.crud as crud, sql_app.models as models, sql_app.schemas as schemas
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", response_model=schemas.User, tags=["Create User"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User],tags=["Read user"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["Search User By ID"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item,tags=["Create Items"])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item],tags=["Read items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_Title}", response_model=schemas.Item, tags=["Serch Item By Title"])
def read_items_title(item_title: str, db: Session = Depends(get_db)):
    items = crud.get_item_by_titile(db, title=item_title)
    if items is None:
        raise HTTPException(status_code=404, detail="item not found")
    return items




@app.put("/items",response_model=schemas.Item,tags=["Update items"])
def update_items(items_id:int,entrada:schemas.ItemUpdate,db:Session=Depends(get_db)):
    items=db.query(models.Item).filter_by(id=items_id).first()
    items.title=entrada.title
    db.commit()
    db.refresh(items)
    return items

@app.delete("/items",response_model=schemas.ItemDelete,tags=["Delete items"])
def delete_items(items_id:int,db:Session=Depends(get_db)):
    items=db.query(models.Item).filter_by(id=items_id).first()
    db.delete(items)
    db.commit()
    itemDelete=schemas.ItemDelete(title="Item deleted")
    return itemDelete








