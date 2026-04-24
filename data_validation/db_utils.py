import yaml
import pyodbc

def load_yaml(path: str) -> dict:
    """Load a YAML file and return its contents as a dict."""
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_connection(conn_file: str, conn_name: str):
    """
    Build a pyodbc connection from connections.yaml.
    Supports Azure SQL and Oracle.
    """
    cfg = load_yaml(conn_file)[conn_name]

    if conn_name == "azure_sql":
        conn_str = (
            f"DRIVER={{{cfg['driver']}}};"
            f"SERVER={cfg['server']};"
            f"DATABASE={cfg['database']};"
            f"UID={cfg['username']};"
            f"PWD={cfg['password']};"
            f"Encrypt={cfg.get('encrypt','yes')};"
            f"TrustServerCertificate={cfg.get('trust_server_certificate','no')};"
            f"Connection Timeout={cfg.get('timeout',30)};"
        )
    elif conn_name == "oracle":
        conn_str = (
            f"DRIVER={{{cfg['driver']}}};"
            f"DBQ={cfg['host']}:{cfg['port']}/{cfg['service_name']};"
            f"UID={cfg['username']};"
            f"PWD={cfg['password']}"
        )
    else:
        raise ValueError(f"Unsupported connection type: {conn_name}")

    return pyodbc.connect(conn_str)
