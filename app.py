# базовые настройки приложения FastAPI
from fastapi import FastAPI

import middlewares
from endpounts.v1.routes import api_router as v1_router
from events import startup_event, shutdown_event
from settings import PROJECT_NAME, API_PREFIX
from versions import VersionedAPIRouterItem, mount_api_router_items

BASE_FAST_API_SETTINGS = dict(title=PROJECT_NAME, debug=False, redoc_url=None)

# элементы роутеров REST API
API_ROUTER_ITEMS = [
    VersionedAPIRouterItem(router=v1_router, settings=BASE_FAST_API_SETTINGS, prefix=API_PREFIX, version="1"),
]

API_DESCRIPTION = """
AgentKM REST API документация.

Версии:<br/>
""" + "<br/>".join(item.get_docs_link() for item in API_ROUTER_ITEMS)

# инициализация приложения FastApi
app = FastAPI(**BASE_FAST_API_SETTINGS, version="1.0", description=API_DESCRIPTION)

# ПОДКЛЮЧЕНИЕ EVENTS
# используется для определения, что сервер полностью запущен/остановлен
# используется в скриптах run_server.sh, run_tests.sh, shutdown_server.sh и др.,
# которые в свою очередь используется в GitLab CI/CD
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# подключение middlewares
middlewares.add_all_middlewares(app)

# ==================================== REST API ====================================

# подключение роутеров API
mount_api_router_items(base_app=app, description=API_DESCRIPTION, api_router_items=API_ROUTER_ITEMS)

# ==================================================================================
