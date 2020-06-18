#! /usr/bin/env python
"""
Use selenium webdriver to automate booking a tee time
"""

from __future__ import print_function

import argparse
import sys
import time
from typing import Callable, Optional, cast

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select


def try_to_execute(action: Callable) -> None:
    error: Optional[Exception] = None
    for i in range(100):
        try:
            action()
            return
        except Exception as e:
            error = e
        time.sleep(0.1)
    raise cast(Exception, error)


# pylint: disable=missing-docstring
def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--username", help="Account username", type=str, required=True,
    )
    parser.add_argument(
        "--password", help="Account password", type=str, required=True,
    )
    parser.add_argument(
        "--date", help="Date to book tee time", type=str, required=True,
    )

    args = parser.parse_args(arguments)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1420,1080")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Remote(
    # command_executor="http://localhost:4444/wd/hub",
    # desired_capabilities=DesiredCapabilities.CHROME,
    # options=chrome_options,
    # )

    driver.get("https://www.bydubaigolf.com/MemberZone2/")

    # sign in
    driver.find_element_by_id("txtMembershipNo").send_keys(args.username)
    driver.find_element_by_id("txtPassword").send_keys(args.password)
    driver.find_element_by_id("btnSignIn").click()

    # click "book tee times"
    try_to_execute(
        lambda: driver.find_elements_by_xpath(
            '//*[@id="content"]/div/aside[1]/div/ul/li[2]/a'
        )[0].click()
    )

    def select_date() -> None:
        Select(
            driver.find_element_by_id("cphMainPlaceHolder_cphBody_ddlDate")
        ).select_by_value(args.date)
        driver.find_element_by_id("btnSubmit").click()

    # Select date
    try_to_execute(select_date)

    # Click through interstitial
    try_to_execute(
        lambda: driver.find_element_by_id("cphMainPlaceHolder_cphBody_Button1").click()
    )

    try_to_execute(lambda: driver.find_element_by_id("btnBook").click())

    try_to_execute(
        lambda: driver.execute_script('document.querySelector("#cnt1").click()')
    )
    try_to_execute(lambda: driver.find_element_by_id("btntTimeBook").click())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
