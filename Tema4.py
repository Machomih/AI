import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import time

dictionar_q = {}


class LumeaGrilei(object):

    def __init__(self):
        super(LumeaGrilei, self).__init__()
        self.start = 0
        self.sosire = 0
        self.randuri = 7
        self.coloane = 10
        self.x_max = self.coloane - 1
        self.y_max = self.randuri - 1
        self.vant_1 = [3, 4, 5, 8]
        self.vant_2 = [6, 7]
        self.lista_actiuni = ['N', 'E', 'S', 'V']

    def celula(self, poz):
        return poz[1] + self.coloane * poz[0]

    def seteazaTerminal(self, stareStart, stareSosire):
        self.start = self.celula(stareStart)
        self.sosire = self.celula(stareSosire)

    def urmatoareaStare(self, stare, actiune):
        x = stare % self.coloane
        y = (stare - x) / self.coloane
        del_x = 0
        del_y = 0
        if actiune == 'E':
            del_x = 1
        elif actiune == 'V':
            del_x = -1
        elif actiune == 'N':
            del_y = -1
        elif actiune == 'S':
            del_y = 1
        else:
            raise ('Actiune Invalida! Actiunile trebuie sa fie in: ', self.lista_actiuni)
        nou_x = max(0, min(x + del_x, self.x_max))
        nou_y = max(0, min(y + del_y, self.y_max))
        if nou_x in self.vant_1:
            nou_y = max(0, nou_y - 1)
        if nou_x in self.vant_2:
            nou_y = max(0, nou_y - 2)

        return self.celula((nou_y, nou_x))

    def verificaTerminal(self, stare):
        return stare == self.sosire

    def functieRecompensa(self, stare_urmatoare):
        if stare_urmatoare == self.sosire:
            return 0
        else:
            return -1


def caleTraiectorie(lume, traiectorie):
    harta_lume = np.zeros((lume.randuri, lume.coloane))
    for i, stare in enumerate(traiectorie):
        x = int(stare % lume.coloane)
        y = int((stare - x) / lume.coloane)
        harta_lume[y, x] = i + 1
    print(harta_lume)
    print("\n")


def LumeaGrilei_QLearning(lume, stareStart, stareSosire, alfa, gamma=1, ep_max=300, eps=0.1):
    lume.seteazaTerminal(stareStart, stareSosire)

    for stare in range(lume.randuri * lume.coloane):
        dictionar_q[stare] = {}
        for act in lume.lista_actiuni:
            if lume.verificaTerminal(stare):
                dictionar_q[stare][act] = 0
            else:
                dictionar_q[stare][act] = np.random.rand()

    def actiuneLacom(_dictionar_q):
        act_lacom = ''
        max_q = -1e10
        for act in lume.lista_actiuni:
            if _dictionar_q[act] > max_q:
                act_lacom = act
                max_q = _dictionar_q[act]
        return act_lacom

    def epsLacom(episod, dictionar_q):
        m = len(lume.lista_actiuni)
        act_lacom = actiuneLacom(dictionar_q)
        p = []
        for act in lume.lista_actiuni:
            if act == act_lacom:
                p.append((eps * 1. / m) + 1 - eps)
            else:
                p.append(eps * 1. / m)
        alegere = np.random.choice(lume.lista_actiuni, size=1, p=p)
        return alegere[0]

    ep_cu_pas = []
    traiectorie = []
    recompense_totale = []
    for ep in range(1, ep_max + 1):
        s = lume.start
        traiectorie = []
        recompensa_totala = 0
        while not lume.verificaTerminal(s):
            act = epsLacom(ep, dictionar_q[s])
            s_urm = lume.urmatoareaStare(s, act)
            recompensa = lume.functieRecompensa(s_urm)

            recompensa_totala += recompensa

            act_urm = actiuneLacom(dictionar_q[s_urm])
            dictionar_q[s][act] += alfa * (recompensa + gamma * dictionar_q[s_urm][act_urm] - dictionar_q[s][act])

            traiectorie.append(s)

            s = s_urm
            ep_cu_pas.append(ep)
        traiectorie.append(lume.sosire)
        recompense_totale.append(recompensa_totala)
    return traiectorie, ep_cu_pas, recompense_totale


