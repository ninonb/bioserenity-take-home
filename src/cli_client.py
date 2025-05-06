import argparse
import requests

SERVER = "http://127.0.0.1:8000/"
TOKEN = None

def get_token(username, password):
    global TOKEN
    resp = requests.post(f"{SERVER}/token", data={"username": username, "password": password})
    if resp.status_code == 200:
        TOKEN = resp.json()["access_token"]
    else:
        print("Authentication failed")
        exit(1)

def auth_header():
    return {"Authorization": f"Bearer {TOKEN}",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

def add_event(args):
    payload = {
        "start": args.start,
        "stop": args.stop,
        "tags": args.tags
    }
    resp = requests.post(f"{SERVER}/add_event", json=payload,  headers=auth_header())
    print(resp.json())

def list_events(args):
    resp = requests.get(f"{SERVER}/list_events", headers=auth_header())
    print(resp.json())

def remove_events(args):
    payload = {
        "start": args.start,
        "stop": args.stop,
        "tags": args.tags
    }
    resp = requests.post(f"{SERVER}/remove_events", json=payload, headers=auth_header())
    print(resp.json())

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