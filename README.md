# Integration to use Yt-DLP within Home Assistant

Integration can be used with yt_dlp-card to see download status

## Installation

### Manually

Clone or download this repository and copy the "yt_dlp" directory to your "custom_components" directory in your config directory

```<config directory>/custom_components/yt_dlp/...```

## Configuration

### Configuration via the "Configuration -> Integrations" section of the Home Assistant UI

1. Search for the integration labeled "Youtube DLP" and select it.  
2. Enter the path for the download directory.

## Downloading

### Via Developer tools -> Services

1. Search for service "yt_dlp.download"
2. Enter link to video download and click "call service"
3. Additional options can be passed into the data in Yaml Mode
4. See [`yt_dlp/YoutubeDL.py`](yt_dlp/YoutubeDL.py#L183) or `help(yt_dlp.YoutubeDL)` in a Python shell for list of options

### Via Yt_DLP-Card
