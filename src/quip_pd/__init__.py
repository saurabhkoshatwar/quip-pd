import pandas as pd
import requests

class QuipDataFrame:
    def __init__(self, quip_access_token: str, thread_id: str):
        self.token = quip_access_token
        self.thread_id = thread_id
        self.df = pd.DataFrame()
        self.api_url = f"https://platform.quip.com/1/spreadsheets/{thread_id}"
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.cell_locks = {}  # {(row, col): locked}

    def load(self):
        """Load data from the Quip spreadsheet into the DataFrame."""
        resp = requests.get(self.api_url, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()
        # Quip spreadsheet data is in 'cells' (row-major order)
        cells = data.get("cells", [])
        if not cells:
            self.df = pd.DataFrame()
            return
        self.df = pd.DataFrame(cells)
        # Parse lock info if available
        self.cell_locks = {}
        locks = data.get("cell_locks", {})
        for lock in locks.get("locked_cells", []):
            row, col = lock[0], lock[1]
            self.cell_locks[(row, col)] = True

    def sync(self):
        """Sync the DataFrame changes back to the Quip spreadsheet."""
        # This will update all cells (for simplicity)
        for row in range(self.df.shape[0]):
            for col in range(self.df.shape[1]):
                value = self.df.iat[row, col]
                payload = {
                    "location": {"row": row, "column": col},
                    "content": str(value)
                }
                url = f"{self.api_url}/cells/update"
                resp = requests.post(url, headers=self.headers, json=payload)
                resp.raise_for_status()

    def check_lock(self, row: int, col: int) -> bool:
        """Check if a cell is locked."""
        return self.cell_locks.get((row, col), False)

    def lock_cell(self, row: int, col: int):
        """Lock a cell in the Quip spreadsheet."""
        url = f"{self.api_url}/cells/lock"
        payload = {"location": {"row": row, "column": col}}
        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        self.cell_locks[(row, col)] = True 