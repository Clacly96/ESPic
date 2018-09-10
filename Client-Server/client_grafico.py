import socket
import threading,pickle
from guizero import App, TextBox, PushButton, Text, ListBox,info,Window,error
username="" # Variabile che conterrà l'username dell'utente

def apri_messaggio(selezionato):
    info("Messaggio",str(selezionato))

def mostra_login():
    finestraLog.show()
    finestraReg.hide()
    finestraScelta.hide()

def mostra_registrazione():
    finestraReg.show()
    finestraLog.hide()
    finestraScelta.hide()

def login():
    global username
    c=socket_client(("127.0.0.1",15000))
    if c!=-1:
        r=["SERVICE","checkPwd",usernameLogin.value,passwordLogin.value]
        r_ser=pickle.dumps(r)    
        c.send(r_ser)
        risposta= c.recv(1024)
        risposta_decod=pickle.loads(risposta)
        if risposta_decod!="":
            if risposta_decod=="CORRETTO":
                interfaccia.enable()
                finestraLog.hide()
                username=usernameLogin.value
                labelUsername.value="Benvenuto "+username
                utenti=richiedi_utenti()
                for utente in utenti:
                    lista_utenti.append(utente)
            elif risposta_decod=="ERRORE":
                error("Errore","Username o password errati, riprova.")
        c.close()        
    elif c==-1:
        error("Errore","Errore di connessione, il server potrebbe non essere disponibile")

def registrazione():
    global username
    c=socket_client(("127.0.0.1",15000))
    if c!=-1:
        r=["SERVICE","regUser",usernameReg.value,passwordReg.value]
        r_ser=pickle.dumps(r)
        c.send(r_ser)
        risposta= c.recv(1024)
        risposta_decod=pickle.loads(risposta)
        if risposta_decod!="":
            if risposta_decod=="INSERITO":
                interfaccia.enable()
                finestraReg.hide()
                info("Successo","Registrazione avvenuta con successo")
                username=usernameReg.value
                labelUsername.value="Benvenuto "+username
                utenti=richiedi_utenti()
                for utente in utenti:
                    lista_utenti.append(utente)
            elif risposta_decod=="ESISTENTE":
                error("Errore","Username già esistente, riprova.")
        c.close()        
    elif c==-1:
        error("Errore","Errore di connessione, il server potrebbe non essere disponibile")

def socket_client(indirizzo):
    try:
        c = socket.socket()
        c.connect(indirizzo)
        print("[Client]Connessione stabilita")
    except OSError:
        print("[Client]Il server scelto non è disponibile")
        return -1
    except socket.error:
        print(f"[Client]Si è verificato un errore: {socket.error}")
        return -1
    return c

def richiedi_messaggi():
    global username    
    if username!="":
        c=socket_client(("127.0.0.1",15000))    
        if c!=-1:
            avvisi.clear()
            r=["GET",str(username)]
            r_ser=pickle.dumps(r)    
            c.send(r_ser)
            risposta= c.recv(1024)
            risposta_decod=pickle.loads(risposta)
            if risposta_decod!="":
                for messaggio in risposta_decod:
                    if len(messaggio)>0:
                        print(f"messaggio {messaggio}")
                        lista_messaggi.append(messaggio[0]+", Inviato da: "+messaggio[1]+ " Orario: "+messaggio[2])
            c.close()        
        elif c==-1:
            avvisi.value="Errore di connessione, il server potrebbe non essere disponibile"
    else:
        return -1

def invia_dati():
    global username
    if textbox.value=="":
        return -1
    if lista_utenti.value==None:
        avvisi.value="Inserisci nome desinatario"
        return -1
    c=socket_client(("127.0.0.1",15000))    
    if c!=-1:
        testo_messaggio=textbox.value
        richiesta=["POST",str(testo_messaggio),str(lista_utenti.value),username]
        richiesta_ser=pickle.dumps(richiesta)
        c.send(richiesta_ser)
        risposta= c.recv(1024)
        avvisi.value=pickle.loads(risposta)
        c.close()
        textbox.clear()            
    elif c==-1:
        error("Errore","Errore di connessione, il server potrebbe non essere disponibile")

