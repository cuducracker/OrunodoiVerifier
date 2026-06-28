from playwright.sync_api import sync_playwright


class EposAutomation:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=300
        )

        self.context = self.browser.new_context()
        self.page = self.context.new_page()

        self.page.goto("https://epos.assam.gov.in/SRC_Trans_Int")

        self.page.wait_for_load_state("networkidle")

        print("Website Loaded Successfully")

    def search_rc(self, rc_number):

        print(f"\nSearching RC Number: {rc_number}")

        # Clear previous value
        self.page.locator("#rc_no").fill("")

        # Enter RC Number
        self.page.locator("#rc_no").fill(str(rc_number))

        # Click Submit
        self.page.get_by_role("button", name="Submit").click()

        # Wait for results
        self.page.wait_for_selector("text=Member Details", timeout=10000)

        # Find the correct table
        tables = self.page.locator("table")

        family_members = []

        for i in range(tables.count()):

            table = tables.nth(i)

            if "Member Details" in table.inner_text():

                rows = table.locator("tbody tr")

                print(f"\nTotal Members Found: {rows.count()}")

                for j in range(rows.count()):

                    name = rows.nth(j).locator("td").nth(1).inner_text().strip()

                    family_members.append(name)

                    print(f"{j+1}. {name}")

                break

        return family_members

    def stop(self):

        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()