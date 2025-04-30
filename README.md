# mp3Player

[![rpazuki github](https://img.shields.io/badge/GitHub-rpazuki-181717.svg?style=flat&logo=github)](https://github.com/rpazuki)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

### platforms
![iOS](https://img.shields.io/badge/macOS-999999.svg?style=flat&logo=apple)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white)
![iOS](https://img.shields.io/badge/iOS-999999.svg?style=flat&logo=apple)

> An mp3 player with multiple playlists support. This is a multi-platform project that is using [BeeWare](https://beeware.org/) framework.

## installing

### Linux


```
sudo apt install cmake
sudo apt install portaudio19-dev python3-pyaudio
pip install pyMOSF[beeware]
```

### MacOS


```
brew install cmake
brew install portaudio
pip install pyMOSF[beeware]
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
### IOS
You need to first install and compile both of these external projects (refere to thier instructions):
 1. [Python-Apple-support](https://github.com/beeware/Python-Apple-support)
 2. [Mobile-Forge](https://github.com/flet-dev/mobile-forge)
```
git clone https://github.com/beeware/Python-Apple-support.git
git clone https://github.com/flet-dev/mobile-forge.git
```
Next, copy the content of 'recipes' folder to 'mobile-forge' project's 'recipes'. After that, you can create
required wheels:
```
forge iOS setuptools-git-versioning
forge iOS numpy
forge iOS pymp3
```
Make sure you updates the xcode paths in each recipe's 'meta.yaml'.
Also update the following entry in 'pyproject.tmol' of this project according to your 'mobile-forge' installation
```
requirement_installer_args = ["--find-links", "/Users/<usename>/<mobile-forge-address>/dist/"]
```

and finally,
```
pip install pyMOSF[beeware]
```

## packaging

```
briefcase create
briefcase build
briefcase package
```

for iOS, use
```
briefcase create iOS
briefcase build iOS

rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/ios-arm64/lib/python3.13/lib-dynload/_hashlib.cpython-313-iphoneos.so
rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/ios-arm64/lib/python3.13/lib-dynload/_ssl.cpython-313-iphoneos.so

rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/ios-arm64_x86_64-simulator/lib/python3.13/lib-dynload/_hashlib.cpython-313-iphoneos.so
rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/ios-arm64_x86_64-simulator/lib/python3.13/lib-dynload/_ssl.cpython-313-iphoneos.so

rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/iphoneos/lib/python3.13/lib-dynload/_hashlib.cpython-313-iphoneos.so
rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/iphoneos/lib/python3.13/lib-dynload/_ssl.cpython-313-iphoneos.so

rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/iphonesimulator/lib/python3.13/lib-dynload/_hashlib.cpython-313-iphoneos.so
rm ./build/mp3Player/ios/xcode/Support/Python.xcframework/iphonesimulator/lib/python3.13/lib-dynload/_ssl.cpython-313-iphoneos.so

```
(make sure to use correct python version for both the directory name and the so file) Next, you can open the Xcode project in "./build/mp3Player/ios/xcode" folder.

