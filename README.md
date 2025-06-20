# quip-pd

A DataFrame-like library for Quip spreadsheets with sync, lock, and cell management features.

## Features
- Load data from a Quip spreadsheet
- Modify data in a pandas-like DataFrame
- Sync changes back to Quip
- Check and lock cells

## Usage
```python
from quip_pd import QuipDataFrame

qdf = QuipDataFrame(quip_access_token="YOUR_TOKEN", thread_id="YOUR_THREAD_ID")
qdf.load()
qdf.df[0, 0] = "new value"  # Modify data
qdf.sync()  # Sync changes back to Quip
```