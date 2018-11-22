pyuic5 -x VidSuchUI3.ui -o VidSuchUI3.py
goto Ende

del /S .\dist\VidSuch
pyinstaller -w -i VidSuch.ico --clean VidSuch.py
copy .\VidSuch.ico .\dist\VidSuch

:Ende
echo Fertig!
rem pause
