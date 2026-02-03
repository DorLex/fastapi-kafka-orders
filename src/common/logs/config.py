from logging.config import dictConfig

LOGGING_CONFIG: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            'format': '[{asctime}] |{levelname}| ({name}.{funcName}:{lineno}): {message}',
            'style': '{',  # использовать в 'format' вместо %
        },
    },
    'handlers': {
        'console': {
            'formatter': 'custom',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {  # базовый logger
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'uvicorn': {  # uvicorn.access и uvicorn.error
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'sqlalchemy': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


def setup_logging() -> None:
    dictConfig(LOGGING_CONFIG)
