import os
import uvicorn
import logging

logging_level = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=logging_level,
    datefmt="%Y-%m-%dT%H:%M",
    format="[%(asctime)s.%(msecs)03dZ]: %(levelname)s: [%(module)s - L%(lineno)d] %(message)s",
)

LOGGER = logging.getLogger("redis_mq")

# Add uvicorn error handler
format_string = "[%(asctime)s.%(msecs)03dZ]:  - %(levelname)s - %(message)s"
log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = format_string
log_config["formatters"]["default"]["fmt"] = format_string
LOGGER.addHandler(log_config)

# Handle logging for the docker container
logger = logging.getLogger("uvicorn.access")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(handler)
