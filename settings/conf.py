from decouple import config 


SECRET_KEY = config("MOVIENIGHT_SECRET_KEY", cast=str)
ENV_ID = config("MOVIENIGHT_ENV_ID", cast=str)