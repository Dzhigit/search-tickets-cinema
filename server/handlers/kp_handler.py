from KinoPoiskAPI.kinopoisk_api import KP


class KPHandler(KP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_film_info(film):
        info = {
            'webUrl': film.kp_url,
            'year': film.year,
            'description': film.description,
            'genres': film.genres,
            'premierWorldCountry': film.premiere_world_country,
            'kp_rate': film.kp_rate
        }

        return info

    def get_films_info(self, films: list):
        films_info = {}
        for film in films:
            films_info[film.name + ' | ' + film.ru_name] = self._get_film_info(
                self.get_film(film.kp_id)
            )

        return films_info



