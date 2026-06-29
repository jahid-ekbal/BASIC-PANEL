import pymem
from pyinjector import inject


exeName = input("Enter Exe Name: ")
pm = pymem.Pymem(exeName)
inject(pm.process_id,"dlls/FromOtherProcess.dll")
pm.close_process()