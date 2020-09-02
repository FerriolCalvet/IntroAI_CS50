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
        if len(self.cells) == self.count:
            return self.cells
        return set()
        # raise NotImplementedError


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()
        # raise NotImplementedError


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # should be taking the cell out of the set of cells associated with a count
        # and also substract one to the counter
        if cell in self.cells:
            self.cells.remove(cell)
            self.count += -1

        # raise NotImplementedError


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # should be taking the cell out of the set of cells associated with a count
        # and keep the counter fixed
        if cell in self.cells:
            self.cells.remove(cell)

        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

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
        # print("Before marking safe", self.safes)
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        # print("After marking safe", self.safes)


    def neighbors(self, cell, count):
        """
        This function produces a sentence based on the information
        of a newly made move.
        Looking for the unexplored neighbors and considering which ones
        are already known mines or safes.
        """
        neighbors_set = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                if (i, j) in self.moves_made:
                    continue

                if (i, j) in self.mines:
                    count -= 1 # we reduce by 1 the expected number of mines
                    continue

                if (i, j) in self.safes:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors_set.add((i,j))

        return Sentence(neighbors_set, count)



    def draw_inferences(self):
        """
        This function is used for drawing new inferences once we have
        updated the knowledge base
        """
        for sentence in self.knowledge:
            new_mines = sentence.known_mines()
            # print("new mines", new_mines)
            new_safes = sentence.known_safes()
            # print("new_safes", new_safes)

            new_mines1 = new_mines.copy()
            new_safes1 = new_safes.copy()

            if new_mines1 != set():
                for mine in new_mines1:
                    self.mark_mine(mine)

            elif new_safes1 != set():
                for safe in new_safes1:
                    self.mark_safe(safe)

        # print("inferences done")



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

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        new_sentence = self.neighbors(cell, count)
        # print("new sentence", new_sentence)
        self.knowledge.append(new_sentence)


        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        # print("Before marking safe", self.safes)
        self.draw_inferences()
        # print("After marking safe", self.safes)

        # print("round 1")
        # for sentence in self.knowledge:
        #     print(sentence.__str__())


        # Recursively process the senetnces in the knowledge base
        for ele in range(len(self.knowledge)):
            # create a copy of the knowledge base before making changes
            current_knowledge = self.knowledge.copy()


            # print("internal round")
            # for sentence in self.knowledge:
            #     print(sentence.__str__())
            # print("")

            # 5) add any new sentences to the AI's knowledge base
            # if they can be inferred from existing knowledge
            new_knowledge = set()
            filtered_sentences = []
            written_sentences = []
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    continue

                elif sentence.cells not in written_sentences:
                    filtered_sentences.append(sentence)
                    written_sentences.append(sentence.cells)

                else:
                    continue

                for sentence2 in self.knowledge:
                    if len(sentence2.cells) == 0:
                        continue

                    if sentence.cells == sentence2.cells :
                        continue

                    if sentence2.cells < sentence.cells:
                        new_sentence = Sentence(sentence.cells - sentence2.cells, sentence.count - sentence2.count)
                        if new_sentence.cells not in written_sentences:
                            filtered_sentences.append(new_sentence)
                            written_sentences.append(new_sentence.cells)

            if filtered_sentences == current_knowledge:
                break

            self.knowledge = filtered_sentences

            # We try to make new inferences from the updated knowledge base
            # print("Before marking safe2", self.safes)
            self.draw_inferences()
            # print("After marking safe2", self.safes)




        # print("round 2")
        # for sentence in self.knowledge:
        #     print(sentence.__str__())
        #
        # print("\n")

        # raise NotImplementedError



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) > 0:
            return safe_moves.pop()
        return None

        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = set()
        for i in range(self.height):
            for j in range(self.width):
                all_cells.add((i,j))

        possible_moves = all_cells - self.moves_made
        possible_moves = possible_moves - self.mines

        if len(possible_moves) > 0:
            return possible_moves.pop()
        return None



        # raise NotImplementedError
