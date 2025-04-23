# fastAPI Auth template

The project can handle auth login and register with JWT Tokens, have the structure for begin others projects.

To init the project active the enviroment and install requirements and run (Depends on postgresDB)
Then enter in the terminal to src folder and run in console:

```console
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

to init in dockers containers run the docker-compose to up the postgresdb and fastapi services with

```console
docker-compose up
```
