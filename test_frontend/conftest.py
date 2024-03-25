import datetime
import os
import random
import string

from urllib.parse import urlparse

import pytest
from playwright.sync_api import sync_playwright

AUTH_URL = os.getenv("AUTH_URL", "http://market-access.local:9880/auth/login/")
BASE_URL = os.getenv("BASE_FRONTEND_TESTING_URL", "http://market-access.local:9880/")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TEST_USERNAME = os.getenv("TEST_USERNAME", "test_user")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "test_password")


def is_https_url(url):
    """Determine if the given URL is an HTTPS URL."""
    parsed_url = urlparse(url)
    return parsed_url.scheme == "https"


def authenticate(page_obj, return_url):
    """Perform the authentication process."""

    # Navigate to the authentication URL.
    page_obj.goto(AUTH_URL)

    # Fill in the login form and submit it.
    page_obj.get_by_label("Email:").fill(TEST_USERNAME)
    page_obj.get_by_label("Password:").fill(TEST_PASSWORD)
    page_obj.get_by_role("button", name="login").click()

    # Wait for navigation to ensure the login process has completed.
    page_obj.wait_for_navigation()

    # After logging in, navigate to the return_url.
    page_obj.goto(return_url)


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    _page = context.new_page()

    # If the base URL is an HTTPS URL, perform the authentication process.
    if is_https_url(BASE_URL):
        # Perform the authentication process.
        authenticate(_page, BASE_URL)
    else:
        # For non-HTTPS URLs, just navigate to the base URL without authentication
        _page.goto(BASE_URL)

    yield _page

    context.close()


@pytest.fixture
def create_test_barrier(page):
    def _create_test_barrier(title):

        random_barrier_id = "".join(
            random.choice(string.ascii_uppercase) for i in range(5)
        )
        random_barrier_name = f"{title} - {datetime.datetime.now().strftime('%d-%m-%Y')} - {random_barrier_id}"

        page.get_by_role("link", name="Report a barrier").click()
        page.get_by_role("link", name="Start now").click()
        page.get_by_label("Barrier title").click()
        page.get_by_label("Barrier title").fill(random_barrier_name)
        page.get_by_label("Barrier description").click()
        page.get_by_label("Barrier description").fill("test description")
        page.get_by_role("button", name="Continue").click()

        page.locator("#status-radio-2").check()
        page.locator("#status-radio-3").check()
        page.locator(
            "#status-date-group-barrier-status-partially_resolved_date_0"
        ).click()
        page.locator(
            "#status-date-group-barrier-status-partially_resolved_date_0"
        ).fill("04")
        page.locator(
            "#status-date-group-barrier-status-partially_resolved_date_1"
        ).click()
        page.locator(
            "#status-date-group-barrier-status-partially_resolved_date_1"
        ).fill("2023")
        page.locator("#id_barrier-status-partially_resolved_description").click()
        page.locator("#id_barrier-status-partially_resolved_description").fill(
            "ifdshgihsdpihgf"
        )
        page.locator("#status-date-group-barrier-status-start_date_0").click()
        page.locator("#status-date-group-barrier-status-start_date_0").fill("03")
        page.locator("#status-date-group-barrier-status-start_date_1").click()
        page.locator("#status-date-group-barrier-status-start_date_1").fill("2024")
        page.get_by_role("button", name="Continue").click()
        page.get_by_role("combobox").select_option("TB00016")
        page.get_by_role("button", name="Continue").click()
        page.get_by_role("radio").first.check()
        page.get_by_role("button", name="Continue").click()
        page.locator("#main_sector_select").select_option(
            "9538cecc-5f95-e211-a939-e4115bead28a"
        )
        page.get_by_text("Add sector").click()
        page.locator("#sectors_select").select_option(
            "9738cecc-5f95-e211-a939-e4115bead28a"
        )
        page.get_by_text("Other sectors (optional) Add").click()
        page.locator("#sectors_select").select_option(
            "9638cecc-5f95-e211-a939-e4115bead28a"
        )
        page.get_by_role("button", name="Continue").click()
        page.get_by_placeholder("Search Company").click()
        page.locator("#search-companies-button").click()
        page.get_by_placeholder("Search Company").fill("Test LTD")
        page.get_by_placeholder("Search Company").press("Enter")
        page.get_by_text("TEST LIMITEDCompanies House").click()
        page.get_by_text("Add company").click()
        page.get_by_role("button", name="Continue").click()
        page.get_by_label("Goods", exact=True).check()
        page.get_by_label("Services", exact=True).check()
        page.get_by_label("Which goods, services or").click()
        page.get_by_label("Which goods, services or").fill("isfdgihisdhfgidsfg")
        page.get_by_role("button", name="Continue").click()
        page.locator("#continue-button").click()
        return f'{BASE_URL}/barriers/{page.url.split("/")[-3]}/'

    return _create_test_barrier
