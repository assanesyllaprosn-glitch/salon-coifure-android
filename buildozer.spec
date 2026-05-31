[app]

# (str) Title of your application
title = HOUSE FADE BARBER SHOP

# (str) Package name
package.name = saloncoifure

# (str) Package domain (needed for android/ios packaging)
package.domain = org.housefade

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,json,db

# (list) Pattern to exclude source files
source.exclude_patterns = 

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = kivy==2.0.0,python-dateutil==2.8.2,pyjnius==1.4.1,android

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,NFC

# (list) Features (Android)
android.features = android.hardware.nfc

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum Android API this application requires
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25.2.9519653

# (str) Android SDK version to use
android.sdk = 33

# (str) python-for-android branch to use, depends on android.api
android.p4a_branch = develop

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android library dependencies
android.gradle_dependencies =

# (bool) Indicate if the application should be fullscreen or not
android.fullscreen = False

# (str) The Android arch to build for, choices are armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Whether to copy Python's standard library into the app
android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
