# icee utils

[![build](https://github.com/Ltony2022/icee/actions/workflows/build-windows.yml/badge.svg)](https://github.com/Ltony2022/icee/actions/workflows/build-windows.yml)
[![platform](https://img.shields.io/badge/platform-windows-blue)](https://github.com/Ltony2022/icee/releases)
[![license](https://img.shields.io/github/license/Ltony2022/icee)](LICENSE)
[![release](https://img.shields.io/github/v/release/Ltony2022/icee)](https://github.com/Ltony2022/icee/releases/latest)

distractions kill deep work. switching between tabs, opening social media "just for a second", or losing track of time adds up fast. most blocking tools are either too aggressive, too limited, or require you to fight your own browser.

icee utils is a lightweight desktop app that combines dns-level domain blocking, a pomodoro timer, and a spaced repetition flashcard system into one tool. it runs locally, needs no account, and gives you control over what gets blocked and when.

## what it does

**dns proxy** blocks distracting websites at the dns level. no browser extension needed. add domains to a block list and the proxy intercepts lookups before they reach the network. subdomains are blocked automatically.

**pomodoro timer** tracks focus and break sessions so you can work in structured intervals without watching a clock.

**flashcards** uses the sm-2 spaced repetition algorithm to schedule reviews. good for studying or retaining anything you keep forgetting.

**application blocker** prevents specific desktop applications from running during focus sessions.

## how to install

go to the [latest release](https://github.com/Ltony2022/icee/releases/latest), download the windows setup `.exe`, and run it. the installer lets you choose the install directory. no additional dependencies are needed.

for detailed installation steps, see the [installation guide](docs/installation.md).

## how to build from source

see the [windows build guide](docs/building-windows.md).

## tech stack

- backend: django, waitress, pyinstaller
- frontend: react, typescript, electron, vite, tailwind
- database: sqlite (local, no server required)
