"""The hass_ytdlp component."""
import logging
import os
import re
import time

import voluptuous as vol

from homeassistant.const import CONF_FILE_PATH
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from yt_dlp import YoutubeDL

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class YTDLP:
    """Service class."""

    hass: HomeAssistant
    downloads: dict
    path: str

    def __init__(self, hass: HomeAssistant, path: str) -> None:
        """Initialize the YTDLP class.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            path (str): The path for storing downloaded videos.
        """
        self.hass = hass
        self.downloads = {}
        self.path = path

    async def download(self, call: ServiceCall):
        """Download a video."""
        hook = DLP_Hook(self)
        # logger = DLP_Logger(self.downloads, hook.id)
        ydl_opts = {
            "progress_hooks": [hook.progress_hook],
            "paths": {
                "home": self.path,
                "temp": "temp",
            },
        }
        for k, v in call.data.items():
            if k not in ["url", "progress_hooks", "paths"]:
                ydl_opts[k] = v
        with YoutubeDL(ydl_opts) as ydl:
            self.hass.async_add_executor_job(ydl.download, [call.data["url"]])
            # ydl.download([call.data["url"]])

    def update_state(self):
        """Update the state of the entity."""
        attr = {}
        for _, v in self.downloads.items():
            try:
                attr[v["filename"]] = {
                    "speed": v["speed"],
                    "downloaded": v["downloaded"],
                    "total": v["total"],
                    "eta": v["eta"],
                }
            except KeyError as e:
                _LOGGER.info(e)
        self.hass.states.set("%s.downloading" % DOMAIN, len(attr), attr)


class DLP_Hook:
    """Class for handling download progress and logging."""

    id: str
    dlp: YTDLP
    t: float

    def __init__(self, dlp: YTDLP) -> None:
        """Initialize the DLP_Hook class.

        Args:
            dlp (YTDLP): YTDLP service class.
        """
        self.id = str(time.time_ns())
        self.dlp = dlp
        self.dlp.downloads[self.id] = {}
        self.t = time.time()

    def progress_hook(self, d):
        """Update download progress."""
        if d["status"] == "finished":
            self.dlp.downloads.pop(self.id, None)
            self.dlp.update_state()
            _LOGGER.info("download finished")
        if d["status"] == "downloading":
            self.dlp.downloads[self.id] = {}
            self.dlp.downloads[self.id]["status"] = "downloading"
            self.dlp.downloads[self.id]["filename"] = d["info_dict"]["filename"].split("/")[-1]
            try:
                self.dlp.downloads[self.id]["speed"] = d["speed"]
            except KeyError as e:
                _LOGGER.warning(e)
            try:
                self.dlp.downloads[self.id]["downloaded"] = d["downloaded_bytes"]
            except KeyError as e:
                _LOGGER.warning(e)
            try:
                self.dlp.downloads[self.id]["total"] = d["total_bytes"]
            except KeyError as e:
                self.dlp.downloads[self.id]["total"] = "Nan"
                _LOGGER.warning(e)
            try:
                self.dlp.downloads[self.id]["eta"] = d["eta"]
            except KeyError as e:
                _LOGGER.warning(e)
            self.dlp.update_state()
        if d["status"] == "error":
            self.dlp.downloads.pop(self.id, None)
            self.dlp.update_state()
            _LOGGER.error("download error")


async def async_setup_entry(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the hass_ytdlp component."""
    # TODO: Add your setup code here
    hass.states.async_set("%s.downloading" % DOMAIN, "0")
    # _LOGGER.info("Download path: " + config.data[CONF_FILE_PATH])
    if not os.path.isdir(config.data[CONF_FILE_PATH]):
        os.mkdir(config.data[CONF_FILE_PATH], 0o755)

    dlp = YTDLP(hass, config.data[CONF_FILE_PATH])

    hass.services.async_register(
        DOMAIN,
        "download",
        dlp.download,
        schema=vol.Schema({vol.Required("url"): cv.url}),
    )

    return True
