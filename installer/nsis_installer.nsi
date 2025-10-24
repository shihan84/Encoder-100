; ITAssist Broadcast Encoder - 100 (IBE-100)
; Professional NSIS Installer Script for Windows
; Cross-platform packaging and deployment

!define APP_NAME "IBE-100"
!define APP_VERSION "1.0.0"
!define APP_DESCRIPTION "ITAssist Broadcast Encoder - 100 (IBE-100)"
!define APP_PUBLISHER "ITAssist Broadcast Solutions"
!define APP_URL "https://itassist.one"
!define APP_EXECUTABLE "IBE-100.exe"
!define APP_ICON "assets\icon.ico"

; Modern UI
!include "MUI2.nsh"

; General
Name "${APP_NAME}"
OutFile "dist\${APP_NAME}-${APP_VERSION}-installer.exe"
InstallDir "$PROGRAMFILES\ITAssist\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "Main Application" SEC01
    SectionIn RO
    
    SetOutPath "$INSTDIR"
    SetOverwrite ifnewer
    
    ; Main application files
    File "dist\${APP_NAME}\${APP_EXECUTABLE}"
    File /r "dist\${APP_NAME}\*"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\ITAssist"
    CreateShortCut "$SMPROGRAMS\ITAssist\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}"
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}"
    
    ; Registry entries
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_DESCRIPTION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
    
    ; Uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; File associations (if needed)
    ; WriteRegStr HKCR ".ibe" "" "${APP_NAME}"
    ; WriteRegStr HKCR "${APP_NAME}\DefaultIcon" "" "$INSTDIR\${APP_EXECUTABLE}"
    ; WriteRegStr HKCR "${APP_NAME}\shell\open\command" "" "$INSTDIR\${APP_EXECUTABLE} %1"
SectionEnd

Section "Desktop Shortcut" SEC02
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}"
SectionEnd

Section "Start Menu Shortcut" SEC03
    CreateDirectory "$SMPROGRAMS\ITAssist"
    CreateShortCut "$SMPROGRAMS\ITAssist\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}"
SectionEnd

Section "TSDuck Integration" SEC04
    ; Check if TSDuck is installed
    ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TSDuck" "InstallLocation"
    ${If} $0 != ""
        DetailPrint "TSDuck found at: $0"
    ${Else}
        MessageBox MB_YESNO "TSDuck not found. Would you like to download and install TSDuck?" IDYES download_tsduck IDNO skip_tsduck
        download_tsduck:
            ExecShell "open" "https://tsduck.io/download/"
        skip_tsduck:
    ${EndIf}
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\${APP_EXECUTABLE}"
    Delete "$INSTDIR\uninstall.exe"
    RMDir /r "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\ITAssist\${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\ITAssist"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
    
    ; Remove file associations (if created)
    ; DeleteRegKey HKCR ".ibe"
    ; DeleteRegKey HKCR "${APP_NAME}"
SectionEnd

; Section Descriptions
LangString DESC_SEC01 ${LANG_ENGLISH} "Main application files and core components."
LangString DESC_SEC02 ${LANG_ENGLISH} "Create desktop shortcut for easy access."
LangString DESC_SEC03 ${LANG_ENGLISH} "Create start menu shortcut."
LangString DESC_SEC04 ${LANG_ENGLISH} "Check and configure TSDuck integration."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} $(DESC_SEC01)
    !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} $(DESC_SEC02)
    !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} $(DESC_SEC03)
    !insertmacro MUI_DESCRIPTION_TEXT ${SEC04} $(DESC_SEC04)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Version Information
VIProductVersion "${APP_VERSION}.0"
VIFileVersion "${APP_VERSION}.0"
VIAddVersionKey "ProductName" "${APP_DESCRIPTION}"
VIAddVersionKey "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey "LegalCopyright" "© 2024 ITAssist Broadcast Solutions | Dubai • Mumbai • Gurugram"
VIAddVersionKey "FileDescription" "${APP_DESCRIPTION}"
VIAddVersionKey "FileVersion" "${APP_VERSION}"
VIAddVersionKey "ProductVersion" "${APP_VERSION}"
VIAddVersionKey "InternalName" "${APP_NAME}"
VIAddVersionKey "OriginalFilename" "${APP_NAME}-${APP_VERSION}-installer.exe"
