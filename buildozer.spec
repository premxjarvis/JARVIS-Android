[app]

title = JARVIS
package.name = jarvis
package.domain = org.prempatel

source.dir = .
source.include_exts = py,json,kv,png,jpg

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.accept_sdk_license = True
android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
