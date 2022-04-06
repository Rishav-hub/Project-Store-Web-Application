from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from project_store_entity_layer import entity as models
from project_store_data_access_layer.data_access import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from project_store_business_logic_layer.auth import get_current_user
from project_store_business_logic_layer import auth
from starlette.responses import RedirectResponse
from starlette import status

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/application", tags=["application"], responses= {"404": {"description": "Not Found"}})

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="project_store_presentation_layer/templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    todos = db.query(models.Application)\
        .filter(models.Application.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "applications": todos, "user": user})

@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...),description: str = Form(...),
                                github_url: str = Form(...), technology: str= Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    todo_model = models.Application()
    todo_model.title = title
    todo_model.description = description
    todo_model.github_url = github_url
    todo_model.technology = technology
    todo_model.owner_id = user.get("id")

    print(todo_model.title)

    db.add(todo_model)
    db.commit()
    return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)

@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    todo = db.query(models.Application).filter(models.Application.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html", {"request": request, "applications": todo, "user": user})

@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_comit(request: Request, todo_id: int, title: str = Form(...),description: str = Form(...),
                                github_url: str = Form(...), technology: str= Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    todo = db.query(models.Application).filter(models.Application.id == todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = github_url
    todo.technology = technology
    db.add(todo)

    db.commit()
    return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)

@router.get("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    todo = db.query(models.Application).filter(models.Application.id == todo_id)\
            .filter(models.Application.owner_id == user.get("id")).first()
    if todo is None:
        return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)
    db.query(models.Application).filter(models.Application.id == todo_id).delete()
    db.commit()

    return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)

@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo.complete = not todo.complete

    db.add(todo)
    db.commit()
    return RedirectResponse(url = '/todos', status_code= status.HTTP_302_FOUND)