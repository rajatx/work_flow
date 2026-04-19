from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase

templates = Jinja2Templates(directory="app/templates")

def render(request, page, partial, context=None):
    if context is None:
        context = {}

# Fetch user data if access token is present in cookies
    user_data = None

    # Check if the request has cookies and an access token
    tocken = request.cookies.get("access_token")
    if tocken:
        try:
            response = supabase.auth.get_user(tocken)
            user_data = response.user
        except Exception as e:
            print(f"Auth error in renderer: {e}")
            user_data = None

    # Add request and user to context for template rendering
    context["request"] = request
    context["user"] = user_data

    # Render partial if it's an HTMX request, otherwise render the full page

    if request.headers.get("hx-request"):
        return templates.TemplateResponse(name=partial, context=context)
    return templates.TemplateResponse(name=page, context=context)