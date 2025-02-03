import tkinter as tk
import random


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.lbl = tk.Label(text="Играем в сапера")
        self.lbl.grid(row=4, column=0, columnspan=3)
        self.pc_butt = tk.Button(self.root, text="Начать новую игру", command=self.init_game)
        self.pc_butt.grid(row=0, column=0, columnspan=3)
        self.game_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.bts = {}
        self.click_count = 0
        self.bombs = False
        self.end_game = False

    def init_game(self):
        self.end_game = False
        self.lbl.config(text="Играем в сапера")
        self.game_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.bombs = False
        self.click_count = 0
        for name in self.bts:
            button = self.bts[name]
            r = button.grid_info()['row']  # Row of the button
            c = button.grid_info()['column']
            button.config(text=f"({r-1},{c})")

    def create_board(self):
        self.bts = {}
        for c in range(3):
            self.root.columnconfigure(index=c, weight=1)
        for r in range(3):
            self.root.rowconfigure(index=r+1, weight=1)

        for r in range(3):
            for c in range(3):
                btn = tk.Button(text=f"({r},{c})")
                btn.configure(command=lambda name=str(btn): self.click(name))
                #print(str(btn))
                #self.bts.append(btn)
                btn.grid(row=r+1, column=c)
                #print(btn)
                self.bts[str(btn)] = btn
        print(self.bts)

    def click(self, name):
        if not self.end_game:
            button = self.bts[name]
            row = button.grid_info()['row']  # Row of the button
            column = button.grid_info()['column']
            while not self.bombs:
                i = random.randrange(3)
                j = random.randrange(3)
                if i != row-1 and j != column:
                    self.game_matrix[i][j] = '*'
                    self.bombs = True
                else:
                    continue
                for k in range(len(self.game_matrix)):
                    for l in range(len(self.game_matrix[k])):
                        if i - 1 <= k <= i + 1 and j - 1 <= l <= j + 1 and self.game_matrix[k][l] == 0:
                            self.game_matrix[k][l] = 1
            self.click_count += 1
            if self.bombs and self.game_matrix[row-1][column] == '*':
                self.lbl.config(text="Вы проиграли")
                self.end_game = True
            elif self.click_count == 8:
                print('puk')
                self.lbl.config(text="Вы выиграли")
                self.end_game = True
            print(self.click_count)
            print(self.game_matrix)
            button.config(text=str(self.game_matrix[row-1][column]))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    app = MainApplication(root)
    app.create_board()
    root.mainloop()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
