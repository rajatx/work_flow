from fastapi import Request, APIRouter, Depends, HTTPException
from app.core.renderer import render
from app.supabase_client import supabase

router = APIRouter()

# Authentication guard to protect dashboard routes
async def auth_guard(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=307) 
    try:
        supabase.auth.get_user(token)
    except:
        raise HTTPException(status_code=307)


router = APIRouter(dependencies=[Depends(auth_guard)])
    


@router.get("/dashboard")
def dashboard(request: Request):
    return render(request,"pages/dashboard.html", "partials/partials-dashboard.html", {"request": request})