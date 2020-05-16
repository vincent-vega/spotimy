#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotify.secrets import client_id, client_secret, redirect_uri
from util.utils import highlight
import base64
import requests

class Spotify:

    @staticmethod
    def get_authorize_uri() -> str:
        return f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=playlist-read-private'

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
        # TODO pagination
        return resp.json() # TODO check response is json

    @staticmethod
    def _get_tracks(tracks: dict) -> list:

        def _process_item(item: dict) -> dict:
            # TODO track_id, album, url
            return { 'artists': [ artist['name'] for artist in item['artists'] ], 'title': item['name'] }

        try:
            return [ _process_item(item['track']) for item in tracks['items'] ]
        except KeyError as e:
            print(highlight(f'Missing key {e}', color='red', bold=True))
        return []

    @staticmethod
    def list_track(access_token: str, playlist_id: str) -> (str, list):
        resp = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}',
                            headers={'Authorization': f'Bearer {access_token}'})
        data = resp.json()
        playlist_name = data['name']
        tracks = []
        try:
            data = data['tracks']
            tracks.extend(Spotify._get_tracks(data))
            while data['next']:
                nxt = data['next']
                resp = requests.get(f'{nxt}', headers={'Authorization': f'Bearer {access_token}'})
                data = resp.json()
                tracks.extend(Spotify._get_tracks(data))
        except KeyError as e:
            print(highlight(f'list_track: key {e} not found', color='red', bold=True))
        return playlist_name, tracks
