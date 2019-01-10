# Rozwiązuje losowe n x n puzzle przy wykorzystaniu A*
# przy oznaczeniach f(x) = g(x) + h(x)
# f(x) - ilość ruchów
# g(x) - głębokość, liczba przesunięć puzzli do tej pory
# h(x) - heurystyczny koszt z obecnego punktu do celu

import random
import math

stan_koncowy = [[1,2,3,4],
               [5,6,7,8],
               [9,10,11,12],
			   [13,14,15,0]]
wymiar = 4
	
# sprawdza czy dana plansza zawiera się w danej liście	
def czy_plansza_w_liscie(plansza, lista):
    try:
        return lista.czy_plansza_w_liscie(plansza)
    except:
        return -1

class NPuzzle:

	# konstruktor
    def __init__(self):
        # h(x)
        self._h_wartosc = 0
        # g(x)
        self._glebokosc = 0
        self._rodzic = None
		# macierz ułożenia puzzli
        self.puzzle_macierz = []
        for i in range(wymiar):
            self.puzzle_macierz.append(stan_koncowy[i][:])
			
	# operator porównania obiektów
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.puzzle_macierz == other.puzzle_macierz
			
	# print obiektu
    def __str__(self):
        res = ''
        for row in range(wymiar):
            res += ' '.join(map(str, self.puzzle_macierz[row]))
            res += '\r\n'
        return res
		
	#klonowanie obiektu
    def _klonuj(self):
        p = NPuzzle()
        for i in range(wymiar):
            p.puzzle_macierz[i] = self.puzzle_macierz[i][:]
        return p

	# lista dozwolonych zamian z puzzlem 0
    def _znajdz_dozwolone_ruchy(self):
        # znalezienie puzzla 0
        row, col = self.znajdz(0)
        dozwolone_ruchy = []
        
        # dodanie puzzla w zależności od jego położenia
        if row > 0:
            dozwolone_ruchy.append((row - 1, col))
        if col > 0:
            dozwolone_ruchy.append((row, col - 1))
        if row < wymiar-1:
            dozwolone_ruchy.append((row + 1, col))
        if col < wymiar-1:
            dozwolone_ruchy.append((row, col + 1))

        return dozwolone_ruchy

	# generuje dozwolone układy puzzli
    def _generuj_ruchy(self):
		#lista list dozwolonych ruchów
        dozwolone_ruchy_lista = self._znajdz_dozwolone_ruchy()
        zero = self.znajdz(0)

        def zamien_i_klonuj(a, b):
			# p jest teraz postaci początkowej
            p = self._klonuj()
			# zamiana wartości a i b, przesyłamy ich listy współrzędnych (puzzel 0 i sąsiad)
            p.zamien_wartosci(a,b)
			# dodanie odległości od stanu początkowego
            p._glebokosc = self._glebokosc + 1
			#zmiana rodzica na obiekt, który wywołał tą funkcję
            p._rodzic = self
			# zwrócenie nowego obiektu
            return p
		# iteracja po dozwolone_ruchy_lista i zwraca obiekty typu NPuzzle 
        return map(lambda pair: zamien_i_klonuj(zero, pair), dozwolone_ruchy_lista)

	# generuje ścieżkę od stanu x do stanu początkowego
    def _generuj_sciezke_rozwiazania(self, sciezka):
		# jeśli ta plansza jest rozwiązaniem to zwracamy ścieżkę
        if self._rodzic == None:
            return sciezka
		# jeśli plansza nie jest rozwiązaniem to dodajemy ją do ścieżki i rekurencyjnie powtarzamy procedurę
        else:
            sciezka.append(self)
            return self._rodzic._generuj_sciezke_rozwiazania(sciezka)
	# algorytm A*
    def rozwiaz(self, h):
		# h - wybrana heurystyka
		# porównuje ułożenie końcowe z danym ułożeniem puzzli
        def czy_rozwiazane(puzzle):
            return puzzle.puzzle_macierz == stan_koncowy
		
		# deklaracja otwartej i zamkniętej(uniemożliwia cofnięcie ostatniego ruchu) listy przeszukiwań
        otwarta_lista = [self]
        zamknieta_lista = []
        licznik_ruchow = 0
		# dopóki otwarta_lista posiada jakieś ułożenia puzzli
        while len(otwarta_lista) > 0:
			# pobierz pierwszy element z otwartej listy
            x = otwarta_lista.pop(0)
            licznik_ruchow += 1
			# sprawdza czy dane ułożenie jest szukanym rozwiązaniem
            if (czy_rozwiazane(x)):
                if len(zamknieta_lista) > 0:
                    return x._generuj_sciezke_rozwiazania([]), licznik_ruchow
				#przypadek gdy stan po początkowym przemieszeniu jest już stanem końcowym
                else:
                    return [x]
			# jeśli nie jest ułożone to generujemy kolejne ruchy
            nastepne_ulozenia_puzzli = x._generuj_ruchy()
            index_otwarty = index_zamkniety = -1
            for plansza in nastepne_ulozenia_puzzli:
                # sprawdzamy dla każdej planszy czy znajduje się w otwartej i zamkniętej liście
                index_otwarty = czy_plansza_w_liscie(plansza, otwarta_lista)
                index_zamkniety = czy_plansza_w_liscie(plansza, zamknieta_lista)
				# uruchomienie heurystyki i obliczenie wartości h
                h_war = h(plansza)
				# f(x) = h(x) + g(x)
                f_war = h_war + plansza._glebokosc

				# jeśli nie ma planszy w zamkniętaj i otwartej liście, to dodajemy ją do otwartej listy
                if index_zamkniety == -1 and index_otwarty == -1:
                    plansza._h_wartosc = h_war
                    otwarta_lista.append(plansza)
				# jeśli plansza jest w otwartej liście to aktualizujemy jej parametry
                elif index_otwarty > -1:
                    kopia_puzzle = otwarta_lista[index_otwarty]
                    if f_war < kopia_puzzle._h_wartosc + kopia_puzzle._glebokosc:
                        kopia_puzzle._h_wartosc = h_war
                        kopia_puzzle._rodzic = plansza._rodzic
                        kopia_puzzle._glebokosc = plansza._glebokosc
				# jeśli plansza jest w zamkniętej liście
                elif index_zamkniety > -1:
                    kopia_puzzle = zamknieta_lista[index_zamkniety]
                    if f_war < kopia_puzzle._h_wartosc + kopia_puzzle._glebokosc:
                        plansza._h_wartosc = h_war
                        zamknieta_lista.remove(kopia_puzzle)
                        otwarta_lista.append(plansza)
			# po przeszukaniu aktualizujemy zamkniętą listę
            zamknieta_lista.append(x)
			# sortujemy otwartą listę według najlepszej wartości f(x)
            otwarta_lista = sorted(otwarta_lista, key=lambda p: p._h_wartosc + p._glebokosc)

        # błąd braku rozwiązania
        return [], 0
		
	# generuje losowy układ puzzli z układu początkowego do układu docelowego
    def generuj_losowy_uklad_docelowy(self, liczba_przeksztalcen):
        for i in range(liczba_przeksztalcen):
            row, col = self.znajdz(0)
            dozwolone_ruchy = self._znajdz_dozwolone_ruchy()
			# losowy ruch
            wybrany_sasiad = random.choice(dozwolone_ruchy)
			# zamiana wartości puzzla 0 i losowego sąsiada
            self.zamien_wartosci((row, col), wybrany_sasiad)
            #row, col = wybrany_sasiad
	
	# znajdowanie wiersza i kolumny zawierającego zerowy kafelek
    def znajdz(self, value):
        if value < 0 or value > wymiar ** 2 - 1:
            raise Exception("value out of range")

        for row in range(wymiar):
            for col in range(wymiar):
                if self.puzzle_macierz[row][col] == value:
                    return row, col
					
    # sprawdz_wartoscenie wartości dla danego wiersza i kolumny
    def sprawdz_wartosc(self, row, col):
        return self.puzzle_macierz[row][col]

	# wstawienie wartości w dane pole
    def wstaw_wartosc(self, row, col, value):
        self.puzzle_macierz[row][col] = value

	# zamiana wartości dwóch wybranych puzzli
    def zamien_wartosci(self, poz_a, poz_b):
		#tymczasowe przechowanie wartości
        temp = self.sprawdz_wartosc(*poz_a)
		# dwukrotne wstawienie wartości na konkretne pozycje
        self.wstaw_wartosc(poz_a[0], poz_a[1], self.sprawdz_wartosc(*poz_b))
        self.wstaw_wartosc(poz_b[0], poz_b[1], temp)


