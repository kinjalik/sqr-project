import uuid
from datetime import datetime, timedelta

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "http://localhost:8080/"
webdriverwait_timeout = 10


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(webdriverwait_timeout)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def credentials():
    return str(uuid.uuid4())


def _get_login_form(driver: WebDriver):
    username = driver.find_element(By.XPATH, '//input[@aria-label="Username"]')
    password = driver.find_element(By.XPATH, '//input[@aria-label="Password"]')
    login_button = driver.find_element(By.XPATH, '//button[@kind="primaryFormSubmit"]')
    register_button = driver.find_element(
        By.XPATH, '//button[@kind="secondaryFormSubmit"]'
    )

    return username, password, login_button, register_button


def _register(driver: WebDriver, username: str, password: str):
    username_field, password_field, _, register_button = _get_login_form(driver)

    username_field.send_keys(username)
    password_field.send_keys(password)
    register_button.click()

    try:
        WebDriverWait(driver, webdriverwait_timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[text()='✔ Successfully registered']")
            )
        )
    except TimeoutException:
        return False

    return True


def _login(driver: WebDriver, username: str, password: str):
    username_field, password_field, login_button, _ = _get_login_form(driver)

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    try:
        WebDriverWait(driver, webdriverwait_timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[text()='✔ Successfully logged in']")
            )
        )
    except TimeoutException:
        return False

    return True


def test_register_login_user(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Tasks']"))
    )


def test_already_registered(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    driver.refresh()

    ok = _register(driver, credentials, credentials)
    assert not ok

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()='Already registered!']"))
    )


def test_login_user(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    driver.refresh()

    assert _login(driver, credentials, credentials)

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Tasks']"))
    )


def test_login_user_wrong_password(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    driver.refresh()

    ok = _login(driver, credentials, "wrong")
    assert not ok

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[text()='Wrong login or password']")
        )
    )


def _get_task_edit_form(driver: WebDriver):
    text = driver.find_element(By.XPATH, '//input[@aria-label="Task Text"]')
    deadline = driver.find_element(
        By.XPATH, '//input[@data-testid="stDateInput-Input"]'
    )
    priority = driver.find_element(By.XPATH, '//input[@aria-label="Priority"]')

    save_button = driver.find_element(By.XPATH, '//button[@kind="primaryFormSubmit"]')
    cancel_button = driver.find_element(
        By.XPATH, '//button[@kind="secondaryFormSubmit"]'
    )

    return text, deadline, priority, save_button, cancel_button


def _get_task_show_form(driver: WebDriver):
    text = driver.find_element(By.XPATH, '//input[@aria-label="Task Text"]')
    deadline = driver.find_element(
        By.XPATH, '//input[@data-testid="stDateInput-Input"]'
    )
    priority = driver.find_element(By.XPATH, '//input[@aria-label="Priority"]')
    is_completed = driver.find_element(By.XPATH, '//input[@aria-label="Is Completed?"]')

    edit_button = driver.find_element(By.XPATH, '//*[text()="Edit"]')
    complete_button = driver.find_element(By.XPATH, '//*[text()="Complete"]')
    delete_button = driver.find_element(By.XPATH, '//*[text()="Delete"]')

    return (
        text,
        deadline,
        priority,
        is_completed,
        edit_button,
        complete_button,
        delete_button,
    )


def _task_create(driver: WebDriver, text: str, deadline: str, priority: str):
    add_task_button = driver.find_element(By.XPATH, '//button[@kind="secondary"]')
    add_task_button.click()

    text_field, deadline_field, priority_field, save_button, _ = _get_task_edit_form(
        driver
    )

    text_field.send_keys(text)
    deadline_field.send_keys(deadline)
    priority_field.send_keys(priority)
    save_button.click()

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[text()="Save"]'))
    )


def test_task_create(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    _task_create(
        driver,
        "Test Task",
        (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d"),
        "1",
    )

    text, deadline, priority, is_completed, _, _, _ = _get_task_show_form(driver)

    assert text.get_attribute("value") == "Test Task"
    assert deadline.get_attribute("value") == (
        datetime.now() + timedelta(days=1)
    ).strftime("%Y/%m/%d")
    assert priority.get_attribute("value") == "1"
    assert not is_completed.is_selected()


def test_task_create_cancel(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    add_task_button = driver.find_element(By.XPATH, '//button[@kind="secondary"]')
    add_task_button.click()

    text, deadline, priority, _, cancel_button = _get_task_edit_form(driver)

    text.send_keys("Test Task")
    deadline.send_keys((datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d"))
    priority.send_keys("1")
    cancel_button.click()

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[text()="Cancel"]'))
    )

    try:
        _get_task_edit_form(driver)
        assert False
    except NoSuchElementException:
        assert True
    except Exception:
        assert False


def test_task_delete(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    _task_create(
        driver,
        "Test Task",
        (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d"),
        "1",
    )

    delete_button = driver.find_element(By.XPATH, '//*[text()="Delete"]')
    delete_button.click()

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.invisibility_of_element_located(
            (By.XPATH, '//input[@aria-label="Task Text"]')
        )
    )


def test_task_complete(driver: WebDriver, credentials: str):
    driver.get(url)

    assert _register(driver, credentials, credentials)

    _task_create(
        driver,
        "Test Task",
        (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d"),
        "1",
    )

    is_completed = driver.find_element(By.XPATH, '//input[@aria-label="Is Completed?"]')
    assert not is_completed.is_selected()

    complete_button = driver.find_element(By.XPATH, '//*[text()="Complete"]')
    complete_button.click()

    WebDriverWait(driver, webdriverwait_timeout).until(
        EC.element_located_to_be_selected(
            (By.XPATH, '//input[@aria-label="Is Completed?"]')
        )
    )
