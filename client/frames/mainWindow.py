from ttkbootstrap.constants import *
import ttkbootstrap as ttk


class MainWindow(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x500")


if __name__ == '__main__':
    MainWindow(title='Cinema Searcher', themename='superhero').mainloop()