
from src.i18n.i18n import I18nAuto

i18n = I18nAuto()

import structlog

logger = structlog.get_logger()

from app.abus_config import azure_translator_available

genuine_init_called = False


def genuine_init():
    global genuine_init_called
    genuine_init_called = True


def azure_text_api_working() -> bool:
    """Check if Azure Translator API is available via environment variable."""
    return azure_translator_available()


def azure_text_api_info() -> str:
    """Return info about Azure API usage."""
    if azure_text_api_working():
        logger.debug(
            "[abus_genuine.py] azure_text_api_info - Using Azure Translator API"
        )
    else:
        logger.debug("[abus_genuine.py] azure_text_api_info - Using the free API")
    return ""
