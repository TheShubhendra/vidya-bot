#!/usr/bin/python
# -*- coding: utf-8 -*-
# vidya - A Discord bot to play quizzes and learn with fun.
# Copyright (C) 2021 Shubhendra Kushwaha
# Email: shubhendrakushwaha94@gmail.com
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional

from aiohttp import ClientSession


class Word:
    @classmethod
    def from_dict(cls, data_dict):
        word = Word()
        word.word = data_dict.get("word")
        word.phonetic = data_dict.get("word")
        word.origin = data_dict.get("origin")
        word.meanings = data_dict.get("meanings")
        return word


class WordsAPI:
    def __init__(
        self,
        session: Optional[ClientSession] = None,
    ):
        self._base_url = "https://api.dictionaryapi.dev"
        self._end_point = "/api/v2/entries/en/"
        self._session = session

    async def fetch_word(self, word: str):
        if self._session is None:
            self._session = ClientSession()
        url = self._base_url + self._end_point + str(word)
        async with self._session.get(url) as res:
            data = await res.json()
            if type(data) == dict and data["title"] == "No Definitions Found":
                raise ValueError("No meaning found for this word")
            return Word.from_dict(data[0])
