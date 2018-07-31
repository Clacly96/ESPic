import socket
import threading
from guizero import App, TextBox, PushButton, Text, ListBox,info

def apri_messaggio(selezionato):
    #finestra_messaggio.show()
    info("Messaggio",str(selezionato))

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
    if nome_mittente.value!="":
        c=socket_client(("127.0.0.1",15000))    
        if c!=-1:
            avvisi.clear()
            mittente=nome_mittente.value
            r="GET"+"&$%"+str(mittente)    
            c.send(r.encode())
            risposta= c.recv(1024)
            print(str(risposta.decode()))
            risposta_decod=risposta.decode()
            if risposta_decod!="":
                messaggi=risposta_decod.split("/&/")
                #lista_messaggi.clear()
                for messaggio in messaggi:
                    if len(messaggio)>0:
                        print(f"messaggio {messaggio}")
                        mess_diviso=messaggio.split("&$%")
                        lista_messaggi.append(mess_diviso[0]+", Inviato da: "+mess_diviso[1]+ " Orario: "+mess_diviso[2])
            c.close()        
        elif c==-1:
            avvisi.value="Errore di connessione, l'altro client potrebbe non essere connesso"
    else:
        avvisi.value="Inserisci il tuo nome per ricevere messaggi"

def invia_dati():
    if textbox.value=="":
        avvisi.value="Non inviare messaggi vuoti"
        return -1
    if nome_destinatario.value=="":
        avvisi.value="Inserisci nome desinatario"
        return -1
    if nome_mittente.value=="":
        avvisi.value="Inserisci nome mittente"
        return -1
    c=socket_client(("127.0.0.1",15000))    
    if c!=-1:
        testo_messaggio=textbox.value
        richiesta="POST"+"&$%"+str(testo_messaggio)+"&$%"+str(nome_destinatario.value)+"&$%"+str(nome_mittente.value)
        c.send(richiesta.encode())
        risposta= c.recv(1024)
        print(str(risposta.decode()))
        avvisi.value=risposta.decode()
        c.close()
        textbox.clear()            
    elif c==-1:
        avvisi.value="Errore di connessione, l'altro client potrebbe non essere connesso"
    
    
if __name__ == "__main__":
    

    interfaccia= App(layout="grid",width=700,title="pymsg")
    messaggi_ricevuti = Text(interfaccia, text="Messaggi ricevuti",align="left",grid=[0,0])
    #lista_messaggi=Text(interfaccia,grid=[0,1])
    #lista_messaggi.height = 5
    lista_messaggi=ListBox(interfaccia,scrollbar=True,align="left",command=apri_messaggio,grid=[0,2,6,1])
    lista_messaggi.width=80
    lista_messaggi.repeat(2000,richiedi_messaggi)
    text = Text(interfaccia, text="Inserisci il testo del messaggio",align="left",grid=[0,6])
    textbox = TextBox(interfaccia,grid=[0,7,4,1])
    textbox.width=30
    tastoInvio = PushButton(interfaccia, text="Invia",align="left", command=invia_dati,grid=[5,7])
    Labelnome=Text(interfaccia, text="Inserisci il tuo nome",align="left",grid=[0,9])
    nome_mittente = TextBox(interfaccia,width=20,grid=[0,10,4,1])
    Labeldest=Text(interfaccia, text="Inserisci destinatario",align="left",grid=[0,11])
    nome_destinatario=TextBox(interfaccia,width=20,grid=[0,12,4,1])
    Labelavvisi=Text(interfaccia, text="Avvisi:",align="left",grid=[0,13])
    avvisi=Text(interfaccia,size=9,align="left",grid=[0,14])

    # finestra_messaggio=Window(interfaccia)
    # finestra_messaggio.hide()
    # Labelmit=Text(finestra_messaggio,text="Mittente: ")
    # mit=Text(finestra_messaggio)
    # Labeltesto=Text(finestra_messaggio,text="Testo: ")
    # testo=Text(finestra_messaggio)
    # testo.width=10
    # testo.height=70
    # Labelora=Text(finestra_messaggio,text="Ora: ")
    # orario=Text(finestra_messaggio)
    
    
    interfaccia.display()


    