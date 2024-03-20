from celery.utils.nodenames import gethostname

PRODUCTION_SERVERS = ['rn-loyality']
DEV_SERVERS = ['rn-loyality-dev']


def is_production() -> bool:
    """Приложение запущено на production сервере"""
    return gethostname().lower() in PRODUCTION_SERVERS


def is_dev() -> bool:
    """Приложение запущено на тестовом сервере"""
    return gethostname().lower() in DEV_SERVERS


def is_local_dev() -> bool:
    """Приложение запущено на локальной машине"""
    return not is_production() and not is_dev()
