from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class TableComponent(BasePage):
    """
    Helpers for reading and interacting with HTML tables.
    Pass the table's locator when using each method.
    """

    def get_headers(self, table_locator: tuple) -> list[str]:
        """Return all column header texts."""
        table = self.find(table_locator)
        headers = table.find_elements(By.TAG_NAME, "th")
        return [h.text.strip() for h in headers]

    def get_row_count(self, table_locator: tuple) -> int:
        """Return number of data rows (tbody > tr)."""
        table = self.find(table_locator)
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        return len(rows)

    def get_cell(self, table_locator: tuple, row: int, col: int) -> str:
        """
        Return text of a specific cell (1-indexed).
        row=1 is the first data row, col=1 is the first column.
        """
        table = self.find(table_locator)
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row - 1].find_elements(By.TAG_NAME, "td")
        return cells[col - 1].text.strip()

    def get_row_data(self, table_locator: tuple, row: int) -> list[str]:
        """Return all cell texts for a given row (1-indexed)."""
        table = self.find(table_locator)
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row - 1].find_elements(By.TAG_NAME, "td")
        return [c.text.strip() for c in cells]

    def get_all_rows(self, table_locator: tuple) -> list[list[str]]:
        """Return all rows as a list of lists."""
        table = self.find(table_locator)
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        return [
            [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
            for row in rows
        ]

    def get_column_values(self, table_locator: tuple, col: int) -> list[str]:
        """Return all values in a given column (1-indexed)."""
        all_rows = self.get_all_rows(table_locator)
        return [row[col - 1] for row in all_rows if len(row) >= col]

    def find_row_by_text(self, table_locator: tuple, text: str) -> int:
        """
        Return 1-indexed row number where any cell contains the given text.
        Returns -1 if not found.
        """
        all_rows = self.get_all_rows(table_locator)
        for i, row in enumerate(all_rows, start=1):
            if text in row:
                return i
        return -1

    def click_cell_action(self, table_locator: tuple, row: int, col: int):
        """Click a link or button inside a specific cell (1-indexed)."""
        table = self.find(table_locator)
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row - 1].find_elements(By.TAG_NAME, "td")
        cells[col - 1].find_element(By.TAG_NAME, "a").click()

    def sort_by_column(self, table_locator: tuple, col: int):
        """Click a column header to trigger sorting (1-indexed)."""
        table = self.find(table_locator)
        headers = table.find_elements(By.TAG_NAME, "th")
        headers[col - 1].click()
