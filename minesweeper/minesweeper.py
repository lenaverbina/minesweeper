import tkinter as tk
import random
import numpy as np

def validate_board(n, bombs):
    if n < 1 or bombs < 1:
        return 1
    elif bombs >= n**2:
        return 1
    else:
        return 0

def make_game_board(n):
    list_of_lists = [[0 for _ in range(n)] for _ in range(n)]
    return list_of_lists

def get_bombs(num, n):
    bombs_indexes = []
    while len(bombs_indexes) < num:
        r = random.randint(0, n-1)
        c = random.randint(0, n-1)
        bombs_indexes.append((r, c))
        bombs_indexes = list(set(bombs_indexes))
    return bombs_indexes

class StartMenu:
    def __init__(self, root):
        self.root = root
        self.button = tk.Button(text="Начать игру", command=self.click)
        self.button.grid(row=0, column=0, columnspan=2)
        self.label = tk.Label(text="Площадь")
        self.label.grid(row=1, column=0, columnspan=1)
        self.inputtxt = tk.Text(self.root, height=1, width=5)
        self.inputtxt.grid(row=1, column=1, columnspan=1)
        self.label1 = tk.Label(text="Количество бомб")
        self.label1.grid(row=2, column=0, columnspan=1)
        self.inputtxt1 = tk.Text(self.root, height=1, width=5)
        self.inputtxt1.grid(row=2, column=1, columnspan=1)

    def click(self):
        try:
            n = int(self.inputtxt.get("1.0", "end"))
            bombs = int(self.inputtxt1.get("1.0", "end"))
            valid = validate_board(n, bombs)
            if valid == 1:
                self.error_label = tk.Label(text="Введите верные значения")
                self.error_label.grid(row=3, column=0, columnspan=1)
            else:
                for child in root.winfo_children():
                    child.destroy()
                app = MainApplication(root, n, bombs)
                app.create_board()
                root.mainloop()
        except ValueError:
            self.error_label = tk.Label(text="Введите верные значения")
            self.error_label.grid(row=3, column=0, columnspan=1)

def exit_to_main_menu():
    for child in root.winfo_children():
        child.destroy()
    start = StartMenu(root)
    root.mainloop()

class MainApplication:
    def __init__(self, root, n, num_bombs):
        self.root = root
        #self.n = int(input())
        self.n = n
        self.num_bombs = num_bombs
        self.lbl = tk.Label(text="Играем в сапера")
        self.lbl.grid(row=self.n+1, column=0, columnspan=self.n)
        self.pc_butt = tk.Button(self.root, text="Режим флажка", command=self.flag)
        self.pc_butt.grid(row=self.n+2, column=0, columnspan=self.n)
        self.exit_btn = tk.Button(self.root, text="Выйти в главное меню", command=exit_to_main_menu)
        self.exit_btn.grid(row=0, column=0, columnspan=self.n)
        self.game_matrix = make_game_board(self.n)
        self.bts = {}
        self.click_count = 0
        self.bombs = False
        self.end_game = False
        self.flag_state = False
        self.bombs_list = []
        self.num_flags = 0

    def flag(self):
        self.flag_state = True
        print('puk')
        self.pc_butt.config(text="Игровой режим", command=self.game_mode)
        #print(self.game_matrix)

    def game_mode(self):
        self.flag_state = False
        print('puk_puk')
        self.pc_butt.config(text="Режим флажка", command=self.flag)

    def create_board(self):
        self.bts = {}
        for c in range(self.n):
            self.root.columnconfigure(index=c, weight=1)
        for r in range(self.n):
            self.root.rowconfigure(index=r+1, weight=1)

        for r in range(self.n):
            for c in range(self.n):
                btn = tk.Button(text="")
                btn.configure(command=lambda name=str(btn): self.click(name))
                btn.grid(ipadx=10, ipady=6, row=r+1, column=c)
                self.bts[str(btn)] = btn

    def click(self, name):
        if not self.end_game:
            button = self.bts[name]
            row = button.grid_info()['row']  # Row of the button
            column = button.grid_info()['column']
            if self.flag_state:
                if not self.bombs_list:
                    label = tk.Label(text="Игра еще не начата")
                    label.grid(row=self.n + 3, column=0, columnspan=self.n)
                else:
                    if button['text'] == '>':
                        button.config(text='')
                        self.num_flags -= 1
                    elif button['text'] != '>':
                        button.config(text='>')
                        self.num_flags += 1
                print(self.num_flags)
            else:
                if button['text'] == '>':
                    button.config(state='disabled')
                else:
                    while not self.bombs:
                        self.bombs_list = get_bombs(self.num_bombs, self.n)
                        #if i != row-1 and j != column:
                        if (row - 1, column) not in self.bombs_list:
                            for bomb_tuple in self.bombs_list:
                                self.game_matrix[bomb_tuple[0]][bomb_tuple[1]] = '*'
                                self.bombs = True
                                for k in range(self.n):
                                    for l in range(self.n):
                                        if (bomb_tuple[0] - 1 <= k <= bomb_tuple[0] + 1 and
                                                bomb_tuple[1] - 1 <= l <= bomb_tuple[1] + 1 and
                                                self.game_matrix[k][l] != '*'):
                                            self.game_matrix[k][l] += 1
                        else:
                            continue
                    if button['state'] != 'disabled':
                        self.click_count += 1
                    button.config(state='disabled')
                    if self.bombs and self.game_matrix[row-1][column] == '*':
                        self.lbl.config(text="Вы проиграли")
                        self.end_game = True
                    elif self.click_count == self.n**2 - self.num_bombs:
                        print('puk')
                        self.lbl.config(text="Вы выиграли")
                        self.end_game = True
                    #print(self.click_count)
                    #print(self.game_matrix)
                    button.config(text=str(self.game_matrix[row-1][column]))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    startapp = StartMenu(root)
    root.mainloop()
    list_bombs = get_bombs(3, 5)
    print(list_bombs)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
