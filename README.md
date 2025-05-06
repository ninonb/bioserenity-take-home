# BioSerenity take home

Run server locally after `cd src`:
```commandline
 uvicorn server:app --reload --port 8000 
```
You can then access the OpenAPI with `http://127.0.0.1:8000/docs`.

Example usage with CLI client:
```
python cli_client.py --user nancy --password secret add --start 1683123456 --tags work
python cli_client.py --user nancy --password secret list
python cli_client.py --user nancy --password secret remove --tags work
```

## Future implementations:
* Add collection with 'users' and their passwords in MongoDB, so that they log into the database.
* Can change so that `add_event` could perform bulk insert operations, instead of using `insert_one` with `pymongo`, we would use `insert_many` and allow the user to pass a list as the first argument.
* Implement a cache for the token.
* Dockerize with `Dockerfile` and `docker-compose.yml`.