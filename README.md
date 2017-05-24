# event-sourcing-example
This is a demonstration of Event Sourcing and CQRS.

## Getting started

### Preparations
1. Clone this repository
1. Install [Python 2.7](https://www.python.org/download/releases/2.7/)
1. Install [PyMongo](https://api.mongodb.com/python/current/installation.html)
1. Install [MongoDB](https://www.mongodb.com/download-center#community)
1. Run [mongod](https://docs.mongodb.com/manual/reference/program/mongod/) locally
1. Optional: Install [robomongo](https://robomongo.org/download)

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

**msg_cmd_handler.py** and **msg_query_handler.py** implement segregated APIs for handling commands and queries of a messaging system.

## How to play around?

For the banking demonstration, type

    python -i bank_script.py

This will run a few commands, and then you can type more commands in the python console, using the variable 'B' as the bank object, with commands such as:

    B.create_account("account_name")
    B.deposit("account_name",100)
    B.withdraw("account_name",50)

You can use Robomongo to examine the database named "bank".

---------

For the CQRS messaging demo, type

    python -i msg_script.py

and in another window, run the projector

    python msg_projector_runner.py

Then, hit "Enter" a couple of times in the first window, and use the variables CMD_HANDLER and QUERY_HANDLER in the python console, to run some more actions such as

    CMD_HANDLER.send_msg_to_user("user_id","msg_id")
    CMD_HANDLER.mark_msg_as_read("user_id","msg_id")
    QUERY_HANDLER.get_num_unread("user_id")

You can kill and restart the msg_projector, to see the effects of eventual consistency (i.e. queries will not reflect the most up-to-date state as follows by the commmands, but a little while after the projector is executed again, they catch up).

Also, use Robomongo to examine the databases beginning with "msg", for an inside look.
