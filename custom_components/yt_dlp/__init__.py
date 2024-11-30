"""The hass_ytdlp component."""
import logging
import os
import re
import time

import voluptuous as vol

from homeassistant.const import CONF_FILE_PATH
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from yt_dlp import YoutubeDL

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

async def async_setup_entry(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the hass_ytdlp component."""    
    hass.states.async_set("downloader.%s" % DOMAIN, "0")
    if not os.path.isdir(config.data[CONF_FILE_PATH]):
        os.mkdir(config.data[CONF_FILE_PATH], 0o755)

    def progress_hook(d):
        """Update download progress & Update the state of the entity"""
        attr = hass.states.get("downloader.%s" % DOMAIN).attributes.copy()
        filename = d["info_dict"]["filename"].split("/")[-1]
        if d["status"] == "finished":
            hass.states.set("downloader.%s" % DOMAIN, len(attr), attr)
            attr.pop(filename)
            _LOGGER.info("download finished")
        if d["status"] == "downloading":
            try:
                speed = d["speed"]
            except KeyError as e:
                speed = 0
                _LOGGER.warning(e)
            try:
                downloaded = d["downloaded_bytes"]
            except KeyError as e:
                downloaded = 0
                _LOGGER.warning(e)
            try:
                total = d["total_bytes"]
            except KeyError as e:
                total = "Nan"
                _LOGGER.warning(e)
            try:
                eta = d["eta"]
            except KeyError as e:
                eta = 0
                _LOGGER.warning(e)
                
            attr[filename] = {
                "speed": speed,
                "downloaded": downloaded,
                "total": total,
                "eta": eta,
            }
        if d["status"] == "error":
            hass.states.set("downloader.%s" % DOMAIN, len(attr), attr)
            attr.pop(filename)
            _LOGGER.error("download error")
            
        hass.states.set("downloader.%s" % DOMAIN, len(attr), attr)

    def download(call):
        """Download a video."""
        # logger = DLP_Logger(self.downloads, hook.id)
        ydl_opts = {
            'ignoreerrors': True,
            "progress_hooks": [progress_hook],
            "paths": {
                "home": config.data[CONF_FILE_PATH],
                "temp": "temp",
            },
        }
        for k, v in call.data.items():
            if k not in ["url", "progress_hooks", "paths"]:
                ydl_opts[k] = v
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([call.data["url"]])

    hass.services.async_register( 
        DOMAIN,
        "download",
        download,
        schema=vol.Schema({vol.Required("url"): cv.url}),
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    hass.states.async_remove("downloader.%s" % DOMAIN)
    hass.services.async_remove(DOMAIN, "download")

    return True
