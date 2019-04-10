# Requests

## LIST

Lists a content of a todo file. That is, it's todo items.

### Valid request

```python client.py localhost 8888 "LIST 0 ."```

Lists the content of the server's todo file.

The LIST includes body length 0 and it's parameter is ".". It does not have a body.

The LISTRESPONSE includes body length, number of items in the body and the body.

### Response
```
A message sent succesfully.
Waiting for a message.
Received the message succesfully.
LISTRESPONSE 116 7
1) eat veggies1
2) eat veggies2
3) eat veggies3
4) eat veggies4
5) eat veggies5
6) eat veggies6
7) eat veggies7
```

### A positive non-zero body length

```python client.py localhost 8888 "LIST 1 ."```

The server terminates the connection and sends an error code 1.

The ERROR includes body length 0 and the error code. It does not have a body.

### Response
```
A message sent succesfully.
Waiting for a message.
Received the message succesfully.
ERROR 0 1
```

### A negative non-zero body length

```python client.py localhost 8888 "LIST -1 ."```

The client does not form a connection to the server. Prints a following message:

```Invalid body length.```

## ADD

Adds a new item to the todo list.

Parameter is the item such as "eat veggies8".
The server sends OK 1 response if the item was added to the file.

### Valid request

```python client.py localhost 8888 "ADD 0 eat veggies8"```

### Response
```
A message sent succesfully.
Waiting for a message.
Received the message succesfully.
OK 0 1
```

## DONE

Removes a done task from the todo file.

Parameter is the number of the todo item to be removed.
For example, "DONE 0 8" removes the eight item from the todo file.
The server sends OK 1 response if the item was added to the file.

### Valid request

```python client.py localhost 8888 "DONE 0 8"```

### Response
```
A message sent succesfully.
Waiting for a message.
Received the message succesfully.
OK 0 2
```
