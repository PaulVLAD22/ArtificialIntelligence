# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    graf = None  # static

    def __init__(self, id, info, parinte, cost, h):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info # numarul nodului
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
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += " g:{}".format(self.g)
        sir += " h:{}".format(self.h)

        sir += " f:{})".format(self.f)
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matriceAdiacenta, matricePonderi, start, scopuri, lista_h):
        self.noduri = noduri
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matriceAdiacenta)
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
            if self.matriceAdiacenta[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
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


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
noduri = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k"]

m = [
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
mp = [
    [0, 3, 9, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 10, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 1, 0, 0, 10, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 7, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
start = "a"
scopuri = ["f"]
# exemplu de euristica banala (1 daca nu e nod scop si 0 daca este)
vect_h = [0, 10, 3, 7, 8, 0, 14, 3, 1, 2]

gr = Graph(noduri, m, mp, start, scopuri, vect_h)
NodParcurgere.graf = gr;



def a_star(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    q_open = [NodParcurgere(gr.indiceNod(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(q_open) > 0:
        print("Coada actuala: " + str(q_open))
        input()
        nodCurent = q_open.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum()
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        # Rezolvați condiția cu g-ul (funcția a-star)
        for s in lSuccesori:
            #cautam locul lui s
            gasit = False  # s gasit in coada open ?
            for x in q_open:
                if s.info == x.info: # daca gasim acelasi nod, vrem sa vedem care i drumul mai bun
                    gasit = True
                    if x.f > s.f: # cost anticipat pana la nod scop mai mare e eliminat
                        q_open.remove(x)
                    elif x.f == s.f:  # acelasi cost anticipat =>
                        if x.g > s.g: # costul mai mare e eliminat
                            q_open.remove(x)
                        else:
                            lSuccesori.remove(s)
                    else:# cost anticipat pana la nod scop e mai mare ca cel al instantei nodului aflat in open
                        lSuccesori.remove(s)
            # a trecut prin toate elementele, nu contineau acelasi nod ca s
            if gasit==False:
                for x in closed:
                    if s.info == x.info:
                        if x.f > s.f:
                            closed.remove(x)
                        elif x.f == s.f:  # Verificam daca f-urile sunt egal
                            if x.g > s.g:
                                c.remove(x)
                            else:
                                lSuccesori.remove(s)
                        else:
                            lSuccesori.remove(s)


a_star(gr, nrSolutiiCautate=3)