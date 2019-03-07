# Protocol programming - assignment 04 - Hannu Oksman L2912

# HannuProtocol

## Description

This is a design document for a simple file transfer protocol, which has two requests (LIST, DOWNLOAD) and two responses (ERROR, FILE). It uses sockets to connect differents hosts. The sockets use TCP and IPv4 protocols to transfer data. The protocol stateless. 
That is, request-response pairs are independent of other pairs. They don't affect each other. The protocol is doesn't have authentication ie. responses don't require username and password from the request. Default port is 8888.

The requests use headers for determining server socket's address and port. Headers are also optionally used for disconnecting the sockets. When a request or a response has a body (payload), a header is used to inform the recipient socket of the size of the body.
The payload data is just plain text. It's not in, for example, JSON-format. Different lines in the data (\r\n) are used to separate information. For example, each item of a list has it's own row.
The server closes connection when the request has the disconnect header, the payload is fulle received or an error occurred.

The protocol is text based ie. the requests and responses are handled as strings instead of bytes. String "\r\n" is used to separate different sections in the requests and responses. The user uses single spaces in the requests to separate different elements.
It enables using sockets as files, which useful because file methods can be used to read and write the requests and responses. The user uses an command line interface (CLI) to use this protocol (she uses keyboard).

## Requests

Request format: method sp address sp port sp option \r\n
Exampe: DOWNLOAD localhost 8888 cat.jpg

Syntax:
* Method (mandatory): name of the method ie. LIST
* Address (mandatory): address of the server socket ie. localhost or 192.0.0.127
* Port (mandatory): port of the address socket ie. 8888
* Option (optional): optional parameter such as a file name ie. cat.jpg
* sp means single space ie. pressing the spacebar button once
* \r\n means carriage return and new line ie. pressing the enter button

### LIST address port

Requests a list of files which are available for downloading from the server. Returns FILE response and the list is in the response's body.

#### Additional information

Client socket cannot specify which folder is used on the server. It's fixed for security reasons (makes it easier to restrict which files the client has access to). The server closes the connection when the list is sent. The client prints the list to the CLI.

#### Example request

LIST localhost 8888

#### Example response

FILE OK
cat.jpg
dog.png
snake.mp3
mouse.flv
pig.txt

### DOWNLOAD address port file-name 

Downloads a file from the server to the client's host. If succesful, the client has the file and the CLI notifies the user. The server closes the connection when the file is uploaded. The client closes the connection if an error occurred.

#### Example request

DOWNLOAD localhost 8888 cat.jpg

#### Example response

FILE OK

## Responses

Response format: method sp body \r\n
Example: FILE file
Example: ERROR errorMessage

Syntax:
* Method (mandatory): name of the method ie. FILE
* Body (mandatory): method's body/payload ie. cat.jpg or error message ie. "File not found"
* sp means single space ie. pressing the spacebar button once
* \r\n means carriage return and new line ie. pressing the enter button

### FILE file

Returns requested file or data from the server. The file/data is in the response's body (payload). If the data is in binary format, it will be converted to base64 string. If succesful, message "FILE OK" will be printed to the CLI.

#### Example request

DOWNLOAD localhost 8888 cat.jpg

#### Example response

FILE OK

### ERROR errorMessage

Returns error message when an error occurres. The cause of error can, for example, be a invalid request ie. unknown method.

#### Example request

UPLOAD localhost 8888

#### Example response

ERROR unknownMethod

#### Error messages

