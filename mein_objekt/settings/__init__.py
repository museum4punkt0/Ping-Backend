import environ

env = environ.Env()
base_env = environ.Path(__file__) - 3
env.read_env(env_file=base_env('.env'))
environment = env('ENVIRONMENT')

if environment == 'local':
    try:
        from .local import *
    except ImportError as e:
        raise ImportError(e)

elif environment == 'test':
    try:
        from .test import *
    except ImportError as e:
        raise ImportError(e)

elif environment == 'qa':
    try:
        from .qa import *
    except ImportError as e:
        raise ImportError(e)

elif environment == 'production':
    try:
        from .production import *
    except ImportError as e:
        raise ImportError(e)
