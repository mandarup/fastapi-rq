
# Generic REST Server For Queuing Jobs


In its current form, this is a generic server with redis for task queuing.


## API Documentation

Swagger UI is available at `http://0.0.0.0:8000/docs` if running locally  or `http://<ip-address>/docs`.


## Set Up


1) Clone the git repo ::sh

    `$git clone <thisrepo>`

2) Add any credential files expected by the workers to the root of project dir.

    # for examle
    # .testtaskcfg   

3) Off you go


## Steps in a production cycle

- Help
    We will be using `docker compose`, so first, install it if you don't have it and feel free to look up help.

        $ docker-compose --help

    There is also help for each subcommand, e.g.

        $ docker-compose  up --help

1. System up


    `$ docker-compose up --build [--remove-orphans  --detach] `

    This will build and  spin up all the docker containers. Refer to docker-compose for details.
    To see all the docker containers that are spun up, run `$docker ps`  in shell.

1. Submit jobs using REST API

    a) curl

        $ curl -X POST  "http://0.0.0.0:8000/jobs/" -H "Content-Type: application/json" --data '{"queuename":"testtask-low",  "jobtype":"testtask", "jobargs":{""}}'

    b) Swagger (useful for testing)

    Hit `localhost:8000/docs` in browser (replace localhost with url/IP address if not on local machine) and test the API interactively.

1. Job Status

    a) Check jobs via URL endpoints


    - To list all jobs
    `http://localhost:8000/jobs/`

    - To get a specific job
    `http://localhost:8000/jobs/<jobid>`

    - You can also filter jobs like
    `http://localhost:8000/jobs/?status=RUNNING&queuename=testtask-low`

    b) You can also use RQ-dashboard to see the queued jobs.
    `http://localhost:9181`


3. System down (if needed, for whatever reason)

    `$ docker-compose down`


## Adding Tasks and Queues

### Adding a new task

1) Edit `app/task_config.py`  to add desired tasks
2) Add this task to `argparse.ArgumentParser:--jobtype` accepted choices.
3) Add this task to `app.main.JobTypeEnum` for payload validation

### Adding a new set of workers and queues for the task
If the new task is independent, then it is likely that you'd want a separate set of workers
specifically for this task. To do this, follow these steps:

1) Add an entry to `supervisord.conf`. For example, for a new task called  `foobar`

    [program:rqworker-foobar]
    ;NOTE: it is critical to pass  settings file  as arg, wihout it the dockerized version fails
    command=rq worker  foobar-high foobar-low -P /usr/src -c redis_settings
    process_name=%(program_name)s_%(process_num)s
    numprocs=20
    priority=2
    startretries=10

NOTE: This defines two queues `foobar-high` and `foobar-low`, which  share the same set of workers,
and `foobar-high` takes priority - set in the order in which the queues are defined.

3) Add these queues to `app.main.QueueEnum` for payload validation



## System Components


Following components are connected together via `docker-compose.yaml`



1. REST API Web Server
    - Dockerfile.app
    - requirements.app.txt

1. Redis Database
    - redis.conf
    - redis_settings.py  (This is actually to help workers)
    *Note*: redis volume is mapped to `./data:/usr/src/data`  [local:docker]

1. Workers
    - Dockerfile.workers
    - supervisord.conf
    - requirements.workers.txt

1. Dashboard
    - Dockerfile.rqdashboard


1. SQLite DB   (Implicit component - not defined in docker-compose)
    This is shared by app (webserver) and the workers via shared volume mapped to `./data:/usr/src/data`  [local:docker]

    ```
    app/
    |__ database/
    |__ |__ models.py  # SQLAlchemy Model
    |__ |__ schema.py  # Pydantic Schema
    |__ |__ crud.py    # SQL CRUD queries
    |__ |__ __init__.py
    ```



## Debugging


A. Debugging containers

1. get list of containers

    ```
        $ docker ps
        CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
        69ef48011367        rq-dashboard        "/bin/bash -c 'rq-da…"   13 minutes ago      Up 13 minutes       0.0.0.0:9181->9181/tcp   redis-server_rq-dashboard_1
        ba3e701a5943        app                 "uvicorn app.main:ap…"   13 minutes ago      Up 13 minutes       0.0.0.0:8000->8000/tcp   app
        1c735115c507        workers             "/bin/bash -c 'super…"   13 minutes ago      Up 13 minutes                                redis-server_workers_1
        aaa49905a50f        redis:latest        "docker-entrypoint.s…"   13 minutes ago      Up 13 minutes       0.0.0.0:6379->6379/tcp   redis-server_redis_1
        8a6a40d1e839        registry            "/entrypoint.sh /etc…"   3 days ago          Up 13 hours         0.0.0.0:5000->5000/tcp   registry
    ```

1. Enter the desired container shell in interactive mode, e.g. for the workers container

    ```
    $ docker exec -it 1c735115c507 /bin/bash
    # or even better, by image name
    $ docker exec -it app /bin/bash
    ```

B. The package follows relative import convention. A side effect is issues when trying to run python scripts directly (say, for debugging). In order to run a script directly, run it as a module

    $cd /usr/src
    $python -m app.tasks.testtask.submit --rqjobid 'dummystringfortesting'


## Misc Notes and Warnings


- Only jobtype and queuename are validated. `jobargs` is not validated, since the args are job specific.
