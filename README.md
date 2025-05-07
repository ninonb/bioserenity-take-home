# BioSerenity take home

## Using with OpenAPI:
Run server locally after `cd src`:
```commandline
 uvicorn server:app --reload --port 8000 
```
You can then access the OpenAPI with `http://127.0.0.1:8000/docs` and use the endpoints there if you'd like.

## Example usage with CLI client:
Where there is a example user 'your_username' and example password 'your_password', in our MongoDB.
Here we can add an event, list all events, and remove events.

```
python cli_client.py --user your_username --password your_password add --start 123 --stop 456 --tags work
python cli_client.py --user your_username --password your_password list
python cli_client.py --user your_username --password your_password remove --start 123 --stop 456 --tags work
```

## Future implementations:
* Can change so that `add_event` could perform bulk insert operations, instead of using `insert_one` with `pymongo`, we would use `insert_many` and allow the user to pass a list as the first argument.
* Implement a cache for the token.
* Dockerize with `Dockerfile` and `docker-compose.yml`.
* Change so that `list_events` lists specific events, not just all events.
* Tests, tests, tests...
* There is always more that can be done ;-)