# un fisier care dureaza prea mult pe un algoritm dar da bine pe altul
import sys

# fa fisierul sa dea minim pe euristica_admisibila_1
# fisierul in nu da  solutia minima pe euristica neadmisibila

# EURISTICA NEADMISIBILA IDEI

import copy
import os
import time


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    nrOrdine = 0
    timp_inceput = 0

    def __init__(self, miscariFacute, info, listaPiese, parinte, stariIncercate, cost=0, h=0):
        NodParcurgere.nrOrdine += 1
        self.id = NodParcurgere.nrOrdine
        self.durataCalcul = time.time() - NodParcurgere.timp_inceput
        self.miscariFacute = miscariFacute
        self.info = info
        self.listaPiese = listaPiese
        self.stariIncercate = copy.deepcopy(stariIncercate)
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self][:]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:

            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    #afisare custom
    def __str__(self):
        out = ""
        out += "f :" + str(self.f) + "\n"
        out += "Nr de Ordine:" + str(self.id) + "\n"
        out += "Timp Calcul:" + str(self.durataCalcul) + "\n"
        out += "Cost :" + str(self.g) + "\n"
        out += "Lungime drum:" + str(len(self.obtineDrum()) - 1) + "\n"
        out += "Miscari incercate:\n" + self.miscariFacute + "\n"
        matriceOut = ""
        for line in [''.join(x) for x in self.info]:
            matriceOut += line + "\n"
        out += "Matricea: \n" + matriceOut
        return out


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        f_open = open(nume_fisier, 'r')
        #verificare input
        try:
            line = f_open.readline()
            matrice = []
            lista_piese = []
            while (line):
                linie_matrice = []
                line = line.replace("\n", '')
                for ch in line:
                    linie_matrice.append(ch)
                    if (ch not in ["#", "."] and ch not in lista_piese):
                        lista_piese.append(ch)
                matrice.append(linie_matrice)
                line = f_open.readline()

            self.start = matrice
            self.lista_piese = lista_piese
            self.toateStarileIncercate = []
        except:
            print("Input Gresit")
            SystemExit

        print("Stare Initiala:", self.start)

    # testam daca matricea e solutie
    def testeaza_matrice(self, matrice):
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if (matrice[i][j] == "*"):
                    return 0
        return 1
    #verificarea solutie
    def testeaza_scop(self, nodCurent):
        return self.testeaza_matrice(nodCurent.info)

    #functii pentru a determina unde putem muta o piesa ( daca intr-o anumita directie este spatiu gol)
    def mutare_stanga_valida(self, matrice, pozitii, piesa):
        if (piesa != "*"):
            for i, j in pozitii:
                if (j == 0 or (matrice[i][j - 1] not in ['.', piesa])):
                    return 0
        else:
            for i, j in pozitii:
                if (j != 0):
                    if (matrice[i][j - 1] not in ['.', piesa]):
                        return 0
        return 1

    def mutare_dreapta_valida(self, matrice, pozitii, piesa):
        if (piesa != "*"):
            for i, j in pozitii:
                if (j == len(matrice[i]) - 1 or (matrice[i][j + 1] not in ['.', piesa])):
                    return 0
        else:
            for i, j in pozitii:
                if (j != len(matrice[i]) - 1):
                    if (matrice[i][j + 1] not in ['.', piesa]):
                        return 0
        return 1

    def mutare_sus_valida(self, matrice, pozitii, piesa):
        if (piesa != "*"):
            for i, j in pozitii:
                if (i == 0 or (matrice[i - 1][j] not in ['.', piesa])):
                    return 0
        else:
            for i, j in pozitii:
                if (i != 0):
                    if (matrice[i - 1][j] not in ['.', piesa]):
                        return 0
        return 1

    def mutare_jos_valida(self, matrice, pozitii, piesa):
        if (piesa != "*"):
            for i, j in pozitii:
                if (i == (len(matrice) - 1) or (matrice[i + 1][j] not in ['.', piesa])):
                    return 0
        else:
            for i, j in pozitii:
                if (i != len(matrice) - 1):
                    if (matrice[i + 1][j] not in ['.', piesa]):
                        return 0
        return 1

    def afiseaza_matrice(self, matrice):
        for lista in matrice:
            for x in lista:
                print(x, end=' ')
            print()

    def matrice_to_string(self, matrice, piesa, directie):

        out = "Am mutat " + piesa + " in " + directie + "\n"
        for lista in matrice:
            for x in lista:
                out += x + " "
            out += "\n"
        return out

    # functie care gaseste pozitiile unei piese
    def pozitii_dupa_piesa(self, matrice, piesa):
        pozitii = []
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if (matrice[i][j] == piesa):
                    pozitii.append([i, j])
        return pozitii

    # functie care executa mutarea pe matrice
    def mutare(self, matrice, pozitii, directie='stanga'):
        if (directie == 'stanga'):
            for i, j in pozitii:
                # daca e pe margine, iesim
                if (j == 0):
                    matrice[i][j] = '.'
                else:
                    copie = matrice[i][j - 1]
                    matrice[i][j - 1] = matrice[i][j]
                    matrice[i][j] = copie
        elif (directie == 'sus'):
            for i, j in pozitii:
                if (i == 0):
                    matrice[i][j] = '.'
                else:
                    copie = matrice[i - 1][j]
                    matrice[i - 1][j] = matrice[i][j]
                    matrice[i][j] = copie

        elif (directie == 'jos'):
            copie_pozitii = copy.deepcopy(pozitii)
            copie_pozitii = sorted(copie_pozitii, key=lambda x: x[0], reverse=True)

            for i, j in copie_pozitii:
                if (i == len(matrice) - 1):
                    matrice[i][j] = '.'
                else:
                    copie = matrice[i + 1][j]
                    matrice[i + 1][j] = matrice[i][j]
                    matrice[i][j] = copie
        elif (directie == 'dreapta'):
            # sortam sa se faca interschimbarea de la dreapta la stanga (sa ducem elementul de la j+1 pana in stanga formei)
            copie_pozitii = copy.deepcopy(pozitii)
            copie_pozitii = sorted(copie_pozitii, key=lambda x: x[1], reverse=True)

            for i, j in copie_pozitii:
                if (j == len(matrice[i]) - 1):
                    matrice[i][j] = '.'
                else:
                    copie = matrice[i][j + 1]
                    matrice[i][j + 1] = matrice[i][j]
                    matrice[i][j] = copie
        else:
            return 0

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        self.toateStarileIncercate.append(nodCurent.info)

        listaSuccesori = []
        copie_matrice = copy.deepcopy(nodCurent.info)

        for piesa in nodCurent.listaPiese:
            pozitii = self.pozitii_dupa_piesa(copie_matrice, piesa)

            pret = len(pozitii) if (piesa != "*") else 1 # Costul mutarii

            if (self.mutare_stanga_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_st = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_st, pozitii, 'stanga')

                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)

                stariIncercateNoi.append(copie_matrice_st)
                # verificare sa nu repetam nod pe aceiasi ramura
                if (copie_matrice_st not in nodCurent.stariIncercate) and (
                        True):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute + self.matrice_to_string(copie_matrice, piesa, 'stanga'),
                                      copie_matrice_st, self.lista_piese, nodCurent, stariIncercateNoi,
                                      nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_st, tip_euristica)))

            if (self.mutare_jos_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_jos = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_jos, pozitii, 'jos')

                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)
                stariIncercateNoi.append(copie_matrice_jos)
                #verificare sa nu repetam nod pe aceiasi ramura
                if (copie_matrice_jos not in nodCurent.stariIncercate and True):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute + self.matrice_to_string(copie_matrice, piesa, 'jos'),
                                      copie_matrice_jos, self.lista_piese, nodCurent, stariIncercateNoi,
                                      nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_jos, tip_euristica)))

            if (self.mutare_sus_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_sus = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_sus, pozitii, 'sus')

                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)
                stariIncercateNoi.append(copie_matrice_sus)
                # verificare sa nu repetam nod pe aceiasi ramura
                if (copie_matrice_sus not in nodCurent.stariIncercate) and (True):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute + self.matrice_to_string(copie_matrice, piesa, 'sus'),
                                      copie_matrice_sus, self.lista_piese, nodCurent, stariIncercateNoi,
                                      nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_sus, tip_euristica)))

            if (self.mutare_dreapta_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_dr = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_dr, pozitii, 'dreapta')

                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)
                stariIncercateNoi.append(copie_matrice_dr)
                # verificare sa nu repetam nod pe aceiasi ramura
                if (copie_matrice_dr not in nodCurent.stariIncercate) and (True):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute + self.matrice_to_string(copie_matrice, piesa, 'dreapta'),
                                      copie_matrice_dr, self.lista_piese, nodCurent, stariIncercateNoi,
                                      nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_dr, tip_euristica)))

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica_banala"):
        if tip_euristica == "euristica_banala":
            if self.testeaza_matrice(infoNod):
                return 0
            else:
                return 1  # minimul dintre costurile tuturor arcelor
        elif (tip_euristica == "euristica_admisibila_1"):  # distanta minima fata de un . sau # de pe margine
            if self.testeaza_matrice(infoNod):
                return 0
            else:
                pozitii = self.pozitii_dupa_piesa(infoNod, "*")
                distanta = float ('inf')
                for i in range(len(infoNod)):
                    for j in range(len(infoNod[i])):
                        if (i == 0 or i == len(infoNod) - 1 or j == 0 or j == len(infoNod[i]) - 1) and (
                                infoNod[i][j] == "#" or infoNod[i][j]=="."):
                            for x in pozitii:
                                if (distanta > abs(i - x[0]) + abs(j - x[1])):
                                    distanta = abs(i - x[0]) + abs(j - x[1])

                return distanta
        elif (tip_euristica == "euristica_admisibila_2"):  # distanta minima fata de orice de pe border in afara de #
            if self.testeaza_matrice(infoNod):
                return 0
            else:
                pozitii = self.pozitii_dupa_piesa(infoNod, "*")
                distanta = float('inf')
                for i in range(len(infoNod)):
                    for j in range(len(infoNod[i])):
                        if (i == 0 or i == len(infoNod) - 1 or j == 0 or j == len(infoNod[i]) - 1) and (
                                infoNod[i][j] != "#"):
                            for x in pozitii:
                                if (distanta > abs(i - x[0]) + abs(j - x[1])):
                                    distanta = abs(i - x[0]) + abs(j - x[1])

                return distanta
        elif (tip_euristica == "euristica_neadmisibila"):  # distanta maxima fata de o margine
                                                            # pe ida star da drum neoptim

            pozitii = self.pozitii_dupa_piesa(infoNod, "*")
            distanta = 0
            for i in range(len(infoNod)):
                for j in range(len(infoNod[i])):
                    if (i == 0 or i == len(infoNod) - 1 or j == 0 or j == len(infoNod[i]) - 1):
                        for x in pozitii:
                            if (distanta < abs(i - x[0]) + abs(j - x[1])):
                                distanta = abs(i - x[0]) + abs(j - x[1])
            return distanta

