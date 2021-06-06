"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii până vă apare o soluție. Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada și input()
"""

##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
noduri = ["a", "b", "c", "d", "e", "f", "g"]

m = []

vect_h = [4,4,9,10,11,0,5]
mp = [
    #a  b  c  d   e  f  g
    [0, 2, 5, 11, 0, 0, 8], #a
    [0, 0, 0, 3, 0, 20, 0], #b
    [0, 1, 0, 0, 4, 22, 2],  #c
    [0, 20, 4, 0, 0, 0, 0],  #d
    [0, 0, 0, 0, 0, 11, 6],  #e
    [0, 0, 0, 0, 0, 0, 0],  #f
    [0, 0, 0, 0, 19, 0, 0]]  #g

print("NR MUCHII ",sum([len([i for i in x if i != 0]) for x in mp]))
for i in range(len(mp)):
    for j in range(len(mp[i])):
        if mp[i][j]!=0:
            print(noduri[i],"-"+str(mp[i][j])+"->",noduri[j])
start = "a"
scopuri = ["f"]
# exemplu de euristica banala (1 daca nu e nod scop si 0 daca este)

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    graf = None  # static

    def __init__(self, id, info, parinte, cost, h):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # costul de la radacina la nodul curent
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self.info];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print(("->").join(l))
        print("Cost: ", self.g)
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
        sir += "(info:"+self.info
        sir += " g:{}".format(self.g)

        sir += " f:{} ".format(self.f)
        if (self.parinte):
            sir += "parinte:{})".format(self.parinte.info)
        else:
            sir+="parinte:None)"
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matriceAdiacenta, matricePonderi, start, scopuri, lista_h):
        self.noduri = noduri
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matricePonderi)
        self.start = start
        self.scopuri = scopuri
        self.lista_h = lista_h

    def indiceNod(self, n):
        return self.noduri.index(n)

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri;

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            if self.matricePonderi[nodCurent.id][i] != 0 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent, nodCurent.g + self.matricePonderi[nodCurent.id][i],
                                       self.calculeaza_h(self.noduri[i]))
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def calculeaza_h(self, infoNod):
        return self.lista_h[self.indiceNod(infoNod)]

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)




gr = Graph(noduri, m, mp, start, scopuri, vect_h)
NodParcurgere.graf = gr;


def a_star(gr):
    print(" LE TAI PE ALEA CARE AU FOST INLOCUITE IN ARBORE")
    print(" DACA SE INLOCUIESTE DIN CLOSE , TAIEM TOT CE E SUB EL")
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]
    noduri = [l_open[0]]

    # l_open contine nodurile candidate pentru expandare
    n=1
    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        print("Pas "+str(n))
        n+=1
        print("open: " + str(l_open))
        print("closed: "+str(l_closed))
        print("\n"*2)
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            print("Noduri:")
            print(noduri)
            return
        print("S-a extins " +nodCurent.info)
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        toBeEliminated = []
        # print(lSuccesori)
        for index, s in enumerate(lSuccesori):
            # print("Succesor -",s.info)
            #print (f'Succesor actual {s}')
            gasitC = False
            for nodC in l_open:
                # print(s.info, nodC.info)
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        print("nodul vechi din open -"+nodC.info+"- nu a fost inlocuit")
                        # lSuccesori.remove(s)
                        toBeEliminated.append(index)
                    else:  # s.f<nodC.f
                        print("nodul vechi din open -" + nodC.info + "- a fost inlocuit de unul cu cost mai mic")
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:

                        if s.f >= nodC.f:
                            # pass
                            toBeEliminated.append(index)
                            print("Nodul " +nodC.info+ " din closed nu a fost inlocuit")
                            # lSuccesori.remove(s)
                            #print("Removed",s)
                            # print(lSuccesori)
                        else:  # s.f<nodC.f
                            print("Nodul din close "+nodC.info +" a fost inlocuit de " + s.__repr__())
                            l_closed.remove(nodC)
                        break
        # print("B-----------|,",toBeEliminated)
        #print (f'Indecsi: {toBeEliminated}')
        for index in sorted(toBeEliminated, reverse=True):
            lSuccesori.pop(index)
        for s in lSuccesori:
            i = 0
            noduri.append(s)
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


a_star(gr)