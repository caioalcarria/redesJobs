from config import message_live_start
from config import server_start
import threading

from message_live import message_live_handle

from app.main import server_client_handle





threading.Thread(target=message_live_start, args=(message_live_handle,)).start()


server_start(server_client_handle)












