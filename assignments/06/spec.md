# Assignment 06 : TODO Protocol

This specification is based on [assignment 04's spec](https://github.com/Szeretni/ttks0500-protocol-programming/blob/master/assignments/04/assignment04.md).
A server maintains a file with todo items, such as "buy vegetables", in it's file system. 
A client can make requests (add, list, done) to the server in order to manipulate the todo file.
The server is multithreaded and can handle concurrently multiple clients.
The todo file is locked when one thread is accessing it and unlocked when it's done.
It is important in order to avoid dirty reads and lost update, for example.

This protocol is implemented with Python 2.7 socket- and threading libraries.
The sockets use TCP/IPv4 protocols for communication.
The protocol is stateless and doesn't have authentication.
A default port isn't forced (my examples use 8888 port).

Messages (requests and responses) are in plain text.
A client makes requests and a server responds to them with responses.
The server cannot initiate communication with the clients.
The message structure is very simple and it doesn't have a body. For example:

```
METHOD sp BODYLENGHT sp METHOD-SPECIFIC-PARAMETER\r\n
[BODY]
```

Items:
* METHOD: LIST, ADD, DONE, OK, ERROR
* sp: single space, that is, pressing the spacebar once
* BODYLENGHT: bytes in the body/payload
* METHOD-SPECIFIC-PARAMETER: a message which an user wants to store to the todo list. Or additional information for a response
  * if parameter is not needed, that must be denoted with '.'
* \r\n: carriage return and new line, that is, pressing the enter once.
* BODY: additional data such as items of the todo list

An user makes requests with a command line interface by running a client file with an ip address, a port, a method name and a possible parameter. For example:

```
python client.py localhost 8888 "ADD 0 Buy vegetables"
```

## Requests

An user makes requests to a server which sends responses back to the user. The server responses with OK or ERROR messages.
The responses may contain additional information such as the todo file's content or an error code.

### LIST

The user requests a todo file's contents from the server.

#### Example request
```
LIST 0 .
```

#### Example response
```
OK
1) Buy milk
2) Pay rent
3) Feed the dog
```

### ADD

The user requests the server to add an item to the todo file.

#### Example request
```
ADD 0 Buy vegetables
```

#### Example response
```
OK
```

### DONE

When the user has done a particular task in the todo list, she requests the server to remove a particular todo item from the list. A tasks number is the parameter of the request.

#### Example request
```
DONE 0 1
```

#### Example response
```
OK
```

## Responses

The server responds to the users requests with response messages.

### OK 0

This response is sent to the client when to request was processed without complications. May have a parameter (when responding to LIST requests, the parameter has the todo items).

### ERROR 0

This response is sent to the client when to request couldn't be processed. For example, DONE response's parameter couldn't be found.
