import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://footytips.espn.com.au/")
    page.get_by_role("button", name="Login").click()
    page.locator("iframe[name=\"oneid-iframe\"]").content_frame.get_by_test_id("InputIdentityFlowValue").click()
    page.locator("iframe[name=\"oneid-iframe\"]").content_frame.get_by_test_id("InputIdentityFlowValue").fill("rossdem699@gmail.com")
    page.locator("iframe[name=\"oneid-iframe\"]").content_frame.get_by_test_id("BtnSubmit").click()
    page.locator("iframe[name=\"oneid-iframe\"]").content_frame.get_by_test_id("InputPassword").click()
    page.locator("iframe[name=\"oneid-iframe\"]").content_frame.get_by_test_id("InputPassword").fill("espnPnmope69")
    page.locator("iframe[name=\"oneid-iframe\"]").content_frame.get_by_test_id("BtnSubmit").click()
    page.get_by_role("link", name="Edit Tips").click()
    page.locator(".MuiFormControlLabel-root.MuiFormControlLabel-labelPlacementEnd.formControlLabel.right > .MuiButtonBase-root").first.click()
    page.locator("[id=\"matches.4\"] > .Container-sc-1kjg77g-0 > .MuiFormGroup-root > .Container-sc-mff5ij-0.iSQNly > .MuiFormControlLabel-root > .MuiButtonBase-root").click()
    page.get_by_role("button", name="SubmitTips").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
