import aiohttp
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import aiosqlite

# Настройка Spotify API
CLIENT_ID = '64275eec6da4443ca19e3ab0b5e20ed1'
CLIENT_SECRET = 'e31e6bf612cf43c0943fa20ca093f24c'

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


# Функция для получения токена доступа
def get_access_token():
    token_info = auth_manager.get_access_token(as_dict=False)
    return token_info


# Создание таблиц и базы данных
async def create_tables():
    async with aiosqlite.connect('spotify_data.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS artists (
                                id TEXT PRIMARY KEY,
                                name TEXT NOT NULL
                            )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS tracks (
                                id TEXT PRIMARY KEY,
                                name TEXT NOT NULL,
                                album TEXT,
                                popularity INTEGER,
                                duration_ms INTEGER,
                                artist_id TEXT,
                                FOREIGN KEY (artist_id) REFERENCES artists (id)
                            )''')
        await db.commit()


# Функция для добавления исполнителя
async def add_artist(db, artist_id, name):
    await db.execute('INSERT OR IGNORE INTO artists (id, name) VALUES (?, ?)', (artist_id, name))
    await db.commit()


# Функция для добавления трека
async def add_track(db, track):
    await db.execute('''INSERT OR IGNORE INTO tracks (id, name, album, popularity, duration_ms, artist_id)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (track['id'], track['name'], track['album']['name'], track['popularity'],
                      track['duration_ms'], track['artists'][0]['id']))
    await db.commit()


# Асинхронная функция для получения треков
async def fetch_tracks(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.json()


# Основная функция для получения информации о треках и исполнителях
async def get_tracks_and_artists():
    limit = 50  # Количество элементов за один запрос
    offset = 0  # Начальное смещение
    async with aiosqlite.connect('spotify_data.db') as db, aiohttp.ClientSession() as session:
        while True:
            url = f"https://api.spotify.com/v1/browse/new-releases?limit={limit}&offset={offset}"
            headers = {"Authorization": f"Bearer {get_access_token()}"}
            response_json = await fetch_tracks(session, url, headers)

            if 'albums' not in response_json:
                print(f"Unexpected response format: {response_json}")
                break

            items = response_json['albums']['items']

            if not items:
                break  # Если данных больше нет, выходим из цикла

            for item in items:
                album_tracks = sp.album_tracks(item['id'])['items']
                for track in album_tracks:
                    track_id = track['id']
                    track_details = sp.track(track_id)

                    artist_id = track_details['artists'][0]['id']
                    artist_name = track_details['artists'][0]['name']

                    await add_artist(db, artist_id, artist_name)
                    await add_track(db, track_details)

            offset += limit  # Увеличиваем смещение для следующего запроса


# Запуск создания таблиц и парсинга
async def main():
    await create_tables()
    await get_tracks_and_artists()


asyncio.run(main())

print('Парсинг завершен')
