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
from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, nullable=False)
    discord_username = Column(String(100), nullable=False)
    score = Column(Integer, default=0)


class Command(Base):
    __tablename__ = "commands"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    command_name = Column(String(10), primary_key=True, nullable=False)
    count = Column(Integer, default=0)