def heur(puzzle, calkowity_koszt_h_danej_planszy, oblicz_calkowity_koszt):
    calkowity_koszt_h_wszystkich_planszy = 0
    for row in range(wymiar):
        for col in range(wymiar):
			# dla każdego puzzla szukamy jego miejsca docelowego w macierzy
            nr_puzzla = puzzle.sprawdz_wartosc(row, col) - 1
            target_col = nr_puzzla % wymiar
            target_row = nr_puzzla / wymiar

            # dla puzzla 0, który ma być w prawym dolnym rogu
            if target_row < 0: 
                target_row = wymiar
			# obliczenie kosztu pojedynczego ułożenia puzzli dla danej heurystyki
            calkowity_koszt_h_wszystkich_planszy += calkowity_koszt_h_danej_planszy(row, target_row, col, target_col)
	# zwrócenie całkowitego kosztu danej heurystyki dla wszystkich stanów
    return oblicz_calkowity_koszt(calkowity_koszt_h_wszystkich_planszy)

# różne heurystyki liczące funkcę h

# Manhattan distance exploring
def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

# Manhattan least squares exploring
def h_manhattan_lsq(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: (abs(tr - r) + abs(tc - c))**2,
                lambda t: math.sqrt(t))

# linear distance exploring
def h_linear(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: math.sqrt(math.sqrt((tr - r)**2 + (tc - c)**2)),
                lambda t: t)

# linear least squares exploring
def h_linear_lsq(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: (tr - r)**2 + (tc - c)**2,
                lambda t: math.sqrt(t))


def main():
	#stworzenie ułożonych puzzli
    p = NPuzzle()
	# przemieszanie stanu początkowego
    p.generuj_losowy_uklad_docelowy(20)
    print(p)

    sciezka, liczba_stanow = p.rozwiaz(h_manhattan)
	# odwrócenie kolejności i rysowanie każdej macierzy puzzli
    sciezka.reverse()
    for i in sciezka: 
        print(i)

    print("Rozwiązano metodą Manhattan distance exploring z przeszukiwaniem ", liczba_stanow, "stanów.")
    sciezka, liczba_stanow = p.rozwiaz(h_manhattan_lsq)
    print("Rozwiązano metodą Manhattan least squares exploring z przeszukiwaniem", liczba_stanow, "stanów.")
    sciezka, liczba_stanow = p.rozwiaz(h_linear)
    print("Rozwiązano metodą linear distance exploring z przeszukiwaniem", liczba_stanow, "stanów.")
    sciezka, liczba_stanow = p.rozwiaz(h_linear_lsq)
    print("Rozwiązano metodą linear least squares exploring z przeszukiwaniem", liczba_stanow, "stanów.")

if __name__ == "__main__":
    main()