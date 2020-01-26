pyuic5 -x VidSuchUI4.ui -o VidSuchUI.py
rem goto Ende

del /S .\dist\VidSuch
pyinstaller -w -i VidSuch.ico --clean VidSuch4.py
copy .\VidSuch.ico .\dist\VidSuch
copy .\EndBut*.png .\dist\
:Ende
echo Fertig!
rem pause
	