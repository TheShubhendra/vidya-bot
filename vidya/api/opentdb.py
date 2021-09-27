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
        obj = OpenTDBQuiz()
        setattr(obj, "correct", data_dict.pop("correct_answer"))
        setattr(obj, "incorrect", data_dict.pop("incorrect_answers"))
        for i, j in data_dict.items():
            setattr(obj, i, j)
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
    ):
        if self.session is None:
            await self._create_session()
        async with self.session.get(
            self._endpoint + f"/api.php?amount={amount}", params=params
        ) as req:
            res = await req.json()
            return [OpenTDBQuiz.from_dict(quiz) for quiz in res["results"]]
