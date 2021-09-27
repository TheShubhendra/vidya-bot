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
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from .models import Base, Command, Student


class DatabaseManager:
    def __init__(
        self,
        database_url: str,
    ):
        self.database_url = database_url
        self.engine = create_async_engine(
            database_url,
        )
        self.session_factory = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.session = async_scoped_session(
            self.session_factory,
            scopefunc=current_task,
        )
        self.base = Base

    async def add_student(
        self,
        discord_id: int,
        discord_username: str,
    ) -> None:
        student = Student(
            discord_id=discord_id,
            discord_username=discord_username,
        )
        self.session.add(student)
        await self.session.commit()

    async def get_student(self, discord_id: int) -> Student:
        stmt = select(Student).where(Student.discord_id == discord_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def record_command(
        self,
        student_id: int,
        command_name: str,
    ) -> None:
        result = await self.session.execute(
            select(Command)
            .where(Command.user_id == student_id)
            .where(Command.command_name == command_name)
        )
        record = result.scalar_one_or_none()
        if record is None:
            record = Command(
                command_name=command_name,
                user_id=student_id,
                count=0,
            )
            self.session.add(record)
        record.count = record.count + 1
        await self.session.commit()

    async def update_score(
        self,
        student: Student,
        score_change: int,
    ) -> None:
        student.score += score_change
        await self.session.commit()
