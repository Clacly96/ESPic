import socket,sys,time,threading,pickle
import mysql.connector
import DBsetting

## ------Inizio Funzioni per il db---------
def connessioneDb():
    db = mysql.connector.connect(
    host=DBsetting.host,
    user=DBsetting.user,
    passwd=DBsetting.passwd,
    database=DBsetting.database)
    return db

def controlloUtente(username):
    db=connessioneDb()
    cursore=db.cursor()
    cursore.execute("SELECT username FROM utenti WHERE username=%s",(username,))
    risposta=cursore.fetchone()
    cursore.close()
    db.close()
    if risposta:
        return True
    else:
        return False
    
def controlloPassword(username,password):
    db=connessioneDb()
    cursore=db.cursor()
    cursore.execute("SELECT username,password FROM utenti WHERE username=%s",(username,))
    risposta=cursore.fetchone()
    cursore.close()
    db.close()
    if risposta:
        username,pwd=risposta
        username=username.decode('utf-8')
        pwd=pwd.decode('utf-8')
        if pwd==password:
            return True
        else:
            return False
    else:
        return False
    

def inserisciUtente(username,password):
    db=connessioneDb()
    cursore=db.cursor()
    cursore.execute("INSERT INTO utenti (username, password) VALUES (%s,%s)",(username,password))
    db.commit()
    cursore.close()
    db.close()

def estraiUtenti():
    db=connessioneDb()
    cursore=db.cursor()
    cursore.execute("SELECT username FROM utenti ORDER BY username")
    risposta=cursore.fetchall()
    cursore.close()
    db.close()
    return risposta


##------Fine funzioni DB-----------

num_client=0
spegni=False

class requestHandlerThread (threading.Thread):
    def __init__(self, socket, connessione,indirizzo_client):
      threading.Thread.__init__(self)
      self.conn = connessione
      self.ind_client=indirizzo_client
      self.lock=threading.Lock()
      self.socket=socket

    def run(self):
        global spegni
        if spegni==False:   #se il server è in fase di spegnimento, nuovi thread non gestiscono la richiesta ma si chiudono direttamente            
            self.conn.setblocking(True) # imposta la connessione corrente come bloccante
            self.conn.settimeout(200) # setta il timeout per la connessione corrente, in secondi
            print(f"Connessione Server - Client Stabilita: {self.ind_client}\n")
            self.richiesta=self.conn.recv(4096)
            self.testo_richiesta=pickle.loads(self.richiesta)

            if self.testo_richiesta[0].upper()=="GET" and len(self.testo_richiesta)>1:
                self.lock.acquire()

                self.destinatario=str(self.testo_richiesta[1])

                self.db=connessioneDb()
                self.cursore = self.db.cursor()
                self.cursore.execute("SELECT id,testo,mittente,data FROM messaggi WHERE letto=false AND destinatario=%s",(self.destinatario,))
                self.selezione=self.cursore.fetchall()

                self.messaggio=[]
                self.messaggi_letti=[]
                if self.selezione:
                    for riga in self.selezione:
                        
                        ID,testo,mittente,data=riga
                        self.messaggio.append([str(testo.decode('utf-8')),str(mittente.decode('utf-8')),str(data)])                     
                        self.messaggi_letti.append(ID)

                    ## Aggiornamento messaggi letti
                    format_strings = ','.join(['%s'] * len(self.messaggi_letti))
                    self.cursore.execute("UPDATE messaggi SET letto=true WHERE id IN (%s)" % format_strings,tuple(self.messaggi_letti))
                    self.db.commit()               

                ## Chiusura connessione db
                self.cursore.close()
                self.db.close()

                self.lock.release()
            elif(self.testo_richiesta[0].upper()=="POST" and len(self.testo_richiesta)>1):
                self.lock.acquire()

                testo_messaggio=self.testo_richiesta[1]
                destinatario=self.testo_richiesta[2]
                mittente=self.testo_richiesta[3]

                self.db=connessioneDb()
                self.cursore = self.db.cursor()
                self.cursore.execute("INSERT INTO messaggi (mittente,destinatario,testo, letto) values (%s,%s,%s,false);",(mittente,destinatario,testo_messaggio))
                
                self.db.commit()
                self.cursore.close()
                self.db.close()
                
                self.messaggio="inviato"

                self.lock.release()

            elif(self.testo_richiesta[0].upper()=="SERVICE" and len(self.testo_richiesta)>1):
                self.azione=self.testo_richiesta[1]

                if(self.azione=="regUser"):
                    self.username=self.testo_richiesta[2]
                    self.password=self.testo_richiesta[3]
                    self.risposta=controlloUtente(self.username)
                    if self.risposta==True:
                        self.messaggio="ESISTENTE"
                    else:
                        inserisciUtente(self.username,self.password)
                        self.messaggio="INSERITO"

                elif(self.azione=="checkPwd"):
                    self.username=str(self.testo_richiesta[2])
                    self.password=str(self.testo_richiesta[3])
                    self.risposta=controlloPassword(self.username,self.password)

                    if self.risposta==True:                        
                        self.messaggio="CORRETTO"
                    else:
                        self.messaggio="ERRORE"

                elif(self.azione=="estraiUtenti"):
                    self.risposta=estraiUtenti()
                    self.messaggio=self.risposta
            else:
                self.messaggio="richiesta non valida"
            self.messaggio_ser=pickle.dumps(self.messaggio)
            self.conn.send(self.messaggio_ser)
            print(f"Messaggio {self.messaggio} inviato a {self.ind_client}")
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
threads=[]
def run_server(server,inizio,durata=0):
    global threads
    while (time.time()-inizio)<durata or durata==0: # differenza conteggiata in secondi
        try:
            conn, indirizzo_client = server.accept() #conn = socket_client
            thread_req=requestHandlerThread(server,conn,indirizzo_client)
            thread_req.start()
            threads.append(thread_req)            
        except BlockingIOError:
            pass
        except OSError:
            sys.exit(1)
    return 0


if __name__ == "__main__":
    inizio=time.time()
    try:
        porta=int(sys.argv[1])
        backlog=int(sys.argv[2])
        durata=int(sys.argv[3])
    except:
        print("Inserire: porta, backlog, timeout (0 per tempo illimitato)")
        sys.exit(1)
    server=launch(porta,backlog)
    if server!=-1:
        try:
            stato=run_server(server,inizio,durata)
        except KeyboardInterrupt: # condizione di spegnimento del server
            exit=input("\n Vuoi spegnere il server? (s per spegnerlo): ")
            if exit.lower()=="s":
                for thread in threads:
                    thread.join()
                server.close()
                print("\nMi sto spegnendo ciaoooooo")
                sys.exit(0)

            else:
                pass
    else:
        print("Si sono verificati errori")
        sys.exit(1)

