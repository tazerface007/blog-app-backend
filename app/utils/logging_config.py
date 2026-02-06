import logging.config
import os

def setup_logging(app_config):
    log_dir = 'instance/logs'
    os.makedirs(log_dir, exist_ok=True)
    logging_config =  {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG' if app_config.DEBUG else 'INFO',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir,'app.log'),
                'maxBytes': 5 * 1024 * 1024, # 5MB per file
                'backupCount': 5,
                'formatter': 'standard',
                'level': 'INFO',
                'encoding': 'utf-8'
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
    logging.config.dictConfig(logging_config)