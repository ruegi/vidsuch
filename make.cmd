set VERSION=

echo Bearbeite VidSuchUI%VERSION%.ui ...
pyuic5 -x VidSuchUI%VERSION%.ui -o VidSuchUI.py
echo %ERRORLEVEL%

if "%1"=="simple" goto Ende

del /S /Y .\dist\VidSuch
pyinstaller -w -i VidSuch.ico --clean -y -p .\FilmDetails --hiddenimport FilmDetails\FilmDetailsUI.py -n vidsuch VidSuch%VERSION%.py
copy .\VidSuch.ico .\dist\VidSuch
copy .\EndBut*.png .\dist\VidSuch
:Ende
echo Fertig!
rem pause
