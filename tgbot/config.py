from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list | int


@dataclass
class DbClient:
    database: str
    user: str
    password: str
    host: str
    port: int = 5432


@dataclass
class Config:
    tg: TgBot
    db: DbClient


def load_config(path: str = '.env'):
    env = Env()
    env.read_env(path)
    return Config(
        tg=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=DbClient(
            database=env.str('DB_BASE'),
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT')
        )
    )
