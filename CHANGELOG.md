# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## [[Embed.xyz](https://embed.xyz) Assessment] - October 13, 2022

Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.

### Added

- [Initial API & Project Structure](https://github.com/kevencript/embed-backend-devops/commit/5bc6bb790bf645f63f62173fa7534b10e047656a)
  Initial project structure (FastAPI & Mongo deployment with Docker-compose and basic requirements)
- [ELK Application Logging #1](https://github.com/kevencript/embed-backend-devops/commit/4bfbbb5b8ea410b221f8f8f9d07d6982ebb61a26)
  Here we deploy/config the [ELK Stack](https://www.elastic.co/pt/elastic-stack/) in order to store, search, analyze, and visualize data from our Python FastAPI application.
  Beside of the ELK stack, we created the logs injection from our app with python-logstash (since that the API already have the logging structure, basically we added the logstash handler in order to inject the data into the Elasticsearch), making the logs available into Kibana.
- [JWT Authentication Method #2](https://github.com/kevencript/embed-backend-devops/CHANGE-ME)
  Initial project structure (FastAPI & Mongo deployment with Docker-compose and basic requirements)

### Changed

### Fixed
