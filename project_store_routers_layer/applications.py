import sys
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from project_store_business_logic_layer import business_logic
from project_store_entity_layer import entity as models
from project_store_data_access_layer.data_access import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from starlette.responses import RedirectResponse
from starlette import status

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from project_store_business_logic_layer.business_logic import BusinessLogic
from project_store_routers_layer.auth import get_current_user
from project_store_config_layer.configuration import Configuration
from project_store_data_access_layer.data_access import engine
from project_store_exception_layer.exception import CustomException as ApplicationException


router = APIRouter(prefix="/application", tags=["application"], responses= {"404": {"description": "Not Found"}})

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory=Configuration().TEMPLATE_DIR)
business_logic = BusinessLogic()

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(business_logic.get_db)):
    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
        todos = db.query(models.Application).all()
        return templates.TemplateResponse("index.html", {"request": request, "applications": todos, "user": user})
    except Exception as e:
        read_all_by_user_exception = ApplicationException(
        "Failed during Reading all user in method [{0}]"
            .format(read_all_by_user.__name__))
        raise Exception(read_all_by_user_exception.error_message_detail(str(e), sys))\
                from e

@router.get("/add-app", response_class=HTMLResponse)
async def add_new_app(request: Request):
    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
        return templates.TemplateResponse("add-app.html", {"request": request, "user": user})
    except Exception as e:
        add_new_app_exception = ApplicationException(
        "Failed during Adding New Application in method [{0}]"
            .format(add_new_app.__name__))
        raise Exception(add_new_app_exception.error_message_detail(str(e), sys))\
                from e

@router.post("/add-app", response_class=HTMLResponse)
async def create_app(request: Request, title: str = Form(...),description: str = Form(...),
                                github_url: str = Form(...), technology: str= Form(...), db: Session = Depends(business_logic.get_db)):
    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
        todo_model = models.Application()
        todo_model.title = title
        todo_model.description = description
        todo_model.github_url = github_url
        todo_model.technology = technology
        todo_model.owner_username = user.get("username")

        db.add(todo_model)
        db.commit()
        return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)
    except Exception as e:
        create_app_exception = ApplicationException(
        "Failed during Creating New Application in method [{0}]"
            .format(create_app.__name__))
        raise Exception(create_app_exception.error_message_detail(str(e), sys))\
                from e

@router.get("/view-app/{todo_id}", response_class=HTMLResponse)
async def view_app(request: Request, todo_id: int, db: Session = Depends(business_logic.get_db)):
    try:
        users = await get_current_user(request)
        if users is None:
            return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
        todo = db.query(models.Application).filter(models.Application.id == todo_id).first()
        return templates.TemplateResponse("view-app.html", {"request": request, "applications": todo, "user": users})
    except Exception as e:
        view_app_exception = ApplicationException(
        "Failed during Getting current user in method [{0}]"
            .format(view_app.__name__))
        raise Exception(view_app_exception.error_message_detail(str(e), sys))\
                from e

@router.post("/view-app/{todo_id}", response_class=HTMLResponse)
async def view_app_comit(request: Request, todo_id: int, title: str = Form(...),description: str = Form(...),
                                github_url: str = Form(...), technology: str= Form(...),\
                                db: Session = Depends(business_logic.get_db)):
    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
        todo = db.query(models.Application).filter(models.Application.id == todo_id).first()

        todo.title = title
        todo.description = description
        todo.github_url = github_url
        todo.technology = technology
        db.add(todo)

        db.commit()
        return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)
    except Exception as e:
        view_app_comit_exception = ApplicationException(
        "Failed during View application Comit in method [{0}]"
            .format(view_app_comit.__name__))
        raise Exception(view_app_comit_exception.error_message_detail(str(e), sys))\
                from e

@router.get("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_app(request: Request, todo_id: int, db: Session = Depends(business_logic.get_db)):
    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code= status.HTTP_302_FOUND)
        todo = db.query(models.Application).filter(models.Application.id == todo_id).first()
        if todo is None:
            return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)
        db.query(models.Application).filter(models.Application.id == todo_id).delete()
        db.commit()

        return RedirectResponse(url = '/application', status_code= status.HTTP_302_FOUND)
    except Exception as e:
        delete_app_exception = ApplicationException(
        "Failed during Deleting application in method [{0}]"
            .format(delete_app.__name__))
        raise Exception(delete_app_exception.error_message_detail(str(e), sys))\
                from e