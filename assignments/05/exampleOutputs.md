# LIST

## Requests

### python client.py localhost 1234 "LIST 0 ."

Lists files and folders of a default location.

THE LIST includes body length 0 and a parameter to a possible folder. It does not have a body.

The LISTRESPONSE includes body length, number of items in the body and the body. The final item does not have "\r\n" suffix.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
LISTRESPONSE 73 4
folder1
LibreOffice_6.1.5_Linux_x86-64_deb.tar.gz
nicepic.png
text.txt
hannu@hannu-VirtualBox:~/git/

### python client.py localhost 1234 "LIST 0 folder1"

Lists files and folders of a subfolder.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
LISTRESPONSE 26 2
folder2
fileInFolder1.txt

### python client.py localhost 1234 "LIST 1 ."

A positive non-zero body length. The server terminates the connection and sends a general error 4.

The ERROR includes body length 0 and the error code. It does not have a body.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
ERROR 0 4

### python client.py localhost 1234 "LIST -1 ."

A negative non-zero body length. The client does not form a connection.

Invalid body length.

### python client.py localhost 1234 "LIST 0 fold"

A folder is not found. Error 1.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
ERROR 0 1

### python client.py localhost 1234 "LIST 0 nicepic.png"

The client tried to list a file. Error 1.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
ERROR 0 1

# DOWNLOAD

### python client.py localhost 1234 "DOWNLOAD 0 folder1"

The client tried to download a folder. Error 2.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
ERROR 0 2

### python client.py localhost 1234 "DOWNLOAD 0 asdf"

The client tried to download a non-existing file. Error 3.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
ERROR 0 3

### python client.py localhost 1234 "DOWNLOAD 0 LibreOffice_6.1.5_Linux_x86-64_deb.tar.gz"

A succesful download. The DFTP behaves well with large files. The file in the example response is 228,2 MB.

The DOWNLOAD includes a body length 0, a name of the file. It does not have the body.

The FILE includes a body length, name of the file and the body. The body is not printed to the console because printing large binary objects is not sensible.

### Response

A message sent succesfully.
Waiting for a message.
Received the message succesfully.
FILE 228152670 LibreOffice_6.1.5_Linux_x86-64_deb.tar.gz
LibreOffice_6.1.5_Linux_x86-64_deb.tar.gz downloaded.
