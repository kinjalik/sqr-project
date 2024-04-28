import requests
import streamlit as st

api = None


def _register_user(username, password):
    url = f"{api}/register"
    # TODO: password should be hashed on backend
    data = {
        "email": username,
        "hashed_password": password,
    }
    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 201:
        st.toast("Successfully registered", icon="✔")
        return True
    elif response.status_code == 400:
        st.error("Already registered!")
        return False
    else:
        st.error(response.text)
        return False


def _login_user(username, password):
    url = f"{api}/login"
    data = {"email": username, "hashed_password": password}
    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 200:
        st.toast("Successfully logged in", icon="✔")
        st.session_state.current_user = username
        return True
    elif response.status_code == 404:
        st.error("Wrong login or password")
        return False
    else:
        st.error(response.text)
        return False


def _auth_form():
    st.header("Login or Register")
    with st.form(key="auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        log_col, reg_col = st.columns([0.107, 0.893])
        with log_col:
            login_pressed = st.form_submit_button("Login", type="primary")
        with reg_col:
            register_pressed = st.form_submit_button("Register")

        if login_pressed or register_pressed:
            if username == "":
                st.warning("Please enter username")
                return
            if password == "":
                st.warning("Please enter password")
                return

        if login_pressed and _login_user(username, password):
            st.rerun()

        if register_pressed and _register_user(username, password) and _login_user(username, password):
            st.rerun()


def login(api_url: str):
    global api
    api = api_url

    if "current_user" not in st.session_state:
        _auth_form()
