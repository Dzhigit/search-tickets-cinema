from environs import Env

env = Env()
env.read_env()

db_config = env.dict("connection_stc_users_postgres")
host, port = env("stc_server_host"), env.int("stc_port")
smtp_login, smtp_password = env.str("smtp_login"), env.str("smtp_password")
