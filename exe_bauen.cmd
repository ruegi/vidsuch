pyuic5 -x VidSuchUI.ui -o VidSuchUI.py
del /S .\dist\VidSuch
pyinstaller -w -i VidSuch.ico --clean VidSuch.py
copy .\VidSuch.ico .\dist\VidSuch

echo Fertig!
rem pause
