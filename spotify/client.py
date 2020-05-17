#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotify.secrets import client_id, client_secret, redirect_uri
from util.utils import highlight
import base64
import requests

class Spotify:

    @staticmethod
    def get_authorize_uri() -> str:
        scope = '%20'.join([ 'playlist-read-private', 'user-library-read' ])
        return f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}'

    @staticmethod
    def token(code: str) -> dict:
        b64auth = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf-8')).decode('utf-8')
        resp = requests.post(f'https://accounts.spotify.com/api/token',
                             data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri},
                             headers={'Authorization': f'Basic {b64auth}'})
        # TODO error handling
        return resp.json()

    @staticmethod
    def list_playlists(access_token: str) -> dict:
        resp = requests.get(f'https://api.spotify.com/v1/me/playlists',
                            headers={'Authorization': f'Bearer {access_token}'})
        # TODO check response is json
        playlists = resp.json()
        try:
            data = resp.json()
            while data['next']:
                nxt = data['next']
                resp = requests.get(f'{nxt}', headers={'Authorization': f'Bearer {access_token}'})
                data = resp.json()
                playlists['items'].extend(data['items'])
        except KeyError as e:
            print(highlight(f'list_playlists: key {e} not found', color='red', bold=True))
        return playlists

    @staticmethod
    def playlist_info(access_token: str, playlist_id: str) -> dict:
        resp = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}',
                            headers={'Authorization': f'Bearer {access_token}'})
        tracks = resp.json()
        try:
            data = resp.json()['tracks']
            while data['next']:
                nxt = data['next']
                resp = requests.get(f'{nxt}', headers={'Authorization': f'Bearer {access_token}'})
                data = resp.json()
                tracks['tracks']['items'].extend(data['items'])
        except KeyError as e:
            print(highlight(f'playlist_info: key {e} not found', color='red', bold=True))
        return tracks

    @staticmethod
    def saved_tracks(access_token: str) -> dict:
        resp = requests.get(f'https://api.spotify.com/v1/me/tracks',
                            headers={'Authorization': f'Bearer {access_token}'})
        tracks = resp.json()
        try:
            data = resp.json()
            while data['next']:
                nxt = data['next']
                resp = requests.get(f'{nxt}', headers={'Authorization': f'Bearer {access_token}'})
                data = resp.json()
                tracks['items'].extend(data['items'])
        except KeyError as e:
            print(highlight(f'saved_tracks: key {e} not found', color='red', bold=True))
        return tracks
