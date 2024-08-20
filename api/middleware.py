import json
import logging
import time

import logstash
from fastapi import Response
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware


class LogstashMiddleware(BaseHTTPMiddleware):
    configured_logger = False

    def configure_logger(self):
        print("Configuring logger")
        self.logger = logging.getLogger("python-logstash-logger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(
            logstash.TCPLogstashHandler("localhost", 50000, version=1)
        )

    async def dispatch(self, request, call_next):
        if not self.configured_logger:
            self.configure_logger()
            self.configured_logger = True
        start_time = time.time()
        request_body = await request.body()
        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:  # type: ignore
            response_body += chunk

        try:
            request_json = json.loads(request_body.decode())
        except json.JSONDecodeError:
            request_json = {}  # Handle the case where the request body isn't JSON

        process_time = time.time() - start_time
        log_data = {
            "latency": process_time,
            "request": request_body.decode(),
            "tag": request_json.get("tag", "unknown"),
            "method": request.method,
            "response": response_body.decode(),
        }

        task = BackgroundTask(self._log_info, log_data)

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=task,
        )

    # Logger configurations
    def _log_info(self, log_data):
        self.logger.info("Log Data", extra=log_data)
