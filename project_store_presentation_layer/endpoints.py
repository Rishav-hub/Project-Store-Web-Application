from fastapi import FastAPI
from project_store_data_access_layer.data_access import engine
from project_store_entity_layer import entity as models
from project_store_business_logic_layer import auth, applications
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# @app.get("/")
# async def root():
#     return {"Database": "Created"}
print("Hello")
app.mount("/static", StaticFiles(directory="project_store_presentation_layer/static"), name="static")
print("Static")
@app.get("/")
async def root():
    print('here')
    return RedirectResponse("/application", status_code=status.HTTP_302_FOUND)
app.include_router(auth.router)
app.include_router(applications.router)
