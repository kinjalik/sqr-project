import datetime
from typing import Literal

import requests
import streamlit as st

NO_ID = -1

api = None


def _create_task(text: str, deadline: datetime.datetime, prior: int):
    url = f"{api}/task"
    data = {
        "user": st.session_state.current_user,
        "text": text,
        "deadline": deadline.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return int(response.json().get("task_id"))
    else:
        print(response.text)
        return NO_ID


def _delete_task(task_id):
    url = f"{api}/task/{task_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        return True
    else:
        print(response.text)
        return False


def _get_tasks():
    url = f"{api}/tasks"
    response = requests.get(url)
    if response.status_code == 200:
        tasks = response.json().get("tasks")
        for task in tasks:
            task["deadline"] = datetime.datetime.strptime(task["deadline"], "%Y.%m.%d %H:%M:%S")
        return tasks
    else:
        print(response.text)
        return []


def _edit_task(id, text, deadline, prior, is_completed):
    url = f"{api}/task"
    data = {
        "id": id,
        "user": st.session_state.current_user,
        "text": text,
        "deadline": deadline,
        "prior": prior,
        "is_completed": is_completed,
    }
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return True
    else:
        print(response.text)
        return False
    
def _complete_task(id):
    url = f"{api}/task/{id}/complete"
    response = requests.put(url)
    if response.status_code == 204:
        return True
    else:
        return False

def _switch_task_mode(id: int):
    if id in st.session_state.edited_tasks:
        st.session_state.edited_tasks.pop(id)
    else:
        st.session_state.edited_tasks[id] = st.session_state.shown_tasks[id]

def _task_form(task: dict, mode: Literal["show", "edit"]):
    id = task.get("id")
    creating = id is NO_ID
    with st.form(key=f"task_form_{id}"):
        text = st.text_input("Task Text", task.get("text"), disabled=mode == "show")
        deadline = st.date_input("Deadline", task.get("deadline"), disabled=mode == "show")
        prior = st.number_input(
            "Priority", min_value=1, max_value=5, value=task.get("prior"), disabled=mode == "show"
        )
        if not creating:
            is_completed = st.checkbox("Is Completed?", task.get("is_completed"), disabled=mode == "show")

        if mode == "edit":
            l_col, r_col = st.columns([0.1, 0.9])
            with l_col:
                save_submitted = st.form_submit_button("Save", type="primary")
            with r_col:
                cancel_submitted = st.form_submit_button("Cancel")

            if save_submitted:
                if text == None or text == "":
                    st.error("Task text cannot be empty", icon="❌")
                    return
                if prior is None or (prior < 1 or prior > 5):
                    st.error("Priority must be between 1 and 5", icon="❌")
                    return

                if creating:
                    id = _create_task(text, deadline, prior)
                    success = id is not NO_ID
                    if success:
                        st.session_state.edited_tasks[id] = st.session_state.edited_tasks.pop(NO_ID)
                else:
                    success = _edit_task(id, text, deadline, prior, is_completed)

                if success:
                    st.toast("Saved successfully", icon="✔")
                    _switch_task_mode(id)
                    st.rerun()
                else:
                    st.error("Failed to save", icon="❌")
            if cancel_submitted:
                _switch_task_mode(id)
                st.rerun()
        elif mode == "show":
            l_col, m_col, r_col = st.columns([0.1, 0.78, 0.12])
            with l_col:
                edit_submitted = st.form_submit_button("Edit", type="primary")
            with m_col:
                complete_submitted = False
                if not is_completed:
                    complete_submitted = st.form_submit_button("Complete")
            with r_col:
                delete_submitted = st.form_submit_button("Delete")

            if edit_submitted:
                _switch_task_mode(id)
                st.rerun()
            if complete_submitted:
                if _complete_task(id):
                    st.toast("Successfully completed task", icon="✔")
                    st.rerun()
                else:
                    st.error("Failed to complete task", icon="❌")
            if delete_submitted:
                if _delete_task(id):
                    st.toast("Successfully deleted task", icon="✔")
                    st.rerun()
                else:
                    st.error("Failed to delete task", icon="❌")


def _tasks_form():
    st.header("Tasks")
    
    for _, task in st.session_state.edited_tasks.copy().items():
        _task_form(task, "edit")

    for _, task in st.session_state.shown_tasks.items():
        _task_form(task, "show")

    add_task = st.button("Add Task", disabled=NO_ID in st.session_state.edited_tasks)
    if add_task:
        task = { "id": NO_ID }
        st.session_state.edited_tasks[task.get("id")] = task
        _task_form(task, "edit")


def tasks(api_url: str):
    global api
    api = api_url

    if "current_user" in st.session_state:
        if st.session_state.get("edited_tasks") is None:
            st.session_state.edited_tasks = {}
        st.session_state.shown_tasks = {task["id"]: task for task in _get_tasks() if task["id"] not in st.session_state.edited_tasks}

        _tasks_form()
