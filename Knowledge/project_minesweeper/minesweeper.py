import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) > 0 and self.count == 0:
            return self.cells.copy()
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        set_mapa = set()
        for i in range(self.height):
            for j in range(self.width):
                set_mapa.add((i,j))
        self.knowledge.append(Sentence(set_mapa,mines))

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)

        self.mark_safe(cell)

        neighbors = set()
        for i in range(3):
            for j in range(3):
                neighbor_cell = (cell[0]+i-1,cell[1]+j-1)
                if neighbor_cell not in self.moves_made and neighbor_cell not in self.safes and (neighbor_cell[0] - (self.height - 1))*(neighbor_cell[0]) <= 0 and (neighbor_cell[1] - (self.width - 1))*(neighbor_cell[1]) <= 0:
                    if neighbor_cell in self.mines:
                        count -= 1
                    else:
                        neighbors.add(neighbor_cell)
        if Sentence(neighbors,count) not in self.knowledge and len(neighbors) > 0:
            self.knowledge.append(Sentence(neighbors,count))

        for sentence_0 in self.knowledge:
            for sentence_1 in self.knowledge:
                if sentence_0.cells.issubset(sentence_1.cells) and sentence_1.cells != sentence_0.cells:
                    sentence_1.cells -= sentence_0.cells
                    sentence_1.count -= sentence_0.count
                elif sentence_1.cells.issubset(sentence_0.cells) and sentence_0.cells != sentence_1.cells:
                    sentence_0.cells -= sentence_1.cells
                    sentence_0.count -= sentence_1.count

        loop = True
        while loop:
            loop = False
            safes_found = set()
            mines_found = set()

            for sentence in self.knowledge:
                safes_found.update(sentence.known_safes())
                mines_found.update(sentence.known_mines())

            if safes_found:
                loop = True
                for safe in safes_found:
                    self.mark_safe(safe)

            if mines_found:
                loop = True
                for mine in mines_found:
                    self.mark_mine(mine)
            MinesweeperAI.infer_generic_intersections(self)

            self.knowledge = [s for s in self.knowledge if s.cells != set()]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for s in self.knowledge:
            print(s)
        #print(self.safes)
        #print(self.mines)
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                        return (i,j)

    def infer_generic_intersections(self):
        """
        Infere minas e células seguras comparando sentenças que compartilham células em comum.
        """
        safes_to_mark = set()
        mines_to_mark = set()

        # 1. Varre o conhecimento coletando apenas tuplas (i, j) de minas e seguras
        for s1 in self.knowledge:
            # Pega seguras e minas diretas de sentenças com count == 0 ou count == len(cells)
            safes_to_mark.update(s1.known_safes())  # OBRIGATÓRIO usar os parênteses ()!
            mines_to_mark.update(s1.known_mines())  # OBRIGATÓRIO usar os parênteses ()!

            for s2 in self.knowledge:
                if s1 == s2 or len(s1.cells) == 0 or len(s2.cells) == 0:
                    continue

                common = s1.cells.intersection(s2.cells)
                if not common:
                    continue

                r1 = s1.cells - common
                r2 = s2.cells - common
                diff = s1.count - s2.count

                # Regra Genérica 1: Se diff == len(r1), R1 são minas e R2 são seguras
                if len(r1) > 0 and diff == len(r1):
                    mines_to_mark.update(r1)
                    safes_to_mark.update(r2)

                # Regra Genérica 2: Se s2.count - s1.count == len(r2), R2 são minas e R1 são seguras
                elif len(r2) > 0 and (s2.count - s1.count) == len(r2):
                    mines_to_mark.update(r2)
                    safes_to_mark.update(r1)

        # 2. Chama self.mark_safe / self.mark_mine fora dos loops
        for safe in safes_to_mark:
            if safe not in self.safes:
                self.mark_safe(safe)  # Adiciona ao self.safes e remove a tupla (i, j) das frases

        for mine in mines_to_mark:
            if mine not in self.mines:
                self.mark_mine(mine)  # Adiciona ao self.mines e limpa as frases