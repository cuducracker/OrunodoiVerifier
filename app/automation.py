from playwright.sync_api import sync_playwright, TimeoutError
from app.logger import logger


class EposAutomation:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # -------------------------------------
    # Start Browser
    # -------------------------------------

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(

            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
                ]

        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        self.page.goto(

            "https://epos.assam.gov.in/SRC_Trans_Int",

            wait_until="networkidle"

        )

        from app.logger import logger

        logger.info("Website Loaded Successfully")

    # -------------------------------------
    # Search RC
    # -------------------------------------

    def search_rc(self, rc_number):

        logger.info(f"Searching RC Number : {rc_number}")

        family_members = []

        try:

            self.page.locator("#rc_no").fill("")

            self.page.locator("#rc_no").fill(str(rc_number))

            self.page.get_by_role(

                "button",

                name="Submit"

            ).click()

            # Wait longer for slow government server

            self.page.wait_for_selector(

                "text=Member Details",

                timeout=60000

            )

            tables = self.page.locator("table")

            for i in range(tables.count()):

                table = tables.nth(i)

                if "Member Details" not in table.inner_text():

                    continue

                rows = table.locator("tbody tr")

                print(f"\nTotal Members Found: {rows.count()}")

                for j in range(rows.count()):

                    try:

                        name = rows.nth(j).locator("td").nth(1).inner_text().strip()

                        if name:

                            family_members.append(name)

                            print(f"{j+1}. {name}")

                    except Exception:

                        continue

                break

        except TimeoutError:

            logger.warning(f"Timeout while searching RC : {rc_number}")

        except Exception as e:

            print(f"Error searching RC : {rc_number}")

            logger.exception(e)

        return family_members

    # -------------------------------------
    # Stop Browser
    # -------------------------------------

    def stop(self):

        if self.context:

            self.context.close()

        if self.browser:

            self.browser.close()

        if self.playwright:

            self.playwright.stop()