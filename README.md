## [[Embed.xyz](https://embed.xyz) Assessment] - October 13, 2022 ~ Octocer 20, 2022
This project is a pratical test for Embed.xyz. That's basically a Web app with any Python lib (we are currently using [FastAPI](https://fastapi.tiangolo.com)) in which i had some days to develop some modules into it and create a automatic way for build (docker-compose), log (ELK) and monitor (Prometheus, Kibana and Nodex-exporter) the app. All of this in a organized and able to grow API strcuture. with security and data contol.

Since that is a 50% Backend and 50% DevOps test, i applied my energy not only to have a nice and organized API, but have controll/visibility regarding what is happening on both App Logging and Infra Metrics. All of this is beeing deployed with a docker-compose, this means that we have almost zero effort to start the whole App and its auxililiar tools. Of course there is a bunch of improvement proposals, but due the short deadline, we can consider this project as a MVP with structure ready to receive new modules.

## Project Folder Structure
```
── CHANGELOG.md # Where you can see the project steps (module by module)
├── Dockerfile 
├── Makefile # File to config the app start 
├── Pipfile
├── Pipfile.lock
├── README.md
├── docker-compose.yml
├── elk # Config folder for Logging [ELK](https://logz.io/learn/complete-guide-elk-stack/) Stack 
│   ├── elasticsearch
│   │   └── ...  
│   ├── kibana
│   │   └── ...
│   ├── logstash
│   │   └── ...
│   └── setup
│   │   └── ...
│
├── embed # Here is where the API file are
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── oauth2.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── posts.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── posts.py
│   │   └── users.py
│   ├── serializers
│   │   ├── postsSerializers.py
│   │   └── userSerializers.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── postsRepository.py
│   │   └── repository.py
│   └── utils.py
│
├── monitoring # Monitoring deploy (Prometheus, Node-exporter and Grafana)
│   ├── grafana
│   │   └── prometheus_ds.yml
│   └── prometheus
│       └── prometheus.yml
│
├── pytest.ini
├── requirements.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    └── test_routers.py
```


## CHANGELOG.md
To keep track of the steps in which we did and its event order, the project is base on [Keep a Changelog](http://keepachangelog.com/) to log the project changes in a effective way (CHANGELOG.md is on the root dir). As improovement proposal, this project should adheres to [Semantic Versioning](http://semver.org/).

## Installation
1. Create `.env` file in the project directory. 
Obs: You have the **`.env.example`** file on project root
```
...
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
ENVIRONMENT=local
...
```
  2. Start the Environment 
```
make up 
```
or (if you don't have [Makefile](https://blogs.iu.edu/ncgas/2019/03/11/installing-software-makefiles-and-the-make-command/))
```
docker-compose up --build 
```
> It takes some minuts to totally deploy the tools (Kibana, Elastic...). If you try to access one the tools and receive an error, try to wait some more minuts and try again

  
  ## Web API Usage 
1. Go to localhost:8989/docs
2. Play with the routes:

![](https://i.ibb.co/RQH4xzr/Captura-de-Tela-2022-10-20-s-12-17-02.png)
> We use Bearer Token for auth. We highly indicate to use Postman to test the routes.


  ## Logging Tools Usage (API Logging > Logstash > ElasticSearch > Kibana)
1. Go to localhost:5601 (Kibana Service)
2. LogIn (`Default User: elastic` and `Default Pass: changeme`)
3. Go to Discover and search for `logs-*` 

![](https://i.ibb.co/7kyGy7N/Captura-de-Tela-2022-10-20-a-s-12-37-36.png)
> You can create your own queries

  ## Infra Monitoring Tools Usage (Env Metrics > Node-exporter > Prometheus > Grafana)
1. Go to localhost:3000
2. LogIn (`Default User: admin` and `Default Pass: admin`)
3. Go to Import Dashboard 
4. Import the Dashboard `1860` (CPU, Memory and other metrics) - [See more about the Dashboard](https://grafana.com/grafana/dashboards/1860-node-exporter-full/)
5. Select `Prometheus` as Datasource (Prometheus DS is. automatically added)

![](https://i.ibb.co/dr5ZQh3/Captura-de-Tela-2022-10-20-s-12-47-32.png)
> Here you have the graphics for our metrics

  ## Conclusion
 The original Embed.xyz assessment requires some other API modules: Subscriptions and spicific Posts searches. In my mind, since that this is a 50% Software and 50% DevOps, i decided to apply time also to develop API routes and modules, but creating the necessary structure to receive any other new module in a organized way. For now, we have authentication module and a nice example with Posts (create posts, search for Stringmatch posts by title). This means that any other route will follow the pattern of what we already have into the API. By the other hand, we are not only allowd to create new modules but we have a structure to visualze our App logs (Errors, Action Tracking and more) and have control regarding our Infrastructure (CPU, Memory and more). All of this running just a command to start the whole environment.
