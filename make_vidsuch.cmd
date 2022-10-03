set VERSION=

echo Bearbeite VidSuchUI%VERSION%.ui ...
pyuic6 -x VidSuchUI%VERSION%.ui -o VidSuchUI.py
echo %ERRORLEVEL%

if "%1"=="simple" goto Ende

del /S /Y .\dist\VidSuch
pyinstaller -i VidSuch.ico --windowed --clean -y -p D:\\DEV\\Py\\vidsuch\\FilmDetails --hiddenimport FilmDetails --hiddenimport sqlalchemy -n vidsuch VidSuch%VERSION%.py
copy .\VidSuch.ico .\dist\VidSuch
copy .\EndBut*.png .\dist\VidSuch
:Ende
echo Fertig!
rem pause
