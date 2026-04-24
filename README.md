## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
Install ODBC Driver 18 for SQL Server:

Windows: winget install Microsoft.Data.SqlClient.ODBCDriver18

Linux: sudo apt-get install -y msodbcsql18

macOS: brew install msodbcsql18

Update connections.yaml with your DB credentials.

Run tests:

bash
pytest -v