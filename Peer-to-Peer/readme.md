# Peer-to-peer

### Dependencies:
Install GuiZero via pip:
```
pip install guizero
```
### Download
You can clone the repository or download zipped repository directly from the repository.

### Usage
```
py nodo.py server_port ip_client client_port
```
## Function description
```python
def stampa_messagggi():
```
This function inserts into listbox of the graphic interface the list of the received messages. Messages are extracted from the queue "messaggi".

```python
class serverThread (threading.Thread):
```
This is the class of the server thread. A server socket is opened in the run method of the class, when the server object is instantiated. The server will accept connection from the client and put received message in the queue "messaggi". In case of errors, the thread is closed

```python
def socket_client():
```
This function opens a socket client and then returns it. If there are any errors, it will return -1.

```python
def invia_dati():
```
This function will send message to the server of the other node. It automatically takes body of message from the graphic interface.
