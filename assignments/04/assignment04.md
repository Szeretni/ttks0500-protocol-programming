# Protocol Programming - Assignment 04 - Hannu Oksman L2912

# HannuProtocol

## Description

This is a design document for a simple file transfer protocol, which has two requests (LIST, DOWNLOAD) and two responses (ERROR, FILE). It uses sockets to connect differents hosts.
The sockets use TCP and IPv4 protocols to transfer data. The protocol stateless.
That is, request-response pairs are independent of other pairs. They don't affect each other.
The protocol is doesn't have authentication ie. responses don't require username and password from the request. Default port is 8888.

The requests use headers for determining server socket's address and port. Headers are also optionally used for disconnecting the sockets.
When a request or a response has a body (payload), a header is used to inform the recipient socket of the size of the body.
The payload data is just plain text. It's not in, for example, JSON-format. Different lines in the data (\r\n) are used to separate information. For example, each item of a list has it's own row.
The server closes connection when the request has the disconnect header, the payload is fully received or an error occurred.

The protocol is text based ie. the requests and responses are handled as strings instead of bytes. String "\r\n" is used to separate different sections in the requests and responses.
The user uses single spaces in the requests to separate different elements.
It enables using sockets as files, which useful because file methods can be used to read and write the requests and responses.
The user uses an command line interface (CLI) to use this protocol (she uses keyboard).

## Requests

Request format: method sp address sp port sp  \r\n

Example: DOWNLOAD localhost 8888 cat.jpg

Syntax:
* Method (mandatory): name of the method ie. LIST
* Address (mandatory): address of the server socket ie. localhost or 192.0.0.127
* Port (mandatory): port of the address socket ie. 8888
* Option (mandatory): optional parameter such as a file name ie. cat.jpg. If not needed, use "." for this element.
* sp means single space ie. pressing the space bar button once
* \r\n means carriage return and new line ie. pressing the enter button

### LIST address port .

Requests a list of files which are available for downloading from the server. Returns FILE response and the list is in the response's body.

#### Additional information

Client socket cannot specify which folder is used on the server. It's fixed for security reasons (makes it easier to restrict which files the client has access to).
The server closes the connection when the list is sent. The client prints the list to the CLI.

#### Example request

LIST localhost 8888 .

#### Example response

FILE body

The body has data with names of the available files in the server. The body is a string and the items are delimited with "\n". A "FILE OK" message and the file names are printed to the client's CLI.

##### Print to the client's CLI

FILE OK<br/>
cat.jpg<br/>
dog.png<br/>
snake.mp3<br/>
mouse.flv<br/>
pig.txt

### DOWNLOAD address port file-name

Downloads a file from the server to the client's host. If successful, the client has the file and the CLI notifies the user. The server closes the connection when the file is uploaded.
The client closes the connection if an error occurred.

#### Example request

DOWNLOAD localhost 8888 cat.jpg

#### Example response

FILE body

The body has data with the name and the content of the file. The name and the content is delimited with "\n". If the file is a binary file, then the data is in base64 format. A "FILE OK" message if printed to the client's CLI:

##### Print to the client's CLI

FILE OK

## Responses

Response format: method sp body \r\n

Example: FILE file

Example: ERROR errorMessage

Syntax:
* Method (mandatory): name of the method ie. FILE
* Body (mandatory): method's body/payload ie. "cat.jpg\ndataInBase64" or error message ie. "File not found"
* sp means single space ie. pressing the space bar button once
* \r\n means carriage return and new line ie. pressing the enter button

### FILE file

Returns requested file or data from the server. The file/data is in the response's body (payload). If the data is in binary format, it will be converted to base64 string.
If successful, message "FILE OK" will be printed to the CLI and the file is written to the client's storage system.

#### Example request

DOWNLOAD localhost 8888 cat.jpg

#### Example response

FILE file

FILE method's body data (file) consists of a file name (and possible extension) and file data delimited by "\n". For example, "filename.ext\nfiledata".

##### Print to the client's CLI

FILE OK

### ERROR errorMessage

Returns error code when an error occurred. The cause of error can, for example, be a invalid request ie. unknown method.

#### Example request 1

UPLOAD localhost 8888

Please note that the UPLOAD method is not supported.

#### Example response 1

ERROR 102

##### Print to the client's CLI

ERROR Unknown Method

#### Example request 2

DOWNLOAD localhost 8888 cat

Please note that a file named "cat" is not available at the server. cat.jpg is available.

#### Example response 2

ERROR 101

##### Print to the client's CLI

ERROR File Not Found

#### Error messages

Error's status code is returned, not description. The client prints a verbose message depending on the status code.

Error messages below are in the following format: statuscode sp statusname

##### 101 fileNotFound

The server does not have the requested file. For example, the server has cat.jpg, but the client requests dog.jpg.

##### 102 unknownMethod

The requested method is unknown. See known methods above (LIST etc.).

##### 103 malformedRequest

The request is malformed. For example, DOWNLOADfile is malformed, single space is required.

## The client side errors

Some errors can occur without ERROR response. For example, if the client cannot connect to the server, the server cannot response. The error is printed to the CLI.

### Error messages

#### 201 hostNotFound

The client cannot connect to the server. The address and/or the port is wrong or the server is down.

#### 202 outOfSpace

Response is received, but the body is too large and it cannot be written to the client's storage system.

#### 203 malformedResponse

Response is received, but it is malformed. For example, the server crashes and the response is not complete (for example, \r\n is missing).

#### 204 connectionTimedOut

The server is up and running, but the client is suffering problems with her Internet connection and drops the connection to the server.