def uniform_cost(gr, nrSolutiiCautate=1, tip_euristica='euristica_banala'):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    out = ""
    c = [NodParcurgere("", gr.start, gr.lista_piese, None, [gr.start], 0, gr.calculeaza_h(gr.start, tip_euristica))]

    while len(c) > 0:
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            out += "Solutie: \n"
            out += nodCurent.__str__() + "\n"
            out += "\n----------------\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return out

        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)

        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici Či ĂŽn desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, nrSolutiiCautate, tip_euristica='euristica_banala'):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere("", gr.start, gr.lista_piese, None, [gr.start], 0, gr.calculeaza_h(gr.start, tip_euristica))]
    out = ""
    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            out += "Solutie: \n"
            out += nodCurent.__str__() + "\n"
            out += "\n----------------\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return out
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
    return out


def a_star_open_closed(gr, nrSolutiiCautate, tip_euristica='euristica_banala'):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [
        NodParcurgere("", gr.start, gr.lista_piese, None, [gr.start], 0, gr.calculeaza_h(gr.start, tip_euristica))]
    out = ""
    # l_open contine nodurile candidate pentru expandare

    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        #print("Coada actuala: " + str(l_open))

        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            out += "Solutie: \n"
            out += nodCurent.__str__() + "\n"
            out += "\n----------------\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return out
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)

    return out


