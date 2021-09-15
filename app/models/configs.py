from environs import Env

env = Env()
env.read_env()

configs = {
    'host': env('HOST'),
    'database': env('DATABASE'),
    'user': env('USER'),
    'password': env('PASSWORD')
}
