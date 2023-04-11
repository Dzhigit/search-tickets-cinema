from ttkbootstrap.constants import *
import ttkbootstrap as ttk

from client.API.scrolled_widgets.xScrolledFrame import XScrolledFrame
from client.API.server_handler.constants import *

import webbrowser


class MainFrame(ttk.Frame):
    def __init__(self, parent, connection, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry("900x600")
        self.parent.resizable(TRUE, TRUE)
        self.connection = connection
        self.films = None

        ttk.Label(self, text="Enter movie title").pack()
        self.search = ttk.StringVar(value='')
        self.create_from_search(self.search)

        ttk.Label(self, text="Select found movie").pack()
        self.combo_box = ttk.Combobox(self, width=40)
        self.combo_box.pack(pady=5)
        btn_get = ttk.Button(self, text='get', command=self._get_film_info)
        btn_get.pack()

        ttk.Label(self, text="Movie information").pack()
        self.info_frame = XScrolledFrame(self)
        self.info_frame.pack(fill=X, pady=5, expand=TRUE)

    def create_from_search(self, variable):
        container = ttk.Frame(self)
        container.pack(fill=X, pady=5)

        ttk.Label(container, text='Name:').pack(side=LEFT, padx=5)
        entry = ttk.Entry(container, width=25, textvariable=variable)
        entry.bind('<Return>', self._get_film_names)
        entry.pack(side=LEFT, padx=5)
        ttk.Button(container, text='search', command=self._get_film_names).pack(side=LEFT)

    def _get_film_names(self):
        self.connection.send_data(
            type=FILM_NAMES,
            film_name=self.search.get()
        )
        title = []
        print(self.search.get())
        self.films = self.connection.listen_server()['films']
        print(self.films)
        for film in self.films:
            title.append(film)
        self.combo_box.config(values=title)

    def _get_film_info(self):
        name = self.combo_box.get()
        if len(self.info_frame.interior.pack_slaves()) > 0:
            for i in self.info_frame.interior.pack_slaves():
                i.destroy()
        if len(name) > 0:
            info = self.films[name]
            print(info)

            web_url = 'URL: ' + str(info['webUrl'])
            year = 'Year: ' + str(info['year'])
            description = 'Description: ' + str(info['description'])
            premiere_world_country = 'Premiere world country: ' + str(info['premierWorldCountry'])
            genres = 'Genres: ' + ', '.join([i for i in info['genres']])
            kp_rare = 'Rating: ' + str(info['kp_rate'])

            ttk.Label(self.info_frame.interior, text=name, justify=LEFT).pack(fill=X)
            ttk.Label(self.info_frame.interior, text=description, justify=LEFT).pack(fill=X)
            ttk.Label(self.info_frame.interior, text=premiere_world_country, justify=LEFT).pack(fill=X)
            ttk.Label(self.info_frame.interior, text=genres, justify=LEFT).pack(fill=X)
            ttk.Label(self.info_frame.interior, text=year, justify=LEFT).pack(fill=X)
            ttk.Label(self.info_frame.interior, text=kp_rare, justify=LEFT).pack(fill=X)
            ttk.Label(self.info_frame.interior, text=web_url, bootstyle=INFO, cursor='hand2', justify=LEFT)
            print(web_url)
            Link(
                self.info_frame.interior,
                web_url,
                text=web_url,
                bootstyle=INFO,
                cursor='hand2',
                justify=LEFT,
            ).pack(fill=X)


class Link(ttk.Label):
    def __init__(self, parent, url, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.url = url
        self.bind('<Button-1>', self.open_url)

    def open_url(self, event):
        webbrowser.open_new_tab(self.url)
