import pytest
import yaml
from data_validation.profiler import run_profiles

@pytest.fixture(scope="session")
def profiles():
    return run_profiles()

@pytest.fixture(scope="session")
def catalog():
    with open("data_validation/catalog.yaml") as f:
        return yaml.safe_load(f)

def generate_rule_params(catalog):
    params = []
    for table in catalog["tables"]:
        table_name = table["name"]
        for rule in table["rules"]:
            if "unique" in rule:
                params.append((table_name, f"unique_{rule['unique']}"))
            if "not_null" in rule:
                for col in rule["not_null"]:
                    params.append((table_name, f"not_null_{col}"))
            if "distinct" in rule:
                params.append((table_name, f"distinct_{rule['distinct']}"))
            if "allow_nulls_except" in rule:
                except_col = rule["allow_nulls_except"]
                # generate nulls_allowed_* for all columns except the one listed
                # you can also introspect schema dynamically if needed
                for col in table.get("columns", []):
                    if col != except_col:
                        params.append((table_name, f"nulls_allowed_{col}"))
    return params

@pytest.mark.parametrize("table_name, rule", generate_rule_params(yaml.safe_load(open("data_validation/catalog.yaml"))))
def test_rules(profiles, table_name, rule):
    profile = next(p for p in profiles if p["table"] == table_name)
    assert profile["rules"][rule], f"Rule {rule} failed for table {table_name}"
