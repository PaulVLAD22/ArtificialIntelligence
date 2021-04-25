"""
Dati enter dupa fiecare solutie afisata.

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet, cu indicii incepănd de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului ascii al literei blocului de mutat si codul ascii al literei "a" ) .
"""

import copy


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:

            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "  "
                else:
                    sir += stiva[inalt - 1] + " "
            sir += "\n"
        sir += "-" * (2 * len(self.info) - 1)
        return sir

    """
    def __str__(self):
        sir=""
        for stiva in self.info:
            sir+=(str(stiva))+"\n"
        sir+="--------------\n"
        return sir
    """


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        def obtineStive(sir):
            stiveSiruri = sir.strip().split("\n")
            listaStive = [sirStiva.strip().split() if sirStiva != "#" else [] for sirStiva in stiveSiruri]
            return listaStive

        f = open(nume_fisier, 'r')

        continutFisier = f.read()
        siruriStari = continutFisier.split("stari_finale")
        self.start = obtineStive(siruriStari[0])  # stare initiala

        self.scopuri = []
        siruriStariFinale = siruriStari[1].strip().split("---")
        for scop in siruriStariFinale:
            self.scopuri.append(obtineStive(scop))
        print("Stare Initiala:", self.start)
        print("Stari finale posibile:", self.scopuri)
        input()

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri;

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        rangeStive = range(len(nodCurent.info))
        # nodCurent.info
        for i in rangeStive:
            if len(nodCurent.info[i]) == 0:
                continue
            copieStive = copy.deepcopy(nodCurent.info)
            bloc = copieStive[i].pop()  # sterge si returneaza ultimul element din lista
            for j in rangeStive:
                if i == j:
                    continue
                infoNodNou = copy.deepcopy(copieStive)
                infoNodNou[j].append(bloc)
                if not nodCurent.contineInDrum(infoNodNou):
                    costArc = 1
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc,
                                                        self.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if infoNod in self.scopuri:
                return 0
            else:
                return 1  # minimul dintre costurile tuturor arcelor
        elif (tip_euristica =="euristica admisibila 1"):
            stari_finale = self.scopuri[:]
            nrMinim = float("inf")
            # pentru fiecare stare scop
            for stare_scop in stari_finale:
                nrMutari = 0
                # pentru fiecare stiva din infoNod (adica informatia nodului curent)
                for i in range(len(infoNod)):

                    # pentru fiecare bloc din stiva din nodul curent
                    for j in range(len(infoNod[i])):
                        #daca nu exista indicele blocului in stiva din starea scop (stiva din starea curenta e mai mare decat cea din starea scop)
                        if (len(stare_scop[i])<=j):
                            nrMutari += 1
                        # daca informatiile blocurilor de la acelasi indice de stiva si acelasi nivel sunt diferite nrMutari creste cu 1
                        elif stare_scop[i][j] != infoNod[i][j]:
                            nrMutari += 1
                # actualizam minimul
                if nrMutari < nrMinim:
                    nrMinim = nrMutari
            return nrMinim

        """
        if tip_euristica=="euristica admisibila 1":
        minim=float('inf')
        pentru fiecare stare scop (stScop)
            nrMutari=0
            pentru fiecare stiva din infoNod (adica informatia nodului curent)
                pentru fiecare bloc din stiva din nodul curent
                    daca nu exista indicele blocului in stiva din starea scop (stiva din starea curenta e mai mare decat cea din starea scop)
                                nrMutari creste cu 1
                in caz contrar (exista indicele)
                    daca informatiile blocurilor de la acelasi indice de stiva si acelasi nivel sunt diferite nrMutari creste cu 1
            daca nrMutari<minim actualizeaza minim
        return minim
        """

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie:")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(True, True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


gr = Graph("in.txt")

# Rezolvat cu breadth first
#print("Solutii obtinute cu breadth first:")
# breadth_first(gr, nrSolutiiCautate=3)

#print("\n\n##################\nSolutii obtinute cu UCS:")
# print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
#uniform_cost(gr, nrSolutiiCautate=5)
# print("\n\n##################\nSolutii obtinute cu A*:")
#a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica banala")
a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica admisibila 1")
