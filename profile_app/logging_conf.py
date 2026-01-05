from logging.config import dictConfig

from profile_app.config import DevConfig, config

def configure_logging():
    """
    Configure logging based on the current configuration.
    In development, set log level to DEBUG for more verbosity.
    In production, use WARNING level to reduce log noise.
    """
    log_level = "DEBUG" if isinstance(config, DevConfig) else "WARNING"
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
                "format": "%(name)s:%(lineno)d - %(message)s"

            },
            "file": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
                "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "class": "rich.logging.RichHandler",
                "formatter": "console",
                "level": log_level,
            },
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "file",
                "filename": "logs/profile_app.log",
                "maxBytes": 1024 * 1024,  # 1MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
            "profile_app": {
                "handlers": ["default", "rotating_file"],
                "level": log_level,
                "propagate": False,
            },
            "database": {"handlers": ["default"], "level": log_level},
        },
    }

    # Apply the configuration
    dictConfig(logging_config)