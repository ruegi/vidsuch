set VERSION=

del /S /Y .\dist\VideoSync
pyinstaller --clean -y -p D:\\DEV\\Py\\vidsuch --hiddenimport sqlalchemy -n VideoSync VideoSync.py
:Ende
echo Fertig!
rem pause