def richiedi_utenti():
    c=socket_client(("127.0.0.1",15000))    
    if c!=-1:
        richiesta=["SERVICE","estraiUtenti"]
        richiesta_ser=pickle.dumps(richiesta)
        c.send(richiesta_ser)
        risposta= c.recv(1024000)        
        c.close()         
        utenti=pickle.loads(risposta)
        utenti_decod=[]
        for utente in utenti:
            ut,=utente
            ut_decod=ut.decode('utf-8')
            if ut_decod!=username:
                utenti_decod.append(ut_decod)
        return utenti_decod
    elif c==-1:
        avvisi.value="Errore di connessione, il server potrebbe non essere disponibile"
    

if __name__ == "__main__":
    

    interfaccia= App(layout="grid",width=700,height=700,title="pymsg")
    interfaccia.disable()
    messaggi_ricevuti = Text(interfaccia, text="Messaggi ricevuti",align="left",grid=[0,0])
    lista_messaggi=ListBox(interfaccia,scrollbar=True,align="left",command=apri_messaggio,grid=[0,2,6,1])
    lista_messaggi.width=80
    lista_messaggi.repeat(2000,richiedi_messaggi)
    text = Text(interfaccia, text="Inserisci il testo del messaggio",align="left",grid=[0,6])
    textbox = TextBox(interfaccia,grid=[0,7,4,1])
    textbox.width=30
    tastoInvio = PushButton(interfaccia, text="Invia",align="left", command=invia_dati,grid=[5,7])
    labelUsername=Text(interfaccia, text="",align="left",grid=[0,9])
    Labeldest=Text(interfaccia, text="Inserisci destinatario",align="left",grid=[0,11])
    #nome_destinatario=TextBox(interfaccia,width=20,grid=[0,12,4,1])
    lista_utenti=ListBox(interfaccia,scrollbar=True,align="left",grid=[0,12,6,1])
    lista_utenti.width=80
    Labelavvisi=Text(interfaccia, text="Avvisi:",align="left",grid=[0,13])
    avvisi=Text(interfaccia,size=9,align="left",grid=[0,14])
    
    ## Finestra per registrazione e login
    finestraScelta = Window(interfaccia,layout="grid",title="Login",width=300,height=100)
    Text(finestraScelta,text="Login o registrati",align="left",grid=[0,0])
    PushButton(finestraScelta, text="Login",align="left", command=mostra_login,grid=[0,2])
    PushButton(finestraScelta, text="Registrati",align="left", command=mostra_registrazione,grid=[1,2])

    ## Finestra Login
    finestraLog = Window(interfaccia,layout="grid",title="Login",visible=False)
    Text(finestraLog, text="Username:",align="left",grid=[0,1])
    usernameLogin=TextBox(finestraLog,width=20,grid=[0,2])
    Text(finestraLog, text="Password:",align="left",grid=[0,3])
    passwordLogin=TextBox(finestraLog,width=20,grid=[0,4])
    PushButton(finestraLog, text="Login",align="left", command=login,grid=[0,6])
    PushButton(finestraLog, text="Registrati",align="left", command=mostra_registrazione,grid=[0,9])

    ## Finestra Registrazione
    finestraReg = Window(interfaccia,layout="grid",title="Login",visible=False)
    Text(finestraReg, text="Username:",align="left",grid=[0,1])
    usernameReg=TextBox(finestraReg,width=20,grid=[0,2])
    Text(finestraReg, text="Password:",align="left",grid=[0,3])
    passwordReg=TextBox(finestraReg,width=20,grid=[0,4])
    PushButton(finestraReg, text="Registrati",align="left", command=registrazione,grid=[0,6])
    PushButton(finestraReg, text="Login",align="left", command=mostra_login,grid=[0,9])

    interfaccia.display()


    