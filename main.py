from typing import Optional
from fastapi import FastAPI, Request,Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import firestore
from models import Query
import starlette.status as status
from fastapi.responses import RedirectResponse


app = FastAPI()

firestore_db = firestore.Client()

firebase_request_adapter = requests.Request()

# Mount static files correctly
app.mount("/static", StaticFiles(directory="static"), name="static")

# Firebase Auth Request Adapter

# Set up templates directory
templates = Jinja2Templates(directory="templates")


def is_logged_in(request:Request):
    id_token = request.cookies.get("token")
    if not id_token:
        return False
    try:
        user_token = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        if user_token:
            return True
    except Exception as e:
        return False

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    return templates.TemplateResponse(
        "main.html",
        {"request": request}
    )
@app.get("/new", response_class=HTMLResponse)
async def root(request: Request):

    return templates.TemplateResponse(
        "new.html",
        {"request": request}
    )


def get_user(user_token):
    user = firestore_db.collection('users').document(user_token['user_id'])
    if not user.get().exists:
        user_data = {
            'name':'chish',
            'age':273
        }
    firestore_db.collection('users').document(user_token['user_id']).set(user_data)

    




#helper function to get pydantic model for querying 
    
def query_form(
    attribute: str = Form(...),
    operator: str = Form(...),
    value: str = Form(...)):
    return Query(attribute=attribute, operator=operator, value=value)

#team routes

    
    try:
        result = TeamService.compare_teams_attributes(team1,team2)
        return templates.TemplateResponse("compare_teams_result.html", {
            "request": request,
            "team1": result['team1'],
            "team2": result['team2'],
            "comparison": result['comparison']
        })
    except Exception as e:
        return HTMLResponse(content=str(e),status_code=404)