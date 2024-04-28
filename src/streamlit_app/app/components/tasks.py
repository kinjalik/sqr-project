import datetime
from typing import Literal

import requests
import streamlit as st

api = None


def _create_task(text: str, deadline: datetime.datetime, priority: int):
    url = f"{api}/task"
    data = {
        "user": st.session_state.current_user,
        "text": text,
        "deadline": deadline.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": priority,
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return True
    else:
        print(response.text)
        return False


def _delete_task(task_id):
    url = f"{api}/task"
    data = {"id": task_id}
    response = requests.delete(url, json=data)
    if response.status_code == 204:
        return True
    else:
        print(response.text)
        return False


def _get_tasks():
    url = f"{api}/tasks"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return []


def _edit_task(id, text, deadline, priority, is_completed):
    url = f"{api}/task"
    data = {
        "id": id,
        "user": st.session_state.current_user,
        "text": text,
        "deadline": deadline,
        "prior": priority,
        "is_completed": is_completed,
    }
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return True
    else:
        print(response.text)
        return False


def _task_form(id: str | None, mode: Literal["show", "edit"]):
    with st.form(key=f"task_form_{id}"):
        text = st.text_input("Task Text", disabled=mode == "show")
        deadline = st.date_input("Deadline", disabled=mode == "show")
        priority = st.number_input(
            "Priority", min_value=1, max_value=5, value=3, disabled=mode == "show"
        )
        if mode == "edit":
            is_completed = st.checkbox("Is Completed?", disabled=mode == "show")
        else:
            is_completed = False

        l_col, r_col = st.columns([0.1, 0.9])
        if mode == "edit":
            with l_col:
                save_submitted = st.form_submit_button("Save")
            with r_col:
                cancel_submitted = st.form_submit_button("Cancel")

            if save_submitted:
                success = None
                if id is not None:
                    success = _edit_task(id, text, deadline, priority, is_completed)
                else:
                    success = _create_task(text, deadline, priority)
                st.toast(success)
                if success:
                    st.toast("Saved successfully", icon="✔")
                    st.session_state[f"task_mode_{id}"] = "show"
                    st.rerun()
                else:
                    st.error("Failed to save", icon="❌")
            if cancel_submitted:
                st.session_state[f"task_mode_{id}"] = "show"
                st.rerun()
        if mode == "show":
            with l_col:
                edit_submitted = st.form_submit_button("Edit")
            with r_col:
                delete_submitted = st.form_submit_button("Delete")

            if edit_submitted:
                st.session_state[f"task_mode_{id}"] = "edit"
                st.rerun()
            if delete_submitted:
                if _delete_task(id):
                    st.toast("Successfully deleted task", icon="✔")
                    st.rerun()
                else:
                    st.error("Failed to delete task", icon="❌")


def _tasks_form():
    st.header("Tasks")

    for task in st.session_state.tasks:
        with st.expander(task["id"]):
            _task_form(task["id"], st.session_state[f"task_mode_{task['id']}"])

    # add_task = st.button("Add Task")
    # if add_task:
    _task_form(None, "edit")


def tasks(api_url: str):
    global api
    api = api_url

    if "current_user" in st.session_state:
        st.session_state.tasks = _get_tasks()
        for task in st.session_state.tasks:
            if f"task_mode_{task['id']}" not in st.session_state:
                st.session_state[f"task_mode_{task['id']}"] = "show"

        _tasks_form()
