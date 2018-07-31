import socket,queue,sys
import threading
from guizero import App, TextBox, PushButton, Text, ListBox, info

messaggi=queue.Queue()
def stampa_messagggi():
    try:
        lista_messaggi.append(messaggi.get_nowait())
    except:
        pass

def apri_messaggio(selezionato):
    info("Messaggio",str(selezionato))

class serverThread (threading.Thread):
    def __init__(self, indirizzo):
      threading.Thread.__init__(self)
      self.indirizzo = indirizzo

    def run(self):
            thread_server = threading.currentThread()
            try:
                s=socket.socket()
                s.bind(self.indirizzo)
                s.listen(1)
                s.setblocking(0)
                print("[Server]Server inizializzato correttamente")
            except BlockingIOError:
                pass
            except socket.error as errore:
                print(f"[Server]Ci sono stati problemi: {errore}")
            while getattr(thread_server, "restaAttivo", True):
                try:    
                    socket_client, indirizzo_client=s.accept()
                    print(indirizzo_client)
                    socket_client.setblocking(1)
                    richiesta=socket_client.recv(1024)
                    #print(f"[Server]La richiesta è: {richiesta.decode()}")
                    messaggi.put(richiesta.decode())
                    socket_client.send("[Server]Messaggio ricevuto".encode())
                except BlockingIOError:
                    pass
            s.close()

def socket_client(indirizzo):
    try:
        c = socket.socket()
        c.connect(indirizzo)
        print("[Client]Connessione stabilita")
    except OSError:
        print("[Client]Il server scelto non è disponibile")
        avvisi.value="L'altro client non è connesso"
        return -1
    except socket.error:
        print(f"[Client]Si è verificato un errore: {socket.error}")
        return -1
    return c

def invia_dati():
    if textbox.value!="":
        c=socket_client(("localhost",porta_client))    
        if c!=-1:
            print(f"&{textbox.value}&")        
            c.send(textbox.value.encode())
            risposta= c.recv(1024)
            print(str(risposta.decode()))
            if risposta.decode()=="[Server]Messaggio ricevuto":
                avvisi.value="Messaggio inviato e ricevuto correttamente"
            c.close()
            textbox.clear()            
        elif c==-1:
            avvisi.value="Errore di connessione, l'altro client potrebbe non essere connesso"
    else:
        avvisi.value="Non inviare messaggi vuoti"
    
if __name__ == "__main__":
    
    porta_server=int(sys.argv[1])
    porta_client=int(sys.argv[2])
    interfaccia= App(layout="grid")
    messaggi_ricevuti = Text(interfaccia, text="Messaggi ricevuti",align="left",grid=[0,0])
    lista_messaggi=ListBox(interfaccia,scrollbar=True,align="left",command=apri_messaggio,grid=[0,2,6,1])
    lista_messaggi.repeat(500,stampa_messagggi)
    text = Text(interfaccia, text="Inserisci il testo del messaggio",align="left",grid=[0,6])
    textbox = TextBox(interfaccia,grid=[0,7,4,1])
    textbox.width=30
    tastoInvio = PushButton(interfaccia, text="Invia",align="left", command=invia_dati,grid=[5,7])
    Labelavvisi=Text(interfaccia, text="Avvisi:",align="left",grid=[0,8])
    avvisi=Text(interfaccia,size=9,align="left",grid=[0,9])
    thread_server=serverThread(("localhost",porta_server))
    thread_server.start()
    
    interfaccia.display()
    thread_server.restaAttivo = False
    thread_server.join()

    