def ida_star(gr, nrSolutiiCautate, f_write, tip_euristica='euristica_banala'):
    nodStart = NodParcurgere("", gr.start, gr.lista_piese, None, [gr.start], 0,
                             gr.calculeaza_h(gr.start, tip_euristica))
    limita = nodStart.f
    while True:

        # f_write.write(("Limita de pornire: "+ str(limita))+"\n")
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, f_write, tip_euristica)
        if rez == "gata":
            break
        if rez == float('inf'):
            f_write.write("No Solutions")
            break
        limita = rez
        # f_write.write(">>> Limita noua: "+ str(limita)+"\n")


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, f_write, tip_euristica):
    #f_write.write("A ajuns la: "+"\n")
    #f_write.write(nodCurent.__str__())
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:

        f_write.write("Solutie: \n")
        f_write.write(nodCurent.__str__())
        f_write.write(str(limita))
        f_write.write("\n----------------\n")

        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    minim = float('inf')
    if (len(lSuccesori) == 0):
        #f_write.write("No succesori:")
        #f_write.write(nodCurent.__str__())
        pass
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, f_write, tip_euristica)
        if rez == "gata":
            return 0, "gata"
        #f_write.write("Compara "+ str(rez)+ " cu "+ str(minim)+"\n")
        if rez < minim:
            minim = rez
            #f_write.write("Noul minim: "+ str(minim)+"\n")
    return nrSolutiiCautate, minim


