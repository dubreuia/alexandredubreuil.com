import threading
import webbrowser

from eventlet import wsgi
import eventlet
import socketio
import tensorflow as tf

from constants import WS_SERVER_HOST, WS_SERVER_PORT
from type import ActionType


class ActionServer(threading.Thread):

  def __init__(self,
               host: str = WS_SERVER_HOST,
               port: int = WS_SERVER_PORT):
    super(ActionServer, self).__init__()
    self.context = {}
    self._host = host
    self._port = port
    self._socket = socketio.Server()
    self._app = socketio.WSGIApp(self._socket, static_files={
      '/': 'app.html',
      '/static/js/jquery': 'node_modules/jquery/dist',
      '/static/js/socket.io': 'node_modules/socket.io-client/dist',
      '/output/models/drums': 'output/models/drums.html',
      '/output/models/melody': 'output/models/melody.html',
      '/output/models/bass': 'output/models/bass.html',
    })
    namespace = ServerNamespace('/', self.context, self._socket)
    self._socket.register_namespace(namespace)

  def run(self):
    wsgi.server(eventlet.listen((self._host, self._port)), self._app,
                log=None, log_output=False)
    webbrowser.open(f"http://{self._host}:{self._port}", new=2)

  def stop(self):
    eventlet.wsgi.is_accepting = False
    del self._socket
    del self._app

class ServerNamespace(socketio.Namespace):

  def __init__(self, namespace, context, socket):
    super(ServerNamespace, self).__init__(namespace)
    self.context = context
    self.socket = socket

  def on_connect(self, sid, environ):
    tf.logging.debug(f"Client {sid} with {environ} connected")

  def on_disconnect(self, sid):
    tf.logging.debug(f"Client {sid} disconnected")

  def on_model(self, sid, data):
    tf.logging.info(f"On model {data} as {sid}")
    model, value = data["model"], data["value"]
    try:
      value = ActionType[value.upper()]
    except KeyError:
      raise Exception(f"Unknown action {value}")
    self.context[model] = value
