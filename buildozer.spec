[app]

title = JARVIS
package.name = jarvis
package.domain = org.prempatel

source.dir = .
source.include_exts = py,json,kv,png,jpg

version = 1.0

requirements = python3==3.13.2,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.accept_sdk_license = True

android.api = 35
android.minapi = 24
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
