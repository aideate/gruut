"""Language class for gruut"""
import logging
import os
import typing
from pathlib import Path

import pydash
import yaml

from gruut_ipa import Phonemes

from .phonemize import Phonemizer
from .toksen import Tokenizer
from .utils import env_constructor

# -----------------------------------------------------------------------------

_LOGGER = logging.getLogger("gruut")

_DIR = Path(__file__).parent
_DATA_DIR = _DIR / "data"

# -----------------------------------------------------------------------------


class Language:
    """Configuation, tokenizer, and phonemizer for a language"""

    def __init__(self, config, language: typing.Optional[str] = None):
        if language is None:
            self.language = pydash.get(config, "language.code")
        else:
            self.language = language

        self.config = config
        self.tokenizer = Tokenizer(config)
        self.phonemizer = Phonemizer(config)
        self.phonemes = Phonemes.from_language(self.language)

    @staticmethod
    def load(language: str) -> typing.Optional["Language"]:
        """Load language from code"""

        # Expand environment variables in string value
        yaml.SafeLoader.add_constructor("!env", env_constructor)

        # Load configuration
        config_path = _DATA_DIR / language / "language.yml"

        if not config_path.is_file():
            _LOGGER.warning("Missing %s", config_path)
            return None

        # Set environment variable for config loading
        os.environ["config_dir"] = str(config_path.parent)
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)

        return Language(config=config, language=language)