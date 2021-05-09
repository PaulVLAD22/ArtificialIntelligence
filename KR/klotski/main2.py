
# un fisier care dureaza prea mult pe un algoritm dar da bine pe altul


# ceilalti 2 algoritmi

# fa fisierul sa dea minim pe euristica_admisibila_1
# fisierul in nu da  solutia minima pe euristica neadmisibila


import copy
import os
import time


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    nrOrdine=0
    timp_inceput = 0
    def __init__(self,miscariFacute, info, listaPiese, parinte, stariIncercate, cost=0, h=0):
        NodParcurgere.nrOrdine+=1
        self.id = NodParcurgere.nrOrdine
        self.durataCalcul = time.time()-NodParcurgere.timp_inceput
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
        out=""
        out+="f :"+str(self.f)+"\n"
        out+="Nr de Ordine:"+str(self.id)+"\n"
        out+="Timp Calcul:"+str(self.durataCalcul)+"\n"
        out+="Cost :"+str(self.g)+"\n"
        out+="Lungime drum:"+str(len(self.stariIncercate)-1)+"\n"
        out+="Miscari incercate:\n" + self.miscariFacute +"\n"
        matriceOut=""
        for line in [''.join(x) for x in self.info]:
            matriceOut+=line+"\n"
        out+="Matricea: \n"+matriceOut
        return out


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        f_open = open(nume_fisier, 'r')

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

        print("Stare Initiala:", self.start)
        input()

    # testam daca matricea e solutie
    def testeaza_matrice(self, matrice):
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if (matrice[i][j] == "*"):
                    return 0
        return 1

    def testeaza_scop(self, nodCurent):
        return self.testeaza_matrice(nodCurent.info)

    # gresite TREBUIE SA POT MUTA DOAR DACA E GOL IN STANGA//DREAPTA/SUS/JOS  (sunt puncte)
    def mutare_stanga_valida(self, matrice, pozitii, piesa):
        if (piesa!="*"):
            for i,j in pozitii:
                if (j==0 or (matrice[i][j-1] not in ['.',piesa])):
                    return 0
        else:
            for i,j in pozitii:
                if (j!=0):
                    if (matrice[i][j-1] not in ['.',piesa]):
                        return 0
        return 1




        # piese_intercalate = {}
        # for i, j in pozitii:
        #     if ((piesa != "*" and j < 1) or matrice[i][j - 1] == "#"):
        #         return 0
        #     # verificam ca numarul partilor dintr-o piesa care sunt mutate sa fie egal cu lungimea piesei ( toata piesa sa se muta)
        #     if (matrice[i][j - 1] not in ['.', piesa]):
        #         if (matrice[i][j - 1] not in piese_intercalate.keys()):
        #             piese_intercalate[matrice[i][j - 1]] = 1
        #         else:
        #             piese_intercalate[matrice[i][j - 1]] += 1
        #
        # for k in piese_intercalate.keys():
        #     if (len(self.pozitii_dupa_piesa(matrice, k)) != piese_intercalate[k]):
        #         return 0
        #
        # return 1

    def mutare_dreapta_valida(self, matrice, pozitii, piesa):
        if (piesa!="*"):
            for i,j in pozitii:
                if (j==len(matrice[i])-1 or (matrice[i][j+1] not in ['.',piesa])):
                    return 0
        else:
            for i,j in pozitii:
                if (j!=len(matrice[i])-1):
                    if (matrice[i][j+1] not in ['.',piesa]):
                        return 0
        return 1

        # piese_intercalate = {}
        # for i, j in pozitii:
        #     if ((piesa != "*" and j > len(matrice[i]) + 2) or matrice[i][j + 1] == "#"):
        #         return 0
        #     # verificam ca numarul partilor dintr-o piesa care sunt mutate sa fie egal cu lungimea piesei ( toata piesa sa se muta)
        #     if (matrice[i][j + 1] not in ['.', piesa]):
        #         if (matrice[i][j + 1] not in piese_intercalate.keys()):
        #             piese_intercalate[matrice[i][j + 1]] = 1
        #         else:
        #             piese_intercalate[matrice[i][j + 1]] += 1
        #
        # for k in piese_intercalate.keys():
        #     if (len(self.pozitii_dupa_piesa(matrice, k)) != piese_intercalate[k]):
        #         return 0
        # return 1

    def mutare_sus_valida(self, matrice, pozitii, piesa):
        if (piesa!="*"):
            for i,j in pozitii:
                if (i==0 or (matrice[i-1][j] not in ['.',piesa])):
                    return 0
        else:
            for i,j in pozitii:
                if (i!=0):
                    if (matrice[i-1][j] not in ['.',piesa]):
                        return 0
        return 1
        # piese_intercalate = {}
        # for i, j in pozitii:
        #     if ((piesa != "*" and i < 1) or matrice[i - 1][j] == "#"):
        #         return 0
        #     # verificam ca numarul partilor dintr-o piesa care sunt mutate sa fie egal cu lungimea piesei ( toata piesa sa se muta)
        #     if (matrice[i - 1][j] not in ['.', piesa]):
        #         if (matrice[i - 1][j] not in piese_intercalate.keys()):
        #             piese_intercalate[matrice[i - 1][j]] = 1
        #         else:
        #             piese_intercalate[matrice[i - 1][j]] += 1
        #
        # for k in piese_intercalate.keys():
        #     if (len(self.pozitii_dupa_piesa(matrice, k)) != piese_intercalate[k]):
        #         return 0
        # return 1

    def mutare_jos_valida(self, matrice, pozitii, piesa):
        if (piesa!="*"):
            for i,j in pozitii:
                if (i==(len(matrice)-1) or (matrice[i+1][j] not in ['.',piesa])):
                    return 0
        else:
            for i,j in pozitii:
                if (i!=len(matrice)-1):
                    if (matrice[i+1][j] not in ['.',piesa]):
                        return 0
        return 1
        # piese_intercalate = {}
        # for i, j in pozitii:
        #     if ((piesa != "*" and i > len(matrice) - 2) or matrice[i + 1][j] == "#"):
        #         return 0
        #     # verificam ca numarul partilor dintr-o piesa care sunt mutate sa fie egal cu lungimea piesei ( toata piesa sa se muta)
        #     if (matrice[i + 1][j] not in ['.', piesa]):
        #         if (matrice[i + 1][j] not in piese_intercalate.keys()):
        #             piese_intercalate[matrice[i + 1][j]] = 1
        #         else:
        #             piese_intercalate[matrice[i + 1][j]] += 1
        #
        # for k in piese_intercalate.keys():
        #     if (len(self.pozitii_dupa_piesa(matrice, k)) != piese_intercalate[k]):
        #         return 0
        # return 1

    def afiseaza_matrice(self, matrice):
        for lista in matrice:
            for x in lista:
                print(x, end=' ')
            print()
    def matrice_to_string(self,matrice,piesa,directie):

        out="Am mutat "+piesa+" in "+directie+"\n"
        for lista in matrice:
            for x in lista:
                out+=x+" "
            out+="\n"
        return out
    def pozitii_dupa_piesa(self, matrice, piesa):
        pozitii = []
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if (matrice[i][j] == piesa):
                    pozitii.append([i, j])
        return pozitii

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
        #if (len(self.toateStarileIncercate )==2):
        #   self.afiseaza_matrice(nodCurent.info)


        #print (nodCurent.info in self.toateStarileIncercate)

        listaSuccesori = []
        copie_matrice = copy.deepcopy(nodCurent.info)

        for piesa in nodCurent.listaPiese:
            pozitii = self.pozitii_dupa_piesa(copie_matrice, piesa)

            pret = len(pozitii) if (piesa != "*") else 1


            if (self.mutare_stanga_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_st = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_st, pozitii, 'stanga')


                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)

                stariIncercateNoi.append(copie_matrice_st)

                if (copie_matrice_st not in nodCurent.stariIncercate) and (copie_matrice_st not in self.toateStarileIncercate):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute+self.matrice_to_string(copie_matrice,piesa,'stanga'),copie_matrice_st, self.lista_piese,nodCurent, stariIncercateNoi, nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_st, tip_euristica)))


            if (self.mutare_jos_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_jos = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_jos, pozitii, 'jos')

                # print(nodCurent.stariIncercate.append(copie_matrice_jos))
                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)
                stariIncercateNoi.append(copie_matrice_jos)


                if (copie_matrice_jos not in nodCurent.stariIncercate and copie_matrice_jos not in self.toateStarileIncercate):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute+self.matrice_to_string(copie_matrice,piesa,'jos'),copie_matrice_jos, self.lista_piese, nodCurent, stariIncercateNoi,
                                      nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_jos, tip_euristica)))


            if (self.mutare_sus_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_sus = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_sus, pozitii, 'sus')

                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)
                stariIncercateNoi.append(copie_matrice_sus)


                if (copie_matrice_sus not in nodCurent.stariIncercate) and (copie_matrice_sus not in self.toateStarileIncercate):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute+self.matrice_to_string(copie_matrice,piesa,'sus'),copie_matrice_sus, self.lista_piese, nodCurent, stariIncercateNoi,
                                      nodCurent.g + pret,
                                      self.calculeaza_h(copie_matrice_sus, tip_euristica)))


            if (self.mutare_dreapta_valida(copie_matrice, pozitii, piesa)):

                copie_matrice_dr = copy.deepcopy(copie_matrice)
                self.mutare(copie_matrice_dr, pozitii, 'dreapta')

                stariIncercateNoi = copy.deepcopy(nodCurent.stariIncercate)
                stariIncercateNoi.append(copie_matrice_dr)

                if (copie_matrice_dr not in nodCurent.stariIncercate) and (copie_matrice_dr not in self.toateStarileIncercate):
                    listaSuccesori.append(
                        NodParcurgere(nodCurent.miscariFacute+self.matrice_to_string(copie_matrice,piesa,'dreapta'),copie_matrice_dr, self.lista_piese, nodCurent, stariIncercateNoi,
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
        elif (tip_euristica=="euristica_admisibila_1"): # distanta fata de un . de pe border
            if self.testeaza_matrice(infoNod):
                return 0
            else:
                pozitii = self.pozitii_dupa_piesa(infoNod,"*")
                distanta = float ('inf')
                for i in range (len(infoNod)):
                    for j in range (len(infoNod[i])):
                        if (i == 0 or i == len(infoNod)-1 or j==0 or j==len(infoNod[i])-1 )and (infoNod[i][j]=="."):
                            for x in pozitii:
                                if (distanta > abs(i-x[0])+abs(j-x[1])):
                                    distanta = abs(i-x[0])+abs(j-x[1])
                if (distanta==float('inf')):
                    self.afiseaza_matrice(infoNod)
                return distanta
        elif (tip_euristica == "euristica_admisibila_2"): # distanta fata de orice de pe border in afara de #
            if self.testeaza_matrice(infoNod):
                return 0
            else:
                pozitii = self.pozitii_dupa_piesa(infoNod,"*")
                distanta = float('inf')
                for i in range(len(infoNod)):
                    for j in range(len(infoNod[i])):
                        if (i == 0 or i == len(infoNod) - 1 or j == 0 or j == len(infoNod[i]) - 1) and (
                                infoNod[i][j] != "#"):
                            for x in pozitii:
                                if (distanta > abs(i - x[0]) + abs(j - x[1])):
                                    distanta = abs(i - x[0]) + abs(j - x[1])

                return distanta
        elif (tip_euristica == "euristica_neadmisibila"): # distanta maxima fata de orice de pe border in afara de #
            #luam cea mai indepartata gaura

            # nu merge


            pozitii = self.pozitii_dupa_piesa(infoNod, "*")
            distanta = 0
            for i in range(len(infoNod)):
                for j in range(len(infoNod[i])):
                    if (i == 0 or i == len(infoNod) - 1 or j == 0 or j == len(infoNod[i]) - 1) and (
                            infoNod[i][j] == "#"):
                        for x in pozitii:
                            if (distanta < abs(i - x[0]) + abs(j - x[1])):
                                distanta = abs(i - x[0]) + abs(j - x[1])
            if (infoNod[0]==['#','.','#','#','#']):
                print(distanta)
            return distanta





    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    out=""
    c = [NodParcurgere("",gr.start, gr.lista_piese, None, [gr.start], 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            out+="Solutie: \n"
            out+=nodCurent.__str__()+"\n"
            out+="\n----------------\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return out

        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

def a_star(gr, nrSolutiiCautate, tip_euristica='euristica banala',timp_inceput=time.time()):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere("",gr.start, gr.lista_piese, None, [gr.start], 0, gr.calculeaza_h(gr.start))]
    out=""
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


def main(caleFiserInput, caleFolderOutput, nSol, timpTimeout):
    gr = Graph(caleFiserInput)

    f_write = open(caleFolderOutput,'w')
    #timp_inceput = time.time()
    #print("\n\n##################\nSolutii obtinute cu UCS:")
    #out = uniform_cost(gr, nrSolutiiCautate=nSol)
    #print(time.time()-timp_inceput)
    NodParcurgere.nrOrdine = 0
    NodParcurgere.timp_inceput = time.time()
    timp_inceput = time.time()
    print("\n\n##################\nSolutii obtinute cu A*:")
    out = a_star(gr, nrSolutiiCautate=nSol,tip_euristica="euristica_admisibila_2")
    timp_final = time.time()
    if (timp_final - timp_inceput > timpTimeout):
        f_write.write("Timeout")
    else:
        if (out==None):
            f_write.write("No Solutions")
        else:
            f_write.write(out)



if __name__ == '__main__':

    caleFolderInput = "input"
    caleFolderOutput = "output"
    nSol = 2
    timpTimeout = 20
    """
    print("Cale Folder input:")
    caleFolderInput = input()
    print("Cale Folder output")
    caleFolderOutput = input()
    print("Nr Solutii:")
    nSol = int(input())
    print("Timpul de timeout:")
    timpTimeout = int(input())
    """

    for inputFilePath in os.listdir(caleFolderInput + "/"):
        main(caleFolderInput + "/" + inputFilePath, caleFolderOutput+"/"+inputFilePath[0:len(inputFilePath)-4]+"_out.txt", nSol, timpTimeout)
