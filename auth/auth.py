import streamlit as st
from utils.session import set_page, get_page, clear_session


def login_user(user: dict):
    st.session_state["authenticated"] = True
    st.session_state["username"]      = user["username"]
    st.session_state["name"]          = user["full_name"]
    st.session_state["role"]          = user["role"]
    st.session_state["email"]         = user["email"]


def logout():
    clear_session()
    set_page("landing")
    st.rerun()


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def require_auth() -> bool:
    if is_authenticated():
        return True
    page = get_page()
    if page == "login":
        from login.login_view import show
        show()
    elif page == "signup":
        from signup.signup_view import show
        show()
    else:
        from landing.landing_view import show
        show()
    return False
