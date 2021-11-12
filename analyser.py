import csv
import pprint
import sys

accounts = {}


def get_user_balance(user):
    """Get the final balance for a given user."""
    try:
        return sum([vl for vl in accounts[user]["balance"].values()])
    except KeyError:
        return 0


def get_or_create_account(user):
    """Get the user accounting."""
    if user not in accounts:
        accounts[user] = {"transactions": [], "balance": {}}
    return accounts[user]


def debit(data):
    """Create a debit transaction on user wallet."""
    user_account = get_or_create_account(data["from"])
    value = -float(data["value"])
    user_account["transactions"].append(
        {
            "date": data["date"],
            "type": "debit",
            "to": data["to"],
            "value": value,
        }
    )

    if not data["date"] in user_account["balance"]:
        user_account["balance"][data["date"]] = value
    else:
        user_account["balance"] += value

    user_account["current_balance"] = get_user_balance(data["from"])


def credit(data):
    """Create a credit transaction on user wallet."""
    user_account = get_or_create_account(data["to"])
    value = float(data["value"])
    user_account["transactions"].append(
        {
            "date": data["date"],
            "type": "credit",
            "from": data["from"],
            "value": value,
        }
    )

    if not data["date"] in user_account["balance"]:
        user_account["balance"][data["date"]] = value
    else:
        user_account["balance"] += value

    user_account["current_balance"] = get_user_balance(data["to"])


def analyse(filename):
    fieldnames = ["date", "from", "to", "value"]
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=fieldnames)

        for row in reader:
            debit(row)
            credit(row)

    pprint.pprint(accounts, indent=2)


if __name__ == "__main__":
    analyse(sys.argv[1])
