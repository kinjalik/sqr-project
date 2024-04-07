"""The main application file."""

import streamlit as st

AUTH_URL = "https://www.strava.com/oauth/authorize?" \
    "client_id=124461&response_type=code&" \
    "redirect_uri=http://localhost:8000/auth/token" \
    "&approval_prompt=force&scope=read"

st.write("- Hello there!")
st.write("- General Kenobi!")

st.link_button("auth", AUTH_URL)
