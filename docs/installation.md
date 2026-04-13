# installation guide

## downloading the installer

1. go to the [latest release](https://github.com/Ltony2022/icee/releases/latest) page.
2. under assets, download the file named `YourAppName-Windows-<version>-Setup.exe`.

## installing

1. run the downloaded `.exe` file.
2. if windows defender smartscreen appears, click "more info" then "run anyway". the app is not code-signed, so this warning is expected.
3. choose an install directory or keep the default.
4. follow the installer prompts to complete the installation.

## first launch

1. open the app from the start menu or desktop shortcut.
2. the backend service starts automatically in the background.
3. the dns proxy requires administrator privileges to bind to port 53. when you start the proxy for the first time, a uac prompt will appear. accept it to allow dns blocking.

## dns proxy setup

the dns proxy works by intercepting dns lookups on your machine. to use it:

1. go to the dns proxy section in the app.
2. add domains you want to block.
3. click start to launch the proxy.
4. accept the administrator prompt.

blocked domains take effect immediately. subdomains are blocked automatically. for example, blocking `example.com` also blocks `www.example.com` and `api.example.com`.

## uninstalling

use "add or remove programs" in windows settings, or run the uninstaller from the app's install directory. the app data in your temp folder (`%TEMP%\icee-utils`) is not removed automatically. delete it manually if you want a clean removal.
