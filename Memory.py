import pyexpat
import pymem
import pymem.pattern
import pymem.process
import time
import ctypes
import ctypes.wintypes
import os
import sys
from pymem.memory import read_bytes, write_bytes
from pymem.pattern import pattern_scan_all

pm = None

# ============ MKP FUNCTION ============
def mkp(aob: str):
    if '??' in aob:
        if aob.startswith("??"):
            aob = f" {aob}"
            n = aob.replace(" ??", ".").replace(" ", "\\x")
            b = bytes(n.encode())
        else:
            n = aob.replace(" ??", ".").replace(" ", "\\x")
            b = bytes(f"\\x{n}".encode())
        del n
        return b
    else:
        m = aob.replace(" ", "\\x")
        c = bytes(f"\\x{m}".encode())
        del m
        return c

# ============ AOB PATTERNS (CLEAN STRINGS) ============
AIMBOT_PATTERN = "FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 A5 43"

DRAG_PATTERN = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A5 43 ?? ?? ?? 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ??"

# ============ SCAN AND REPLACE ============
def scan_and_replace(processName, search, replace):
    try:
        pm = pymem.Pymem(processName)
        # If search is string, convert using mkp
        if isinstance(search, str):
            search = mkp(search)
        matches = pattern_scan_all(pm.process_handle, search, return_multiple=True)
        if matches:
            for match in matches:
                pm.write_bytes(match, replace, len(replace))
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_process(procesName):
    try:
        pm = pymem.Pymem(procesName)
        print('Process Found Please Continue')
        return pm.process_id
    except:
        print('Process Not Found Waiting for process')
        return False

def get_pid(processName):
    pm = pymem.Pymem(processName)
    return pm.process_id

def get_drive_serial_number():
    kernel32 = ctypes.windll.kernel32
    volume_name_buffer = ctypes.create_unicode_buffer(1024)
    file_system_name_buffer = ctypes.create_unicode_buffer(1024)
    serial_number = ctypes.c_ulong(0)
    max_component_length = ctypes.c_ulong(0)
    file_system_flags = ctypes.c_ulong(0)
    success = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p("C:\\"),
        volume_name_buffer,
        ctypes.sizeof(volume_name_buffer),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(file_system_flags),
        file_system_name_buffer,
        ctypes.sizeof(file_system_name_buffer)
    )
    if success:
        return serial_number.value
    return None

def get_hwid():
    serial_number = get_drive_serial_number()
    if serial_number:
        return serial_number
    return None

def adjust_privileges():
    SE_DEBUG_NAME = "SeDebugPrivilege"
    SE_PRIVILEGE_ENABLED = 0x00000002
    token_handle = ctypes.c_void_p()
    luid = ctypes.c_longlong()
    
    ctypes.windll.advapi32.OpenProcessToken(
        ctypes.windll.kernel32.GetCurrentProcess(),
        0x20 | 0x8,
        ctypes.byref(token_handle)
    )
    ctypes.windll.advapi32.LookupPrivilegeValueA(
        0, SE_DEBUG_NAME.encode('ascii'), ctypes.byref(luid)
    )
    
    class LUID_AND_ATTRIBUTES(ctypes.Structure):
        _fields_ = [("Luid", ctypes.c_longlong), ("Attributes", ctypes.c_ulong)]
    class TOKEN_PRIVILEGES(ctypes.Structure):
        _fields_ = [("PrivilegeCount", ctypes.c_ulong), ("Privileges", LUID_AND_ATTRIBUTES)]
    
    new_privileges = TOKEN_PRIVILEGES(1, LUID_AND_ATTRIBUTES(luid.value, SE_PRIVILEGE_ENABLED))
    ctypes.windll.advapi32.AdjustTokenPrivileges(
        token_handle, False, ctypes.byref(new_privileges), 0, None, None
    )
    ctypes.windll.kernel32.CloseHandle(token_handle)

def find_pattern(pm, module_name, pattern):
    if isinstance(pattern, str):
        pattern = mkp(pattern)
    return pattern_scan_all(pm.process_handle, pattern, return_multiple=True)

# ============ AIMBOT FUNCTIONS ============
def aimbot_load():
    try:
        adjust_privileges()
        process_name = "HD-Player.exe"
        pm = pymem.Pymem(process_name)
        
        # ✅ FIX: Use mkp() to convert string pattern to bytes
        pattern = mkp(AIMBOT_PATTERN)
        addresses = find_pattern(pm, process_name, pattern)

        if not addresses:
            print("No addresses found")
            return False
        print(f"Found {len(addresses)} addresses")
        return addresses
    except Exception as e:
        print(f"Error: {e}")
        return False

original_values = []

def aimbot_on(addresses):
    global original_values
    if not addresses:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        original_values.clear()
        for address in addresses:
            addressscan = address + 0xB6   # Source
            addressrep = address + 0xB2    # Target
            buffer = pm.read_int(addressscan)
            original_values.append(pm.read_int(addressrep))
            pm.write_int(addressrep, buffer)
        return True
    except Exception as e:
        print(f"Error in aimbot_on: {e}")
        return False

def aimbot_off(addresses):
    global original_values
    if not addresses or not original_values:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        for index, address in enumerate(addresses):
            addressrep = address + 0xB2
            if index < len(original_values):
                pm.write_int(addressrep, original_values[index])
        return True
    except Exception as e:
        print(f"Error in aimbot_off: {e}")
        return False

# ============ DRAG FUNCTIONS ============
drag_addresses = []
original_drag_values = []

def drag_load():
    global drag_addresses
    try:
        adjust_privileges()
        process_name = "HD-Player.exe"
        pm = pymem.Pymem(process_name)
        
        # ✅ FIX: Use mkp() instead of raw bytes
        pattern = mkp(DRAG_PATTERN)
        drag_addresses = find_pattern(pm, process_name, pattern)

        if not drag_addresses:
            print("No drag addresses found")
            return False
        print(f"Found {len(drag_addresses)} drag addresses")
        return drag_addresses
    except Exception as e:
        print(f"Error in drag_load: {e}")
        return False

def aimdrag_on(drag_addresses):
    global original_drag_values
    if not drag_addresses:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        original_drag_values.clear()
        for address in drag_addresses:
            addressscan = address + 0xE2
            addressrep = address + 0xAE
            buffer = pm.read_int(addressscan)
            original_drag_values.append(pm.read_int(addressrep))
            pm.write_int(addressrep, buffer)
        return True
    except Exception as e:
        print(f"Error in aimdrag_on: {e}")
        return False

def aimdrag_off(drag_addresses):
    global original_drag_values
    if not drag_addresses or not original_drag_values:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        for index, address in enumerate(drag_addresses):
            addressrep = address + 0xAE
            if index < len(original_drag_values):
                pm.write_int(addressrep, original_drag_values[index])
        return True
    except Exception as e:
        print(f"Error in aimdrag_off: {e}")
        return False