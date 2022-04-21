import os

from channels.auth import AuthMiddlewareStack #추가
from channels.routing import ProtocolTypeRouter, URLRouter #URLRouter 추가
from django.core.asgi import get_asgi_application
import voicebot.routing # chat import

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiplay.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack( # 추가
        URLRouter(
            voicebot.routing.websocket_urlpatterns
        )
    ),
})