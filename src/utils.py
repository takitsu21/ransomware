import sys
import subprocess

def get_hwid():
    if sys.platform == 'win32':
        out = subprocess.Popen('wmic csproduct get uuid', shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode().split('\n')[1].strip()
    else:
        out = subprocess.Popen('sudo cat /sys/class/dmi/id/product_uuid',
                               shell=True, stdout=subprocess.PIPE).stdout.read().decode().strip()
    return out