import sys
from urllib import response
from wsgiref import validate

from starlette.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Request, Response, Form
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from project_store_entity_layer import entity as models
from project_store_data_access_layer.data_access import engine

# from project_store_business_logic_layer.business_logic import get_db, \
#                 get_password_hash, verify_password, authenticate_user, \
#                 create_access_token
from project_store_business_logic_layer.business_logic import BusinessLogic
from project_store_config_layer.configuration import Configuration
from project_store_exception_layer.exception import CustomException as AuthenticationException


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory=Configuration().TEMPLATE_DIR)

router = APIRouter(prefix="/auth", tags=["auth"], responses= {"401": {"description": "Not Authorized!!!"}}) 

business_logic = BusinessLogic()
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None
    
    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")



async def get_current_user(request: Request):
    try:
        token=request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, Configuration().SECRET_KEY, algorithms=[Configuration().ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        
        if username is None or user_id is None:
            return logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Detail Not Found")
    except Exception as e:
            load_get_current_user_exception = AuthenticationException(
            "Failed during Getting current user in method [{0}]"
                .format(get_current_user.__name__))
            raise Exception(load_get_current_user_exception.error_message_detail(str(e), sys))\
                 from e

@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(business_logic.get_db)):
    try:
        user = business_logic.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            return False
        token_expires = timedelta(minutes=60)
        token = business_logic.create_access_token(user.username,
                                    user.id,
                                    expires_delta=token_expires)

        response.set_cookie(key="access_token", value=token, httponly=True)
        return True
    except Exception as e:
        login_for_access_token_exception = AuthenticationException(
        "Failed during getting access token in method [{0}]"
            .format(login_for_access_token.__name__))
        raise Exception(login_for_access_token_exception.error_message_detail(str(e), sys))\
                from e  


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        authentication_page_exception = AuthenticationException(
        "Failed during Authenticating in method [{0}]"
            .format(authentication_page.__name__))
        raise Exception(authentication_page_exception.error_message_detail(str(e), sys))\
                from e  

@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(business_logic.get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/application", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(response= response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username and password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response

    except HTTPException:
        msg = "UnKnown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    except Exception as e:
        login_exception = AuthenticationException(
        "Failed during user Login in method [{0}]"
            .format(login.__name__))
        raise Exception(login_exception.error_message_detail(str(e), sys))\
                from e    


@router.get("/logout")
async def logout(request: Request):
    try:
        msg = "You have been logged out"
        response =  templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        response.delete_cookie(key="access_token")
        return response
    except Exception as e:
        logout_exception = AuthenticationException(
        "Failed during user Logout in method [{0}]"
            .format(logout.__name__))
        raise Exception(logout_exception.error_message_detail(str(e), sys))\
                from e

@router.get("/register", response_class=HTMLResponse)
async def authentication_page(request: Request):
    try:
        return templates.TemplateResponse("register.html", {"request": request})
    except Exception as e:
        authentication_page_exception = AuthenticationException(
        "Failed during Authenticating user in method [{0}]"
            .format(authentication_page.__name__))
        raise Exception(authentication_page_exception.error_message_detail(str(e), sys))\
                from e

@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request,
                        email: str = Form(...),
                        username: str= Form(...),
                        firstname: str= Form(...),
                        lastname: str= Form(...),
                        password: str= Form(...),
                        password2: str= Form(...),
                        db: Session = Depends(business_logic.get_db)):
    try:
        validation1 = db.query(models.Users).filter(models.Users.username == username).first()
        validation2 = db.query(models.Users).filter(models.Users.email == email).first()

        if password != password2 or validation1 is not None or validation2 is not None:
            msg = "Invalid Registration Request"
            return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
        
        user_model = models.Users()
        user_model.username = username
        user_model.email = email
        user_model.first_name = firstname
        user_model.last_name = lastname
        user_model.hashed_password = business_logic.get_password_hash(password)
        user_model.is_active = True

        db.add(user_model)
        db.commit()

        msg = "Registration Successful...Please Login to continue"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    except Exception as e:
        register_user_exception = AuthenticationException(
        "Failed during Register user in method [{0}]"
            .format(register_user.__name__))
        raise Exception(register_user_exception.error_message_detail(str(e), sys))\
                from e 