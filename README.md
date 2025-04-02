# mp3Player

[![jhc github](https://img.shields.io/badge/GitHub-rpazuki.svg?style=flat&logo=github)](https://github.com/rpazuki)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> An mp3 player with multiple playlists support. This is a multi-platform project that is using [BeeWare](https://beeware.org/) framework.

## installing

### MacOS


```
brew install cmake
brew install portaudio
```

Next, find the 'portaudio' install address by running

```
brew info portaudio
```
and accordingly, replace the <PORTAUDIO-ADDRESS> in below command

```
export CFLAGS="-I/<PORTAUDIO-ADDRESS>/include/"
export LDFLAGS="-L/<PORTAUDIO-ADDRESS>/lib/"
pip install --global-option='build_ext' --global-option='-I/<PORTAUDIO-ADDRESS>/include' --global-option='-L/<PORTAUDIO-ADDRESS>/lib' -r requirment
```

## packaging

```
briefcase create
briefcase build
briefcase package
```
