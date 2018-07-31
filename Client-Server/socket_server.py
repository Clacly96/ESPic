import socket
import sys
import time
from threading import Thread
import threading

import psycopg2


i=0 # per testing
num_client=0
spegni=False

class requestHanlerThread (Thread):
    def __init__(self, socket, connessione,indirizzo_client, log_file):
      Thread.__init__(self)
      self.conn = connessione
      self.ind_client=indirizzo_client
      self.lock=threading.Lock()
      self.log=log_file
      self.socket=socket
      self.lock_spegnimento=threading.Lock()

    def run(self):
        global i
        global spegni
        global num_client
        if spegni==False:
            self.lock.acquire()
            num_client+=num_client
            self.lock.release()
            self.conn.setblocking(True) # imposta la connessione corrente come bloccante
            self.conn.settimeout(200) # setta il timeout per la connessione corrente, in secondi
            print(f"Connessione Server - Client Stabilita: {self.ind_client}\n")
            richiesta=self.conn.recv(4096)
            print(richiesta.decode())
            testo_richiesta=richiesta.decode().split("&$%")
            if(testo_richiesta[0].upper()=="GET"):
                self.lock.acquire()
                #qui va la scrittura del file di log
                num_client+=1                
                destinatario=testo_richiesta[1]

                conn=psycopg2.connect(database="pymsg",user="calcolatori",password="calcolatori")
                cur = conn.cursor()
                cur.execute("select id,testo,mittente,data from messaggi where letto=false and destinatario=%s",(destinatario,))

                selezione=cur.fetchall()
                messaggio=""
                messaggi_letti=[]
                if selezione:
                    for riga in selezione:
                        ID,testo,mittente,data=riga
                        messaggio+=str(testo)+"&$%"+str(mittente)+"&$%"+str(data)+"/&/"
                        messaggi_letti.append(ID)
                    cur.execute("update messaggi set letto=true where id in %s",(tuple(messaggi_letti),))  
                i+=1
                
                conn.commit()
                cur.close()
                conn.close()

                self.lock.release()
            elif(testo_richiesta[0].upper()=="POST" and len(testo_richiesta)>1):
                #esempio post: POST&$%testo del messaggio&$%nome_destinatario&$%nome_mittente
                self.lock.acquire()
                #qui va la scrittura del file di log
                testo_messaggio=testo_richiesta[1]
                destinatario=testo_richiesta[2]
                mittente=testo_richiesta[3]
                conn=psycopg2.connect(database="pymsg",user="calcolatori",password="calcolatori")
                cur = conn.cursor()
                cur.execute("INSERT INTO messaggi (mittente,destinatario,testo, letto) values (%s,%s,%s,false);",(mittente,destinatario,testo_messaggio))
                
                i+=1

                conn.commit()
                cur.close()
                conn.close()
                
                messaggio="inviato"
                i+=1
                self.lock.release()
            elif(testo_richiesta[0]=="spegni"):
                self.lock_spegnimento.acquire()
                spegni=True
                while num_client!=0 :
                    continue
                messaggio="hai spento il server"
                self.conn.send(messaggio.encode())
                self.conn.close()
                self.socket.close()
                self.lock_spegnimento.release()
                print("\nMi sto spegnendo ciaoooooo")
                sys.exit(0)
            else:
                messaggio="richiesta non valida"
            self.conn.send(messaggio.encode())
            self.lock.acquire()
            num_client-=num_client
            self.lock.release()
            print(f"Messaggio {messaggio} inviato a {self.ind_client}")
            self.conn.close()
        self.conn.close()

def launch(porta,backlog):
    try:
        server = socket.socket()
        server.setblocking(False) # imposto il socket non bloccante, poi in seguito renderò bloccante la singola connessione quando sarà necessario
        server.bind(("127.0.0.1",porta))
        server.listen(backlog)
        print("Server Inizializzato. "+socket.gethostbyname(socket.gethostname()) +" In ascolto...")
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")
        print(f"Sto tentando di reinizializzare il server...")
        test=input("riprovare? s/n ")
        if(test=="n"):
            return -1
        launch(porta, backlog)
    return server

def run_server(server,inizio,durata=0,log_file=""):
    #qui va l'apertura' del file di log
    while (time.time()-inizio)<durata or durata==0: # differenza conteggiata in secondi
        try:
            conn, indirizzo_client = server.accept() #conn = socket_client
            thread_req=requestHanlerThread(server,conn,indirizzo_client,log_file)
            thread_req.start()
        except BlockingIOError:
            #print("niente richieste "+str(time.time()-inizio)) #testing
            pass
        except OSError:
            sys.exit(1)
    return 0


if __name__ == "__main__":
    frasi=["ciccio","pluto","pippo"]
    inizio=time.time()
    porta=int(sys.argv[1])
    backlog=int(sys.argv[2])
    #aggiungere parametro sys.argv[3] per il tempo di timeout del server
    durata=0 # tempo di vita del server, se 0 significa infinito
    server=launch(porta,backlog)
    log_file="" #path del file di log
    if(server!=-1):
        while True:
            try:
                stato=run_server(server,inizio,durata,log_file)
                if(stato==0): #stato spento
                    break
            except KeyboardInterrupt: # condizione di spegnimento del server
                exit=input("\n Vuoi spegnere il server? (s per spegnerlo): ")
                if exit.lower()=="s":
                    print("\nMi sto spegnendo ciaoooooo")
                    server.close()
                    sys.exit(0)

                    #qui va la chiusura del file di log
                pass
        print("\nMi sto spegnendo ciaoooooo")
        server.close()
