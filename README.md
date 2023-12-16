# Integration to use YT-DLP within Home Assistant

Integration can be used with [`yt_dlp-card`](https://github.com/ybk5053/yt_dlp-card) to see download status

## Installation

### Manually

Clone or download this repository and copy the "yt_dlp" directory to your "custom_components" directory in your config directory

```<config directory>/custom_components/yt_dlp/...```

## HACS

- Add Custom Repositories

```text
Repository: https://github.com/ybk5053/yt_dlp_hass
Category: Integration
```

## Configuration

### Configuration via the "Configuration -> Integrations" section of the Home Assistant UI

- Search for the integration labeled "Youtube DLP" and select it.  
- Enter the path for the download directory.

## Downloading

### Via Developer tools -> Services

- Search for service "yt_dlp.download"
- Enter link to video download and click "call service"
- Additional options can be passed into the data in Yaml Mode
- See [`yt_dlp/YoutubeDL.py`](yt_dlp/YoutubeDL.py#L183) or `help(yt_dlp.YoutubeDL)` in a Python shell for list of options

### Via [`yt_dlp-card`](https://github.com/ybk5053/yt_dlp-card)
