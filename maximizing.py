eElec = 50e-09
eFs = 100e-12
packetSize = 500*8
d = 80
eTX = (eElec*packetSize)+(eFs*packetSize*(d**2))
eRX = eElec*packetSize
saludoSize = 25
saludoTx = (eElec*saludoSize)+(eFs*saludoSize*(d**2))
saludoRx = eElec*saludoSize
n_nodos = [3,3,6,12,24]
e_inicial = 5
paquetes = 0
coronas = []
condicion = True

class Corona:
    def __init__(self, nodos, corona):
        self.nodos = nodos
        if corona == 0:
            self.bateria = (nodos*e_inicial)-(e_inicial*nodos*.15)
        elif corona == 1:
            self.bateria = (nodos*e_inicial)+(e_inicial*nodos*0.079)
        elif corona == 4:
            self.bateria = (nodos*e_inicial)-(e_inicial*nodos*.0935)
        else:
            self.bateria = (nodos*e_inicial)+(e_inicial*nodos*.1365)
c = 0
for n in n_nodos:
    coronas.append(Corona(n, c))
    c += 1

suma = 0
for corona in coronas:
    suma += corona.bateria
print(suma)

def ciclo():
    global paquetes
    global condicion
    for c in range(len(coronas)):
        if c == 0:
            # Cada nodo de la corona más exterior (0) envía un Hello
            coronas[c].bateria -= saludoTx*coronas[c].nodos
            # En la corona 0 se recibe un Hello por cada nodo en la corona 1
            coronas[c].bateria -= saludoRx*coronas[c+1].nodos
            # Cada nodo de la corona 0 envía un paquete
            coronas[c].bateria -= eTX*coronas[c].nodos
            paquetes += coronas[c].nodos
        elif c == len(coronas)-1:
            # Cada nodo de la corona 'c' envía un Hello
            coronas[c].bateria -= saludoTx*coronas[c].nodos
            # Estos Hello se escuchan en la corona c-1
            coronas[c-1].bateria -= saludoRx*coronas[c].nodos
            # En la corona 'c' se escuchan los Hello de la corona c-1
            coronas[c].bateria -= saludoRx*coronas[c].nodos
            # Cada nodo de la corona 'c' envía un paquete
            coronas[c].bateria -= eTX*coronas[c].nodos
            # Estos paquetes se escuchan en la corona c-1
            coronas[c-1].bateria -= eRX*coronas[c].nodos
            # En la corona 'c' se escuchan los paquetes de la corona c-1
            coronas[c].bateria -= eRX*coronas[c].nodos
            paquetes += coronas[c].nodos - coronas[c-1].nodos
        else:
            # Cada nodo de la corona 'c' envía un Hello
            coronas[c].bateria -= saludoTx*coronas[c].nodos
            # Estos Hello se escuchan en las coronas c-1 y c+1
            coronas[c-1].bateria -= saludoRx*coronas[c].nodos
            coronas[c+1].bateria -= saludoRx*coronas[c+1].nodos
            # En la corona 'c' se escuchan los Hello de las coronas c+1 y c-1
            coronas[c].bateria -= saludoRx*coronas[c].nodos + saludoRx*coronas[c+1].nodos
            # Cada nodo de la corona 'c' envía un paquete
            coronas[c].bateria -= eTX*coronas[c].nodos
            # Estos paquetes se escuchan en las coronas c-1 y c+1
            coronas[c-1].bateria -= eRX*coronas[c].nodos
            coronas[c+1].bateria -= eRX*coronas[c+1].nodos
            # En la corona 'c' se escuchan los paquetes de las coronas c+1 y c-1
            coronas[c].bateria -= eRX*coronas[c].nodos + eRX*coronas[c+1].nodos
            paquetes += coronas[c].nodos - coronas[c-1].nodos
    
    contador = 0
    for corona in coronas:
        if corona.bateria > 0:
            contador += 1
    if contador < len(coronas):
        condicion = False

while condicion:
    ciclo()

for corona in coronas:
    print(corona.bateria)
print(paquetes - coronas[-1].nodos)