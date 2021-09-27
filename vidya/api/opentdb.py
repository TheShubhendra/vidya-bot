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
        self._endpoint = "https://opentdb.com"
        self.session = None

    async def _create_session(self):
        self.session = ClientSession()

    async def fetch(
        self,
        amount: int = 1,
        params: dict = {},
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
