import argparse
import requests

SERVER = "http://127.0.0.1:8000"
TOKEN = None

def get_token(username, password):
    global TOKEN
    try:
        resp = requests.post(
            f"{SERVER}/token", data={"username": username, "password": password}
        )
    except:
        raise Exception("Token generation failed! Argh!")
    if resp.ok:
        TOKEN = resp.json()["access_token"]
    else:
        raise Exception(resp.text)


def auth_header():
    if TOKEN is None:
        raise Exception("Token is not initialized!")
    return {"Authorization": f"Bearer {TOKEN}"}


def add_event(args):
    payload = {"start": args.start, "stop": args.stop, "tags": args.tags}
    try:
        resp = requests.post(f"{SERVER}/add_event", json=payload, headers=auth_header())
    except:
        raise Exception("Unable to add event")
    if resp.ok:
        print(resp.json())
    else:
        print(f"Failed to add event: {resp}")


def list_events(args):
    try:
        resp = requests.get(f"{SERVER}/list_events", headers=auth_header())
    except:
        raise Exception("Unable to list events")
    if resp.ok:
        print(resp.json())
    else:
        print(f"Failed to list events: {resp}")


def remove_events(args):
    payload = {"start": args.start, "stop": args.stop, "tags": args.tags}
    try:
        resp = requests.delete(
            f"{SERVER}/remove_events", json=payload, headers=auth_header()
        )
    except:
        raise Exception("Unable to remove events")
    if resp.ok:
        print(resp.json())
    else:
        print("Failed to remove event")


parser = argparse.ArgumentParser(description="CLI Client for Event Manager")
parser.add_argument("--user", required=True)
parser.add_argument("--password", required=True)

subparsers = parser.add_subparsers(dest="command")

parser_add = subparsers.add_parser("add")
parser_add.add_argument("--start", type=int, required=True)
parser_add.add_argument("--stop", type=int)
parser_add.add_argument("--tags", nargs="+", required=True)
parser_add.set_defaults(func=add_event)

parser_list = subparsers.add_parser("list")
parser_list.set_defaults(func=list_events)

parser_remove = subparsers.add_parser("remove")
parser_remove.add_argument("--start", type=int)
parser_remove.add_argument("--stop", type=int)
parser_remove.add_argument("--tags", nargs="+")
parser_remove.set_defaults(func=remove_events)

args = parser.parse_args()
if args.command:
    get_token(args.user, args.password)
    args.func(args)
else:
    parser.print_help()
