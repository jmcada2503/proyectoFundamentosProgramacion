from random import choice, randint
import json
from datetime import datetime

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

    def showScoreTable(self):
        with open("scores.json", "r") as f:
            data = json.loads(f.read())

        ordered_names = list(data.keys())
        for i in range(len(ordered_names)):
            for j in range(len(ordered_names)-1):
                if data[ordered_names[j]]['score'] < data[ordered_names[j+1]]['score']:
                    ordered_names[j], ordered_names[j+1] = ordered_names[j+1], ordered_names[j]

        print("\n*** TABLA DE POSICIONES ***\n")
        for i in range(len(ordered_names)):
            print(f"{i+1}. {ordered_names[i]} {data[ordered_names[i]]['score']} puntos acumulados. Última partida en {data[ordered_names[i]]['date']}")
        print()



    def updateScores(self, win:bool = False):
        with open("scores.json", "r") as f:
            data = json.loads(f.read())

        # Update when win
        if win:
            if data.get(self.turno.name):
                data[self.turno.name]['score'] += 1
            else:
                data[self.turno.name] = {'score': 1, 'date': datetime.now().strftime('%Y-%m-%d a las %H:%M')}

        # Always update to create new users
        if not data.get(self.p1.name):
            data[self.p1.name] = {'score': 0, 'date': datetime.now().strftime('%Y-%m-%d a las %H:%M')}
        if not data.get(self.p2.name):
            data[self.p2.name] = {'score': 0, 'date': datetime.now().strftime('%Y-%m-%d a las %H:%M')}

        with open("scores.json", "w") as f:
            f.write(json.dumps(data))

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
                            print("Esta columna está llena...")
                            print(f"El jugador {self.turno.name} pierde el turno")
                            break
                    else:
                        print("Debes ingresar un número entre 1 y 7")
                except ValueError:
                    print("Debes ingresar un número")
        self.turno = self.p1 if self.turno == self.p2 else self.p2

    def checkFull(self):
        full = True
        for i in self.table[0]:
            if i == None:
                full = False
                break
        return full

    def checkWin(self, row, column):
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
        print("Has sumado 1 punto esta partida! :D")
        juego.updateScores(win=True)
        juego.showScoreTable()
        while True:
            ans = input("¿Desean volver a tomar la partida Si [S] No [N]?:")
            if ans == "N":
                break
            elif ans == "S":
                juego = game(p1, p2)
                break
            else:
                print("Debes ingresar Si [S] No [N]")
        if ans == "N":
            break
    if (juego.checkFull()):
        print(juego.getTable())
        print("El tablero está lleno, no se pueden hacer más jugadas, tenemos un empate")
        juego.updateScores()
        juego.showScoreTable()
        while True:
            ans = input("¿Desean volver a tomar la partida Si [S] No [N]?:")
            if ans == "N":
                break
            elif ans == "S":
                juego = game(p1, p2)
                break
            else:
                print("Debes ingresar Si [S] No [N]")
        if ans == "N":
            break
