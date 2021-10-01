#!/usr/bin/bash
export DATABASE_URL=${DATABASE_URL/"postgres"/"postgresql+asyncpg"}
python -m vidya