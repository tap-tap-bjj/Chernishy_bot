from dataclasses import dataclass
from environs import Env

@dataclass
class TokenConfig:
    bot_token_srv: str
    chat_id: str
    captcha_token: str


@dataclass
class SRV:
    login: str
    password: str

@dataclass
class Config:
    token: TokenConfig
    srv: SRV

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        token=TokenConfig(
            bot_token_srv=env.str("BOT_TOKEN_SRV"),
            chat_id=env.str("CHAT_ID"),
            captcha_token=env.str("CAPTCHA_TOKEN")
        ),
        srv=SRV(
            login=env.str("LOGIN_SRV"),
            password=env.str("PASSWORD_SRV")
        )
    )
