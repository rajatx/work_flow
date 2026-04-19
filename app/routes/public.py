from fastapi import Request, Form, APIRouter, Response
from fastapi.responses import HTMLResponse
from app.core.renderer import render
from app.supabase_client import supabase
import time

router = APIRouter()

@router.get("/")
def home(request: Request):
    faq_data = [
        {
            "id": 1,
            "question": "What services does your company offer?",
            "answer": "Our company specializes in SaaS solutions, offering tools for project management, team collaboration, and data analytics. We customize our offerings to meet the specific needs of businesses in diverse industries, empowering them to thrive in a digital landscape."
        },
        {
            "id": 2,
            "question": "How can I contact customer support?",
            "answer": "You can reach our customer support team by emailing admin@flowem.com, calling +91-9474154888, or using the live chat on our website. Our dedicated team is available 24/7 to assist with any inquiries or issues. <br> We're dedicated to delivering fast and efficient solutions to maximize your productivity. "
        },
        {
            "id": 3,
            "question": "What is your subscription policy?",
            "answer": "We offer a pay as you go subscription policy with a freemium model. Recharge your wallet and use when you want no monthly fees."
        }
    ]
    return render(request, "pages/home.html", "partials/partials-home.html", {"faq_data": faq_data, "request": request})

@router.get("/about")
def about(request: Request):
    return render(request, "pages/about.html", "partials/partials-about.html", {"request": request}) 

@router.get("/contact")
def contact_form(request: Request):
    return render(request, "pages/contact.html", "partials/partials-contact.html", {"request": request})   

# Simple in-memory store for tracking last submission times (for demonstration purposes)
last_submit_time = {}

@router.post("/submit-contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    company: str = Form(None),
    subject: str = Form(...),
    question: str = Form(...),
    honeypot: str = Form(None)  # Honeypot field for spam prevention
):
    
    # Check honeypot field
    if honeypot:
        return HTMLResponse(content="")# Ignore submissions that fill the honeypot field (likely bots)
    
    # Rate limiting based on client IP
    user_ip = request.client.host
    current_time = time.time()
    # Rate limiting: Allow one submission every 30 seconds per IP
    if user_ip in last_submit_time and current_time - last_submit_time[user_ip] < 60:
        return HTMLResponse(content="<div class='text-red-500 text-sm'>Too many messages! Please wait 1 minute.</div>")
    

    # Styles for success and error messages
    succsess_message = "p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 border border-green-200"
    error_message = "p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 border border-red-200"

    try:
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "subject": subject,
            "question": question
        }
        supabase.table("contacts").insert(data, returning="minimal").execute()

        # Update the last submission time for this IP
        last_submit_time[user_ip] = current_time
        
        return HTMLResponse(content=f"<div hx-get='/clear-msg' hx-trigger='load delay:5s' hx-swap='outerHTML' class='{succsess_message}'><strong>Success!</strong> Your message has been sent. We will contact you soon.</div>")
    except Exception as e:
        return HTMLResponse(content=f"<div hx-get='/clear-msg' hx-trigger='load delay:5s' hx-swap='outerHTML' class='{error_message}'><strong>Error!</strong> Something went wrong. Please try again later.</div>")


# Endpoint to clear messages after a delay (used in the success/error message auto-clear)
@router.get("/clear-msg")
def clear_msg():
    return HTMLResponse(content="") 




@router.get("/blog")
def blog(request: Request):
    return render(request, "pages/blog.html", "partials/partials-blog.html", {"request": request})

@router.get("/services")
def services(request: Request):
    return render(request, "pages/services.html", "partials/partials-services.html", {"request": request})

@router.get("/appointment")
def appointment(request: Request):
    return render(request, "pages/appointment.html", "partials/partials-appointment.html", {"request": request})

@router.get("/signup")
def signup_form(request: Request):
    return render(request, "pages/signup.html", "partials/partials-signup.html", {"request": request})    

@router.post("/signup")
def signup(
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    error_style = "p-3 mb-4 text-sm text-red-800 rounded-lg bg-red-50 border border-red-200 text-center"

    if password != confirm_password:
        return HTMLResponse(content=f"<div class='{error_style}'>Passwords do not match!</div>")

    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options":{
                "data": {
                    "full_name": full_name,
                    "phone": phone
                }
            }
        })

        if res.session:
            user_id = res.user.id
            supabase.table("profiles").insert({
                "id": user_id, "full_name": full_name, "phone": phone
            }).execute()

            response = Response(headers={"HX-Redirect": "/dashboard"})
            response.set_cookie(key="access_token", value=res.session.access_token, httponly=True)
            return response
        
        return HTMLResponse(content=f"<div class='text-green-500 text-center'>Account created! Please login.</div>")
    except Exception as e:
        error_message = str(e)
        display_message = "An error occurred during signup. Please try again."
        if "User already registered" in error_message.lower():
            display_message = "This email is already registered. Please login or use a different email."
        elif "row-level security" in error_message.lower():
            display_message = "Database configuration error (RLS Policy)."
        elif "password" in error_message.lower():
            display_message = "Password is too weak or invalid."
        return HTMLResponse(content=f"<div class='{error_style}'> {display_message}</div>")

@router.get("/login")
def login_form(request: Request):
    return render(request, "pages/login.html", "partials/partials-login.html", {"request": request})

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})

        response = Response(headers={"HX-Redirect": "/dashboard"})
        response.set_cookie(key="access_token", value=res.session.access_token, httponly=True)
        return response
    except Exception:
        return HTMLResponse(content=f"<div class='p-3 mb-4 text-sm text-red-800 rounded-lg bg-red-50 border border-red-200 text-center'>Invalid email or password!</div>")

@router.get("/logout")
def logout(request: Request):
    referer = request.headers.get("referer", "/")
    response = Response(headers={"HX-Redirect": referer})
    response.delete_cookie("access_token")
    return response