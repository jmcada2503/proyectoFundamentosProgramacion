from random import choice, randint
import math

class player():
    def __init__(self, name="", piece=""):
        self.name = name
        self.piece = piece

    def getPiece(self):
        while True:
            self.piece = input(f"{self.name}, por favor indica con qué ficha deseas jugar [X] o [O]: ")
            if self.piece in ("X", "O"):
                break
            print("Debes ingresar [X] o [O]")

class game():
    def __init__(self, p1, p2):
        self.table = [[None]*7 for i in range(6)]
        self.p1 = p1
        self.p2 = p2
        self.turno = choice((p1,p2))

    def getTable(self):
        tableStr = " 1234567 \n+-------+\n"
        for i in range(6):
            tableStr += "|"
            for j in range(7):
                tableStr += self.table[i][j].piece if self.table[i][j] else "."
            tableStr += "|\n"
        tableStr += "+-------+\n"
        return tableStr

    def getRow(self, column):
        if self.table[0][column] != None:
            return False
        else:
            if self.table[5][column] == None:
                self.table[5][column] = self.turno
                if self.checkWin(5, column):
                    return "win"
            else:
                for i in range(1, 6):
                    if self.table[i][column] != None:
                        self.table[i-1][column] = self.turno
                        if self.checkWin(i-1, column):
                            return "win"
                        break
            return True

    def inputColumn(self):
        while True:
            column = input(f"{self.turno.name}, indica un número de columna o pulsa [S] para tentar la suerte: ")
            if column == "S":
                while True:
                    comprobacion = self.getRow(randint(0, 6))
                    if comprobacion == "win":
                        return "win"
                    elif comprobacion:
                        break
                break
            else:
                try:
                    column = int(column)
                    if column >= 1 and column <= 7:
                        comprobacion = self.getRow(column-1)
                        if comprobacion == "win":
                            return "win"
                        elif comprobacion:
                            break
                        else:
                            print("Esta columna está llena")
                    else:
                        print("Debes ingresar un número entre 1 y 7")
                except ValueError:
                    print("Debes ingresar un número")
        self.turno = self.p1 if self.turno == self.p2 else self.p2
        return None

    def checkFull(self):
        full = True
        for i in self.table[0]:
            if i == None:
                full = False
                break
        return full

    def checkWin(self, row, column):

        print(f"C: {column} R: {row}")

        win = False

        # Verificar fila
        cont = 0
        for i in self.table[row]:
            if i == self.turno:
                cont += 1
                if cont == 4:
                    win = True
                    break
            else:
                cont = 0

        # Verificar columna
        if not win:
            cont = 0
            for i in range(6):
                if self.table[i][column] == self.turno:
                    cont += 1
                    if cont == 4:
                        win = True
                        break
                else:
                    cont = 0

        # Verificar diagonal principal
        if not win:
            cont = 0
            if column-row < 0:
                pi = [row-column, 0]
            else:
                pi = [0, column-row]
            while pi[0] < 6 and pi[1] < 7:
                if self.table[pi[0]][pi[1]] == self.turno:
                    cont += 1
                    if cont == 4:
                        win = True
                        break
                else:
                    cont = 0
                pi[0] += 1
                pi[1] += 1

        # Verificar diagonal secundaria
        if not win:
            cont = 0
            if column-(5-row) < 0:
                pi = [(5-row)-column, 0]
            else:
                pi = [5, column-(5-row)]
            while pi[0] > 0 and pi[1] < 7:
                if self.table[pi[0]][pi[1]] == self.turno:
                    cont += 1
                    if cont == 4:
                        win = True
                        break
                else:
                    cont = 0
                pi[0] -= 1
                pi[1] += 1

        print("Win:", win)
        return win


print("*** CUATRO SEGUIDAS ***")
p1 = player(name=input("Por favor indique nombre de participante #1: "))
p1.getPiece()
p2 = player(name=input("Por favor indique nombre de participante #2: "), piece="X" if p1.piece == "O" else "O")
print(f"{p2.name}, te toca jugar con la siguiente ficha: {p2.piece}")

juego = game(p1, p2)

print("Lanzando una moneda para determinar quién inicia la partida...")
print(f"La partida la inicia {juego.turno.name}")

while True:
    print(juego.getTable())
    if juego.inputColumn() == "win":
        print(juego.getTable())
        print(f"¡Felicidades, {juego.turno.name}, has ganado la partida!")
        break
    if (juego.checkFull()):
        print(juego.getTable())
        print("El tablero está lleno, no se pueden hacer más jugadas, tenemos un empate")
        break
        