def mainP(caleFiserInput, caleFolderOutput, nSol, timpTimeout):
    gr = Graph(caleFiserInput)

    out = ""
    for algoritm in ["uniform_cost","a_star", "a_star_open_closed", "ida_star"]:
        for euristica in ["euristica_admisibila_1", "euristica_admisibila_2", "euristica_neadmisibila",
                          "euristica_banala"]:
            NodParcurgere.nrOrdine = 0
            NodParcurgere.timp_inceput = time.time()
            f_write = open(caleFolderOutput + algoritm + euristica + ".txt", 'w')
            timp_inceput = time.time()
            if (algoritm == "a_star"):
                out = a_star(gr, nrSolutiiCautate=nSol, tip_euristica=euristica)
            elif (algoritm == "a_star_open_closed"):
                out = a_star_open_closed(gr, nrSolutiiCautate=nSol, tip_euristica=euristica)
            elif(algoritm == "ida_star"):
                out = ida_star(gr, nSol, f_write, tip_euristica=euristica)
            else:
                out = uniform_cost(gr,nSol,euristica)

            if (out != None):  # nu facem ida star
                timp_final = time.time()
                print(timp_final - timp_inceput)
                if (timp_final - timp_inceput > timpTimeout):
                    f_write.write("Timeout")
                else:
                    if (out == ""):
                        f_write.write("No Solutions")
                    else:
                        f_write.write(out)
            else:  # ida star
                timp_final = time.time()
                if (timp_final - timp_inceput > timpTimeout):
                    f_write.truncate(0)
                    f_write.write("Timeout")

            f_write.write("\nNumar noduri totale generate : " + str(len(gr.toateStarileIncercate)) + "\n")


def cheamaMain(inputFolder, outputFolder, nSolutii, timpTime):
    #caleFolderInput = inputFolder
    caleFolderInput = "input"
    #caleFolderOutput = outputFolder
    caleFolderOutput = "output"
    #nSol = int(nSolutii)
    nSol = 2
    #timpTimeout = float(timpTime)
    timpTimeout = 1 # 0.035 ar trb sa mearga a_star dar nu a_star_open_closed / ida_star

    for inputFilePath in os.listdir(caleFolderInput + "/"):
        mainP(caleFolderInput + "/" + inputFilePath,
              caleFolderOutput + "/" + inputFilePath[0:len(inputFilePath) - 4], nSol, timpTimeout)


if __name__ == '__main__':
    # python main2.py input output 2 20
    # python main2.py input output 3 0.035

    #cheamaMain(*sys.argv[1:])
    cheamaMain(0, 0, 0, 0)