def afiseazaPolitica(lume):
    harta_politicii = np.full((lume.randuri, lume.coloane), ' ')
    for stare in range(lume.randuri * lume.coloane):
        if lume.verificaTerminal(stare):
            harta_politicii[stare // lume.coloane][stare % lume.coloane] = 'G'
        else:
            cea_mai_buna_actiune = max(dictionar_q[stare], key=dictionar_q[stare].get)
            harta_politicii[stare // lume.coloane][stare % lume.coloane] = cea_mai_buna_actiune[0]
    print(harta_politicii)


def incearca_caz_1(timp_start, lume, stareStart, stareSosire, alfa, gamma, ep_max, eps):
    traiectorie, ep_cu_pas, recompense_totale = LumeaGrilei_QLearning(lume, stareStart, stareSosire, alfa, gamma,
                                                                      ep_max, eps)
    print("Timp scurs pentru cazul 1: ", time.time() - timp_start)
    print(f"Numarul de miscari: {len(traiectorie)}")
    caleTraiectorie(lume, traiectorie)
    pl.figure(1)
    pl.plot(ep_cu_pas)
    plt.title('LumeaGrilei_Q-learning (eps=0.1,alfa=0.1)')
    pl.xlabel("Numarul de pasi facuti")
    pl.ylabel("Numarul de episoade")
    pl.show()
    pl.figure(2)
    pl.plot(recompense_totale)
    plt.title('Recompense Totale per Episod')
    pl.xlabel("Episoade")
    pl.ylabel("Recompensa Totala")
    pl.show()


def incearca_caz_2(timp_start, lume, stareStart, stareSosire, alfa, gamma, ep_max, eps):
    traiectorie, ep_cu_pas, recompense_totale = LumeaGrilei_QLearning(lume, stareStart, stareSosire, alfa, gamma,
                                                                      ep_max, eps)
    print("Timp scurs pentru cazul 2: ", time.time() - timp_start)
    print(f"Numarul de miscari: {len(traiectorie)}")
    caleTraiectorie(lume, traiectorie)
    pl.figure(1)
    pl.plot(ep_cu_pas)
    plt.title('LumeaGrilei_Q-learning (eps=0.2,alfa=0.1)')
    pl.xlabel("Numarul de pasi facuti")
    pl.ylabel("Numarul de episoade")
    pl.show()
    pl.figure(2)
    pl.plot(recompense_totale)
    plt.title('Recompense Totale per Episod')
    pl.xlabel("Episoade")
    pl.ylabel("Recompensa Totala")
    pl.show()


def incearca_caz_3(timp_start, lume, stareStart, stareSosire, alfa, gamma, ep_max, eps):
    traiectorie, ep_cu_pas, recompense_totale = LumeaGrilei_QLearning(lume, stareStart, stareSosire, alfa, gamma,
                                                                      ep_max, eps)
    print("Timp scurs pentru cazul 3: ", time.time() - timp_start)
    print(f"Numarul de miscari: {len(traiectorie)}")
    caleTraiectorie(lume, traiectorie)
    pl.figure(1)
    pl.plot(ep_cu_pas)
    plt.title('LumeaGrilei_Q-learning (eps=0.5,alfa=0.2)')
    pl.xlabel("Numarul de pasi facuti")
    pl.ylabel("Numarul de episoade")
    pl.show()
    pl.figure(2)
    pl.plot(recompense_totale)
    plt.title('Recompense Totale per Episod')
    pl.xlabel("Episoade")
    pl.ylabel("Recompensa Totala")
    pl.show()


if __name__ == '__main__':
    start = (3, 0)
    sosire = (3, 7)
    lume = LumeaGrilei()

    timp_start = time.time()
    incearca_caz_1(timp_start, lume, stareStart=start, stareSosire=sosire, alfa=0.5, gamma=1, ep_max=300, eps=0.1)
    afiseazaPolitica(lume)
    timp_start = time.time()
    incearca_caz_2(timp_start, lume, stareStart=start, stareSosire=sosire, alfa=0.1, gamma=1, ep_max=300, eps=0.2)
    afiseazaPolitica(lume)
    timp_start = time.time()
    incearca_caz_3(timp_start, lume, stareStart=start, stareSosire=sosire, alfa=0.2, gamma=1, ep_max=300, eps=0.5)
    afiseazaPolitica(lume)
