from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.security.auth import login,  create_session_cookies, AUTH_ENABLED

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if not AUTH_ENABLED:
        return RedirectResponse("/", status_code=302)
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login — DevInfra</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Inter', sans-serif;
                background: #0f1117;
                color: #e2e8f0;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .card {
                background: #1e2330;
                border: 1px solid #2d3348;
                border-radius: 12px;
                padding: 2rem;
                width: 100%;
                max-width: 360px;
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }
            .logo-row {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .logo {
                width: 36px;
                height: 36px;
                background: #534AB7;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                color: white;
            }
            .app-name { font-size: 15px; font-weight: 600; color: #f1f5f9; }
            .app-sub  { font-size: 12px; color: #64748b; }
            .form {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .field {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            label { font-size: 12px; color: #94a3b8; }
            input {
                background: #0f1117;
                border: 1px solid #2d3348;
                border-radius: 8px;
                padding: 10px 12px;
                color: #e2e8f0;
                font-size: 14px;
                font-family: 'Inter', sans-serif;
                outline: none;
                transition: border-color 0.2s;
            }
            input:focus { border-color: #534AB7; }
            button {
                background: #534AB7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Inter', sans-serif;
                cursor: pointer;
                transition: background 0.2s;
                margin-top: 4px;
            }
            button:hover { background: #6459c4; }
            .error {
                background: #2d1515;
                border: 1px solid #7f1d1d;
                color: #ef4444;
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="logo-row">
                <div class="logo">D</div>
                <div>
                    <div class="app-name">DevInfra Monitor</div>
                    <div class="app-sub">sign in to continue</div>
                </div>
            </div>
            <form class="form" method="post" action="/login">
                <div class="field">
                    <label>Username</label>
                    <input type="text" name="username" autofocus autocomplete="username" />
                </div>
                <div class="field">
                    <label>Password</label>
                    <input type="password" name="password" autocomplete="current-password" />
                </div>
                <button type="submit">Sign in</button>
            </form>
        </div>
    </body>
    </html>
    """

@router.post("/login")
def handle_login(username: str = Form(...), password:str = Form(...)):
    if login(username, password):
        cookie_value = create_session_cookies(username)
        response = RedirectResponse("/", status_code=302)
        response.set_cookie(          
                key="session",
                value= cookie_value,
                httponly=True,
                max_age=86400,
                samesite="lax"
            )
        return response
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login — DevInfra</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Inter', sans-serif;
                background: #0f1117;
                color: #e2e8f0;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .card {
                background: #1e2330;
                border: 1px solid #2d3348;
                border-radius: 12px;
                padding: 2rem;
                width: 100%;
                max-width: 360px;
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }
            .logo-row {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .logo {
                width: 36px;
                height: 36px;
                background: #534AB7;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                color: white;
            }
            .app-name { font-size: 15px; font-weight: 600; color: #f1f5f9; }
            .app-sub  { font-size: 12px; color: #64748b; }
            .form {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .field {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            label { font-size: 12px; color: #94a3b8; }
            input {
                background: #0f1117;
                border: 1px solid #2d3348;
                border-radius: 8px;
                padding: 10px 12px;
                color: #e2e8f0;
                font-size: 14px;
                font-family: 'Inter', sans-serif;
                outline: none;
                transition: border-color 0.2s;
            }
            input:focus { border-color: #534AB7; }
            button {
                background: #534AB7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Inter', sans-serif;
                cursor: pointer;
                transition: background 0.2s;
                margin-top: 4px;
            }
            button:hover { background: #6459c4; }
            .error {
                background: #2d1515;
                border: 1px solid #7f1d1d;
                color: #ef4444;
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="logo-row">
                <div class="logo">D</div>
                <div>
                    <div class="app-name">DevInfra Monitor</div>
                    <div class="app-sub">sign in to continue</div>
                </div>
            </div>
            <form class="form" method="post" action="/login">
                <div class="field">
                    <label>Username</label>
                    <input type="text" name="username" autofocus autocomplete="username" />
                </div>
                <div class="field">
                    <label>Password</label>
                    <input type="password" name="password" autocomplete="current-password" />
                </div>
                <button type="submit">Sign in</button>
            </form>
            <div class="error">incorrect username or password</div>
        </div>
    </body>
    </html>
    """, status_code=401)


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("session")
    return response












