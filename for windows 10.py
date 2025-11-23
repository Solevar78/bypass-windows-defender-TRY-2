import os
import subprocess
import sys

def install_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_gpo_simple():
    gpo_code = '''import os
import subprocess
import time
import ctypes

def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file, None, 1)
        return False
    except:
        return False

if not run_as_admin():
    sys.exit()

time.sleep(1)

# 1. Устанавливаем настройку через реестр (это работает как групповые политики)
commands = [
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f',
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f',
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f',
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f',
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d 1 /f',
    
    # Останавливаем службы
    'sc stop WinDefend',
    'sc config WinDefend start= disabled',
    'sc stop WdNisSvc',
    'sc config WdNisSvc start= disabled',
    
    # Обновляем политики
    'gpupdate /force'
]

for cmd in commands:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Executed: {cmd}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

print("Windows Defender disabled via registry policies")
print("Settings will persist after reboot")
'''

    with open('simple_defender_disable.py', 'w', encoding='utf-8') as f:
        f.write(gpo_code)

def compile_to_exe():
    os.system('pyinstaller --onefile --noconsole --name "DefenderDisable" simple_defender_disable.py')
    print("EXE создан: DefenderDisable.exe")

if __name__ == "__main__":
    install_pyinstaller()
    create_gpo_simple()
    compile_to_exe()
