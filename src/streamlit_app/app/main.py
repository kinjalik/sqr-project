import streamlit as st
from components.login import login
from components.tasks import tasks

back_url = "http://localhost:8000"


# TODO: add caching or something
def main():
    st.title("InnoTasks")

    login(back_url)
    tasks(back_url)


if __name__ == "__main__":
    main()
