eElec = 50e-09
eFs = 100e-12
packetSize = 500*8
d = 80
eTX = (eElec*packetSize)+(eFs*packetSize*(d**2))
eRX = eElec*packetSize
saludoSize = 100
saludoTx = (eElec*saludoSize)+(eFs*saludoSize*(d**2))
saludoRx = eElec*saludoSize
n_nodos = [3,3,6,12,16]
e_inicial = 5
paquetes = 0
coronas = []
condicion = True

class Corona:
    def __init__(self, nodos):
        self.nodos = nodos
        self.bateria = nodos*e_inicial

for n in n_nodos:
    coronas.append(Corona(n))

def ciclo():
    global paquetes
    global condicion
    for c in range(len(coronas)):
        if c == 0:
            coronas[c].bateria -= saludoTx*coronas[c].nodos
            coronas[c].bateria -= saludoRx*coronas[c+1].nodos
            coronas[c].bateria -= eTX*coronas[c].nodos
            paquetes += coronas[c].nodos
        else:
            coronas[c].bateria -= saludoRx*coronas[c-1].nodos
            coronas[c].bateria -= saludoTx*coronas[c].nodos
            coronas[c].bateria -= eRX*coronas[c-1].nodos
            coronas[c].bateria -= eTX*coronas[c].nodos
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