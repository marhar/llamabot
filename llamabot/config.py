"""Paths to configuration files and directories."""
from pathlib import Path

llamabotrc_paths = [Path.home() / ".llamabotrc", Path.home() / ".llamabot/.llamabotrc"]

llamabot_config_dir = Path.home() / ".llamabot"