import threading
import uvicorn

from . import db
from .grpc_server import serve
from .fastapi_app import app


def main():
    db.init_db()

    grpc_server = serve(port=50051)

    def stop_grpc():
        grpc_server.stop(0)

    threading.Thread(target=uvicorn.run, kwargs={
        "app": app,
        "host": "0.0.0.0",
        "port": 8000,
        "log_level": "info",
    }, daemon=True).start()

    print("FastAPI escuchando en 8000")

    try:
        grpc_server.wait_for_termination()
    except KeyboardInterrupt:
        stop_grpc()


if __name__ == "__main__":
    main()
