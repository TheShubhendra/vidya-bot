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
from base64 import decodebytes
from typing import Dict, Union

from aiohttp import ClientSession


class OpenTDBQuiz:
    @property
    def options(self) -> list:
        return self.incorrect + [self.correct]

    def check(self, answer: str) -> bool:
        return self.correct == answer

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Union[str, list]]):
        def decode(b):
            return decodebytes(b.encode()).decode()

        obj = OpenTDBQuiz()
        setattr(obj, "correct", decode(data_dict.pop("correct_answer")))
        setattr(
            obj,
            "incorrect",
            list(
                map(
                    decode,
                    data_dict.pop("incorrect_answers"),
                )
            ),
        )
        for i, j in data_dict.items():
            setattr(obj, i, decode(j))
        return obj


class OpenTDB:
    def __init__(
        self,
    ):
        """Opentdp Api handler."""
        self._endpoint = "https://opentdb.com"
        self.session = None

    async def _create_session(self):
        self.session = ClientSession()

    async def fetch(
        self,
        amount: int = 1,
        params: dict = {},  # pylint: disable=W0102
        encoding="base64",
    ):
        params["encode"] = encoding
        if self.session is None:
            await self._create_session()
        async with self.session.get(
            self._endpoint + f"/api.php?amount={amount}",
            params=params,
        ) as req:
            res = await req.json()
            return [OpenTDBQuiz.from_dict(quiz) for quiz in res["results"]]
