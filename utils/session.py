import streamlit as st


def get_page() -> str:
    return st.query_params.get("page", "landing")


def set_page(page: str):
    st.query_params["page"] = page


def clear_session():
    for key in ["authenticated", "username", "name", "role", "email"]:
        st.session_state.pop(key, None)
    st.query_params.clear()
