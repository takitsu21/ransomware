import sys
import subprocess


def get_hwid():
    if sys.platform == 'win32':
        out = subprocess.Popen('wmic csproduct get uuid', shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode().split('\n')[1].strip()

    elif sys.platform == 'darwin':
        out = subprocess.Popen('ioreg -rd1 -c IOPlatformExpertDevice | grep -E "UUID"', shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode().split(' ')[-1].strip().replace('"', '')
    else:
        out = subprocess.Popen('sudo cat /sys/class/dmi/id/product_uuid',
                               shell=True, stdout=subprocess.PIPE).stdout.read().decode().strip()
    return out


textchars = bytearray({7, 8, 9, 10, 12, 13, 27} |
                      set(range(0x20, 0x100)) - {0x7f})


def is_binary_string(bytes): return bool(bytes.translate(None, textchars))
