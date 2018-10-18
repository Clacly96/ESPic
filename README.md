# PyMsg

## Why PyMsg?
This project has been created as a mini-thesis for the main course “Computer Systems and Networks” related exam. Its purpose is to explain the Socket’s operating principles, and how they enable to establish connections and exchange messages in order to create protocols and services.
The project was carried out by three students from Marche Polytechnic University:

-Broccoletti Roberto

-Spada Claudio

-Spada Valeria Anna

## What is PyMsg?
PyMsg is a python lightweight messaging service composed by two type of services: one with a central server and the other one is a P2P implementation.
Both services are based on python socket implementation.

## What is a socket?
A socket is one endpoint of a two-way communication link between two programs running on the network. A socket is bound to a port number so that the TCP layer can identify the application that data is destined to be sent to.
Socket are based on the Unix file model, so the operations on socket are open, close, read and write, adding some parameters like ip address and protocol.

## PyMsg schemas
PyMsg peer-to-peer version:

![Schema](https://github.com/Clacly96/PyMsg/blob/master/docs/p2p.png)

PyMsg Client-Server version:

![Schema](https://github.com/Clacly96/PyMsg/blob/master/docs/CS.png)
