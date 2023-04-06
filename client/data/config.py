from environs import Env

env = Env()
env.read_env()

theme = env.str("stc_theme")
db_config = env.dict("connection_stc_users_postgres")

host, port = env.str("stc_client_host"), env.int("stc_port")
