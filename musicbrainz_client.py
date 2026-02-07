import requests
import time

class MusicBrainzClient:
    BASE_URL = "https://musicbrainz.org/ws/2"
    USER_AGENT = "GigDexApp/1.0.0 ( anderson@example.com )" # Recomendado pela MusicBrainz

    def __init__(self):
        self.headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "application/json"
        }

    def search_artist(self, artist_name: str):
        """Busca um artista pelo nome e retorna o MBID e gênero principal."""
        params = {
            "query": artist_name,
            "fmt": "json",
            "limit": 1
        }
        try:
            response = requests.get(f"{self.BASE_URL}/artist", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data.get("artists"):
                artist = data["artists"][0]
                # Tenta pegar o gênero das tags
                genres = [tag["name"] for tag in artist.get("tags", [])]
                main_genre = genres[0] if genres else "Unknown"
                
                return {
                    "mbid": artist["id"],
                    "name": artist["name"],
                    "genre": main_genre
                }
            return None
        except Exception as e:
            print(f"Erro ao buscar artista {artist_name}: {e}")
            return None
        finally:
            # Respeitar o limite de taxa da MusicBrainz (1 req/s)
            time.sleep(1)

    def get_artist_image(self, mbid: str):
        """
        MusicBrainz não hospeda imagens diretamente. 
        Poderíamos usar a Cover Art Archive se quiséssemos capas de álbuns,
        ou uma API como Fanart.tv ou Spotify. 
        Para simplificar, retornaremos um placeholder ou usaremos o MBID para linkar futuramente.
        """
        return f"https://www.gravatar.com/avatar/{mbid}?d=identicon&s=200"
