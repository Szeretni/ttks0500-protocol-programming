# Protocol Programming - Assignment 04 - Hannu Oksman L2912

# HannuProtocol

## Description

This is a design document for a simple file transfer protocol, which has two requests (LIST, DOWNLOAD) and two responses (ERROR, FILE). It uses sockets to connect differents hosts.
The sockets use TCP and IPv4 protocols to transfer data. The protocol stateless.
That is, request-response pairs are independent of other pairs, they don't affect each other.
The protocol doesn't have authentication ie. responses don't require username and password from the request. Default port is 8888.

The payload data is just plain text. It's not in, for example, in JSON-format. New lines (\"n") in the data are used to separate information. For example, each item of a list has it's own row. 
It enables using sockets as files, which is useful because file methods can be used to read and write the requests and responses.
In case of binary files ie. pictures, the data is converted to a base64 format.
The server closes the connection when the payload is fully received or an error occurred.

The protocol is text based ie. requests and responses are handled as strings instead of binaries. String "\r\n" is used to denote the end of the request/response.
Single spaces are used to separate different elements/arguments in the requests/responses.
Examples below assume that an user uses a command line interface (CLI) to use this protocol.

## Requests

Request format: method sp address sp port sp option \r\n

Example: DOWNLOAD localhost 8888 cat.jpg

Example: LIST 192.0.0.127 8888 .

Syntax:
* Method (mandatory): name of the method ie. LIST
* Address (mandatory): address of the server socket ie. localhost
* Port (mandatory): port of the server socket ie. 8888
* Option (mandatory): optional parameter such as a file name ie. cat.jpg. If not needed, use "." for this argument
* sp means single space ie. pressing the space bar button once
* \r\n means carriage return and new line ie. pressing the enter button

### LIST address port .

Requests a list of files which are available for downloading from the server. Returns a FILE response and the list is in the response's body. The option element is not needed in this request, so the fourth argument is ".".

#### Additional information

Client socket cannot specify which folder is used on a server. It's fixed for security reasons (makes it easier to restrict which files the client has access to).
The server closes the connection when the list is sent. The client prints a list of available files to a CLI.

#### Example request

LIST localhost 8888 .

#### Example response

FILE body

Body has data with names of available files on server. The body is a string and items (file names) are delimited with "\n". A "FILE OK" message and the file names are printed to a client's CLI.

##### Print to the client's CLI

FILE OK<br/>
cat.jpg<br/>
dog.png<br/>
snake.mp3<br/>
mouse.flv<br/>
pig.txt

### DOWNLOAD address port file-name

Downloads a file from a server to client's host. If successful, the file is written to the client's storage system. The server closes the connection when the file is uploaded.
The client closes the connection if an error occurred.

#### Example request

DOWNLOAD localhost 8888 cat.jpg

#### Example response

FILE body

Body has data with a name and a content of a file. The name and the content are delimited with "\n" ie. "cat.jpg\nbase64data". If the file is a binary file, then the data is in base64 format. 
A "FILE OK" message is printed to the client's CLI.

##### Print to the client's CLI

FILE OK

## Responses

Response format: method sp body \r\n

Example: FILE file

Example: ERROR errorCode

Syntax:
* Method (mandatory): name of a method ie. FILE
* Body (mandatory): method's body/payload ie. "cat.jpg\nbase64data" or error code ie. "101" (Status code for "file not found")
* sp means single space ie. pressing the space bar button once
* \r\n means carriage return and new line ie. pressing the enter button

### FILE file

Returns requested file or data from a server. Response's body (payload) has the data (the file). If the data is in binary format, it will be converted to a base64 string.
If successful, a message "FILE OK" will be printed to client's CLI and the file is written to the client's storage system.

#### Example request

DOWNLOAD localhost 8888 cat.jpg

#### Example response

FILE file

FILE method's body (data, file) consists of a file name (and an possible extension) and file data delimited by "\n". For example, "filename.ext\nfiledata".

##### Print to the client's CLI

FILE OK

### ERROR errorCode

Returns an error code when an error occurred. A cause of the error can be, for example, an invalid request ie. unknown method.

#### Example request 1

UPLOAD localhost 8888

Please note that the UPLOAD method is not supported.

#### Example response 1

ERROR 102

##### Print to the client's CLI

ERROR Unknown Method

#### Example request 2

DOWNLOAD localhost 8888 cat

Please note that a file named "cat" is not available at a server (cat.jpg is).

#### Example response 2

ERROR 101

##### Print to the client's CLI

ERROR File Not Found

### Error codes and descriptions

Error's status code is returned, not description. Client's CLI prints an verbose error message depending on the error's status code.

Error messages below are in the following format: statuscode sp statusname

#### 101 fileNotFound

Server does not have the requested file. For example, the server has cat.jpg, but client requested dog.jpg.

#### 102 unknownMethod

The requested method is unknown. See known methods above (LIST, DOWNLOAD).

#### 103 malformedRequest

The request is malformed. For example, "DOWNLOADfile" is malformed, a single space is required.

## Client side errors

Some errors can occur without a ERROR response. For example, if a client cannot connect to a server, the server cannot response. An error is printed to the client's CLI.

### Error messages

#### 201 hostNotFound

A client cannot connect to a server. Requests address and/or port is wrong or the server is down.

#### 202 outOfSpace

Response is received, but it's body is too large and it cannot be written to the client's storage system.

#### 203 malformedResponse

Response is received, but it is malformed. For example, the server crashes and the response is not complete (for example, \r\n is missing).

#### 204 connectionTimedOut

A server is up and running, but the client is suffering problems with her Internet connection and drops the connection to the server.
