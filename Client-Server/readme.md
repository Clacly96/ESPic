# Server
## Installation:
### Dependencies:
Install mysql server from the official site and then the mysql-connector via pip:
```
pip install mysql-connector
```
### Download
You can clone the repository or download zipped repository directly from the repository.

### Usage
```
py server.py port_num backlog_num expire_time
```
### Close
Close the server with Ctrl+C and then type s.

## Function description

```python
def connessioneDb()
```
This function will take parameters from DBsetting and open a connection with MySql.
It returns a db object.

```python
def controlloUtente(username)
```
#### Parameters:
    username (string) 

This funcion will check if the provided username is in the DB.
It returns True if username exists, False otherwise.

```python
def controlloPassword(username,password)
```
#### Parameters:
    username (string)
    password (string)

This function will check if user exists and password is valid.
It returns True or False.

```python
def inserisciUtente(username,password)
```
#### Parameters:
    username (string)
    password (string)

This function inserts in the DB the provided user.

```python
def estraiUtenti()
```
This function extracts all user from the DB.
It returns a list of tuple.

```python
class requestHandlerThread (threading.Thread):
```
This class extends threading.Thread and it is used to handle concurrent requests in multiple threads.

#### Parameters:
    socket (socket object) - It's the created socket server
    connessione (socket object) - It's the connected client
    indirizzo_client (string) - Address of the client

#### Type of request:
    Syntax: <action><parameter>{<parameter>}
#####   Actions:
        -GET: for receive incoming messages from the server. 
            E.g. ["GET","Mario"] will send all incoming messages to Mario's client
        -POST: for send messages to other people and save them on DB.
            E.g. ["POST","Hi!","Mario","Luigi"] will put the message "Hi!" from Mario to Luigi in the DB.
        -SERVICE: used for service's request:
            -regUser: register a new user on the DB
            -checkPwd: will check if login crediantials are correct
            -estraiUtenti: extracts all user from DB and send them to client

```python
def launch(porta,backlog):
``` 
#### Parameters:
    porta (int): the port on which the server will listen for request
    backlog (int): maximum number of pending requests

This function will start a socket server on the specified port.
It return a socket object or -1 in case of errors

```python
def run_server(server,inizio,durata=0)
``` 
#### Parameters:
    server (socket object)
    inizio (float): the inizial time
    durata (int): maximum seconds of life of the server (0 is used for unlimited life)

This function will accept requests and start a new thread to handle the request.


# Client
### Dependencies:
Install GuiZero via pip:
```
pip install guizero
```
### Download
You can clone the repository or download zipped repository directly from the repository.

### Usage
```
py client.py ip_server server_port
```
## Function description
```python
def mostra_login():
``` 
```python
def mostra_registrazione():
```
These function only show login or registration window

```python
def login():
```
This function will check with the server if provided credential are correct. It takes parameters directly from graphic interface.

```python
def registrazione():
```
This function checks if the username already exixsts and register it if not exists. It will show an error message if user already exists.

```python
def socket_client():
```
This function opens a socket client and then returns it. If there are any errors, it will return -1.

```python
def richiedi_messaggi():
```
This function will request to the server incoming messages for the logged user. It will print messages on graphic interface.

```python
def invia_dati():
```
This function will send message to the server. It automatically takes body of message and receiver from the graphic interface.

```python
def richiedi_utenti():
```
This function will request user's list and then print it in the graphic interface.