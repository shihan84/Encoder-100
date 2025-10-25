define APP_NAME "IBE-100" 
define APP_VERSION "1.0.0" 
define APP_DESCRIPTION "ITAssist Broadcast Encoder - 100 (IBE-100)" 
 
Name "${APP_NAME}" 
OutFile "dist\IBE-100-1.0.0-installer.exe" 
InstallDir "$PROGRAMFILES\ITAssist\IBE-100" 
 
Section "MainSection" SEC01 
  SetOutPath "$INSTDIR" 
  SetOverwrite ifnewer 
  File "dist\IBE-100\*.*" 
  File /r "dist\IBE-100\*" 
 
  CreateDirectory "$SMPROGRAMS\ITAssist" 
  CreateShortCut "$SMPROGRAMS\ITAssist\IBE-100.lnk" "$INSTDIR\IBE-100.exe" 
  CreateShortCut "$DESKTOP\IBE-100.lnk" "$INSTDIR\IBE-100.exe" 
 
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\IBE-100" "DisplayName" "ITAssist Broadcast Encoder - 100 (IBE-100)" 
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\IBE-100" "UninstallString" "$INSTDIR\uninstall.exe" 
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\IBE-100" "DisplayVersion" "1.0.0" 
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\IBE-100" "Publisher" "ITAssist Broadcast Solutions" 
 
  WriteUninstaller "$INSTDIR\uninstall.exe" 
SectionEnd 
 
Section "Uninstall" 
  Delete "$INSTDIR\*.*" 
  RMDir /r "$INSTDIR" 
  Delete "$SMPROGRAMS\ITAssist\IBE-100.lnk" 
  Delete "$DESKTOP\IBE-100.lnk" 
  RMDir "$SMPROGRAMS\ITAssist" 
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\IBE-100" 
SectionEnd 
