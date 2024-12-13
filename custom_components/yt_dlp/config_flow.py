"""Handles the configuration flow for the hass_ytdlp custom component."""
import os

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_FILE_PATH
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            try:
                if not os.path.isdir(user_input[CONF_FILE_PATH]):
                    os.mkdir(user_input[CONF_FILE_PATH], 0o755)
            except OSError:
                errors["base"] = "cannot_create_folder"
                return self.async_show_form(
                    step_id="user", 
                    data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}), 
                    errors=errors
                )
            await self.async_set_unique_id(f"{DOMAIN}.downloader")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}), 
            errors=errors
        )
    
    
    async def async_step_reconfigure(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                if not os.path.isdir(user_input[CONF_FILE_PATH]):
                    os.mkdir(user_input[CONF_FILE_PATH], 0o755)
            except OSError:
                errors["base"] = "cannot_create_folder"
                return self.async_show_form(
                    step_id="user", 
                    data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}), 
                    errors=errors
                )
            await self.async_set_unique_id(f"{DOMAIN}.downloader")
            self._abort_if_unique_id_mismatch()
            return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_FILE_PATH): str}),
            errors=errors
        )
