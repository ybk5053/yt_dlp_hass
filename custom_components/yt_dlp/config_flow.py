"""Handles the configuration flow for the hass_ytdlp custom component."""
import os

import voluptuous as vol
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_FILE_PATH
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Abort if already configured."""
        await self.async_set_unique_id("yt_dlp")
        self._abort_if_unique_id_configured()

        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            try:
                if not os.path.isdir(user_input[CONF_FILE_PATH]):
                    os.mkdir(user_input[CONF_FILE_PATH], 0o755)
            except OSError:
                errors["base"] = "cannot_create_folder"
                return self.async_show_form(
                    step_id="user", data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}), errors=errors
                )
            return self.async_create_entry(title="YT_DLP", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)

class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        errors = {}
        if user_input is not None:
            try:
                if not os.path.isdir(user_input[CONF_FILE_PATH]):
                    os.mkdir(user_input[CONF_FILE_PATH], 0o755)
            except OSError:
                errors["base"] = "cannot_create_folder"
                return self.async_show_form(
                    step_id="init", data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}), errors=errors
                )
            self._options.update(user_input)
            _LOGGER.warn(user_input)
            _LOGGER.warn(self._options)
            return self.async_create_entry(title="YT_DLP", data=self._options)

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema({vol.Required(CONF_FILE_PATH, default=self.config_entry.data[CONF_FILE_PATH]): str}), errors=errors
        )
