# event-sourcing-example
This is a demonstration of Event Sourcing and CQRS.

## Getting started

### Preparations
1. Clone this repository
1. Install [Python 2.7](https://www.python.org/download/releases/2.7/)
1. Install [PyMongo](https://api.mongodb.com/python/current/installation.html)
1. Install [MongoDB](https://www.mongodb.com/download-center#community)
1. Run [mongod](https://docs.mongodb.com/manual/reference/program/mongod/) locally

### Running the tests
1. Run the following command in the repo's folder:

        python -m unittest discover -v -p *_tests.py

## Background

### What is Event Sourcing?
Event Sourcing is an architecture style where application state is derived by historical events. An Event Store keeps the record of all events, and is used as a source of truth from which current state is derived.

The business benefits are that data doesn't get lost, and can always be interpreted and analyzed in new ways.

The technical benefits are that the source of truth is append-only and consists of immutable objects, that can be safely shared and cached. It also allows to restore all past states. 

### What is CQRS?
Command and Query Responsibility Segragation is an architecture style where the commands (e.g. update / set / write) and queries (e.g. get / read) are handled by different components and different APIs.

The benefits are that it allows queries and commands to scale independently, and to be optimized for different availability and performance requirements.

CQRS is often used with Event Sourcing, because the event store keeps data in a way that is not optimized for queries, and a separate projection mechanism is required for converting event data into a reporting structure.

## What's in this repository?

**mongodb_event_store.py** implements an event store based on MongoDB.

**bank.py** implements an API for banking, which works with an event store behind the scenes. It also implements concurrency controls for making sure that withdrawals or transfers between accounts are rejected in case there isn't enough money in the account.

**messages_cmd_handler.py** and **messages_query_handler.py** implement segregated APIs for handling commands and queries of a messaging system.
