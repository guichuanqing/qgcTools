@echo off

Title By key9928

cd\&color 0a&cls

reg add "HKCU\Control Panel\Colors" /v Window /t REG_SZ /d "202 234 206" /f

reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\DefaultColors\Standard" /v Window /t REG_DWORD /d 13298382 /f

pause