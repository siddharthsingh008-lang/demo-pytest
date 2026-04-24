import pandas as pd
from data_validation.db_utils import load_yaml, get_connection

def profile_table(conn, table_name):
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    return df

def apply_rules(df, rules):
    results = {}
    for rule in rules:
        if "unique" in rule:
            col = rule["unique"]
            results[f"unique_{col}"] = df[col].is_unique
        if "not_null" in rule:
            for col in rule["not_null"]:
                results[f"not_null_{col}"] = df[col].notnull().all()
        if "distinct" in rule:
            col = rule["distinct"]
            results[f"distinct_{col}"] = len(df[col]) == df[col].nunique()
        if "allow_nulls_except" in rule:
            except_col = rule["allow_nulls_except"]
            for col in df.columns:
                if col != except_col:
                    results[f"nulls_allowed_{col}"] = df[col].isnull().any()
    return results

def run_profiles(conn_file="data_validation/connections.yaml",
                 catalog_file="data_validation/catalog.yaml"):
    catalog = load_yaml(catalog_file)
    results = []
    for tbl in catalog["tables"]:
        conn = get_connection(conn_file, tbl["connection"])
        df = profile_table(conn, tbl["name"])
        rule_results = apply_rules(df, tbl.get("rules", []))
        results.append({"table": tbl["name"], "rules": rule_results})
    return results
