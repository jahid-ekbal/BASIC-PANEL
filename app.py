from pdb import run
import datetime
import pymem
from flask import Flask,jsonify, redirect, render_template,request,session
from keyauth import *
import sys
import Memory
from pyinjector import inject
import utils
import threading
app = Flask(__name__,template_folder='templates',static_folder='static')
def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest
keyauthapp = api(
    name = "REGIX STORE", # Application Name
    ownerid = "JjpGjXJhfE", # Owner ID
    secret = "f1e3904593d857cc2af43b4f59a3e008286677b82f15aeb8bf6fa4ca278a6265", # Application Secret
    version = "1.0", # Application Version
    hash_to_check = getchecksum()
)

# Global Stuff
messages = []
addresses = []
drag_addresses = []
user = {}
is32bit = True
isChangedDirectory = False
tab = 1
version = ""

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for both development and PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



@app.get('/sniper-panel')
def sniperPanel():
    if keyauthapp.user_data.username:
        return render_template('Sniper.html')
    else:
        return redirect('/')

@app.get('/extra-panel')
def extraPanel():
    if keyauthapp.user_data.username:
        return render_template('Extra.html')
    else:
        return redirect('/')
@app.get('/settings')
def settings():
    if keyauthapp.user_data.username:
        return render_template('Settings.html')
    else:
        return redirect('/')



@app.post('/auth')
def auth():
    if request.method == "POST":
        
        data = request.get_json()
        reply = keyauthapp.login(user=data['username'],password=data['password'])
        if reply:
            user['username'] = keyauthapp.user_data.username
            user['hwid'] = keyauthapp.user_data.hwid
            user['ip'] = keyauthapp.user_data.ip
            dt_object = datetime.datetime.fromtimestamp(int(keyauthapp.user_data.expires))
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            user['expiry'] = formatted_time
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            messages.append(
                time + f" Logged in as {keyauthapp.user_data.username}"
            )
            return jsonify(
                status= 200,
                message="logged in",
            )
        else:
            return jsonify(
                status=301,
                message="Credentails MissMatch"
            )
@app.post('/auth-check')
def authCheck():
    
    if not user:
        
        return jsonify(
            status=302,
            
        )
    else:
        
        return jsonify(
            status=200,
            
        )


@app.get('/logout')
def logout():
    reply = keyauthapp.logout()
    print(reply)
    if reply:
        return jsonify(
            status=200
        )
    else:
        return jsonify(
            status= 303
        )

@app.post('/logs')
def logs():
    global messages
    return jsonify(
        status=200,
        message=messages[::-1]
    )

@app.post('/user-info')
def userInfo():
    onlineUsers = keyauthapp.fetchOnline()
    OU = ''
    if onlineUsers is None:
        OU = "No online users"
    else:
        for i in range(len(onlineUsers)):
            OU += onlineUsers[i]["credential"] + " "
    return jsonify(
        status=200,
        username=user['username'],
        ipAddress=user['ip'],
        hwid=user['hwid'],
        expiry=user['expiry'],
        onlineUsers=OU
    )

@app.post('/get-process')
def getProcess():
    
    status = Memory.get_process("HD-Player.exe")
    if status == False:
        
        return jsonify(
            status=303,
            
        )
    else:
       
        return jsonify(
            status=200,
            pid=status,
            
        )



@app.post('/aimbot-load')
def aimbotLoad():
    
    global addresses
    addresses = Memory.aimbot_load()
    if addresses:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Aimbot Load Done"
        )
        
        return jsonify(
            status=200,
            
        )
    else:
        messages.append(
            str(datetime.datetime.now) + " Aimbot Load Error"
        )
        
        return jsonify(
            status=304,
            
        )

@app.post('/aimbot-on')
def aimbotOn():
    global addresses
    Memory.aimbot_on(addresses)
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    messages.append(
        time + " Aimbot On Done"
    )
    return jsonify(
        status=200
    )

@app.post('/aimbot-off')
def aimbotOff():
    global addresses
    Memory.aimbot_off(addresses)
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    messages.append(
        time + " Aimbot Off Done"
    )
    return jsonify(
        status=200
    )

@app.post('/aimdrag-load')
def aimDragLoad():
    global drag_addresses
    drag_addresses = Memory.drag_load()
    if drag_addresses:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Aimdrag Load Done"
        )
        return jsonify(
            status=200
        )
    else:
        return jsonify(
            status=304
        )

@app.post('/aimdrag-on')
def aimDragOn():
    global drag_addresses
    Memory.aimdrag_on(drag_addresses)
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    messages.append(
        time + " Aimdrag On Done"
    )
    return jsonify(
        status = 200
    )

@app.post('/aimdrag-off')
def aimDragOff():
    global drag_addresses
    Memory.aimdrag_off(drag_addresses)
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    messages.append(
        time + " Aimdrag Off Done"
    )
    return jsonify(
        status=200
    )


@app.post('/chams-menu')
def chamsMenu():
    global isChangedDirectory
    pid = Memory.get_pid('HD-Player.exe')
    if isChangedDirectory:
        os.chdir('..')
        isChangedDirectory = False
    try:
        inject(pid,Memory.get_resource_path('dlls/FARHAN EXE.dll'))
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Chams Menu Done"
        )
        return jsonify(
            status=200
        )
    except:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Chams Menu Failed"
        )
        return jsonify(
            status=305
        )

@app.post('/update-bit32')
def bit32():
    is32bit = True
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    messages.append(
        time + " 32 bit FreeFire Selected"
    )
    return jsonify(
        status=200
    )

@app.post('/update-bit64')
def bit64():
    is32bit = True
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    messages.append(
        time + " 64 bit FreeFire Selected"
    )
    return jsonify(
        status=200
    )

@app.post('/chams-3D')
def chams3D():
    global isChangedDirectory
    pid = Memory.get_pid('HD-Player.exe')
    if isChangedDirectory:
        os.chdir('..')
        isChangedDirectory = False
    try:
        inject(pid,Memory.get_resource_path('dlls/wallhack.dll'))
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Chams 3D Done"
        )
        return jsonify(
            status=200
        )
    except:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Chams 3D Failed"
        )
        return jsonify(
            status=305
        )

@app.post('/sniper-scope-on')
def sniperScopeOn():
    global is32bit
    if not is32bit:
        search = rb"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        replace = b"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    else:
       search=rb"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    replace=b"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    status = Memory.scan_and_replace("HD-Player.exe",search,replace)
    if status:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Scope On"
        )
        return jsonify(
            status=200
        )
    else:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Scope On Failed"
        )
        return jsonify(
            status=304
        )
@app.post('/sniper-scope-off')
def sniperScopeOf():
    global is32bit
    if not is32bit:
        search = b"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        replace = rb"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    else:
        search=rb"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        replace=b"\xFF\xFF\x08\x00\x00\x00\x00\x00\x60\x40\xCD\xCC\x8C\x3F\x8F\xC2\xF5\x3C\xCD\xCC\xCC\x3D\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    status = Memory.scan_and_replace("HD-Player.exe",replace,search)
    if status:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Scope Off"
        )
        return jsonify(
            status=200
        )
    else:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Scope Off Failed"
        )
        return jsonify(
            status=304
        )

@app.post('/sniper-switch-on')
def sniperSwitchOn():
    global is32bit
    if not is32bit:
        search = rb"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"
        replace = b"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"
    else:
        search1 = rb"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"     
        search2 = rb"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"
       
    status = Memory.scan_and_replace("HD-Player.exe",search1,replace)
    status1 = Memory.scan_and_replace("HD-Player.exe",search2,replace)
   
    
    
    if status:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Switch On"
        )
        return jsonify(
            status=200
        )
    else:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Switch On Failed"
        )
        return jsonify(
            status=304
        )



@app.post('/sniper-switch-off')
def sniperSwitchOff():
    global is32bit
    if not is32bit:
        search = rb"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"
        replace = b"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"
    else:
        search1 = rb"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"     
        search2 = rb"\x00\x00\x01\x00\x00\x00\xC3\xF5\xE8\x3F\x01\x00\x00\x00\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x00\x00\xC3\xF5\xE8\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\xCD\xCC\xCC\x3D\x00\x00\x00\x00\x00\x00\x5C\x43\x00\x00\x90\x42\x00\x00\xB4\x42\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x00\x00\x80\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x20\x41\x00\x00\x34\x42\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x0A\xD7\x23\x3F\x9A\x99\x99\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x00\x00\x00\x00\x00\x00\x40\x3F\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x80\x3F\x00\x00\x00\x00\x01"
       
    status = Memory.scan_and_replace("HD-Player.exe",search1,replace)
    status1 = Memory.scan_and_replace("HD-Player.exe",search2,replace)
    
    
    if status and status1 :
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Switch On"
        )
        return jsonify(
            status=200
        )
    else:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " Sniper Switch On Failed"
        )
        return jsonify(
            status=304
        )









@app.post('/m82b-esp-on')
def M82BEspOn():
    global is32bit
    if not is32bit:
        search = b"\x19\x00\x00\x00\x69\x00\x6E\x00\x67\x00\x61\x00\x6D\x00\x65\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x5F\x00\x62\x00\x6D\x00\x39\x00\x34\x00"
        replace= rb"\x1D\x00\x00\x00\x65\x00\x66\x00\x66\x00\x65\x00\x63\x00\x74\x00\x73\x00\x2F\x00\x76\x00\x66\x00\x78\x00\x5F\x00\x69\x00\x6E\x00\x61\x00\x67\x00\x6D\x00\x65\x00\x5F\x00\x6C\x00\x61\x00\x73\x00\x65\x00\x72\x00\x5F\x00\x73\x00\x68\x00\x6F\x00\x70\x00"
    else:
        search = b"\x19\x00\x00\x00\x69\x00\x6E\x00\x67\x00\x61\x00\x6D\x00\x65\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x5F\x00\x62\x00\x6D\x00\x39\x00\x34\x00"
        replace= rb"\x1D\x00\x00\x00\x65\x00\x66\x00\x66\x00\x65\x00\x63\x00\x74\x00\x73\x00\x2F\x00\x76\x00\x66\x00\x78\x00\x5F\x00\x69\x00\x6E\x00\x61\x00\x67\x00\x6D\x00\x65\x00\x5F\x00\x6C\x00\x61\x00\x73\x00\x65\x00\x72\x00\x5F\x00\x73\x00\x68\x00\x6F\x00\x70\x00"
        status = Memory.scan_and_replace("HD-Player.exe",search,replace)
    if status:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " M82B Esp On"
        )
        return jsonify(
            status=200
        )
    else:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " M82B on Failed"
        )
        return jsonify(
            status=304
        )

@app.post('/m82b-esp-off')
def M82BEspOff():
    global is32bit
    if not is32bit:
        search = b"\x19\x00\x00\x00\x69\x00\x6E\x00\x67\x00\x61\x00\x6D\x00\x65\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x5F\x00\x62\x00\x6D\x00\x39\x00\x34\x00"
        replace= rb"\x1D\x00\x00\x00\x65\x00\x66\x00\x66\x00\x65\x00\x63\x00\x74\x00\x73\x00\x2F\x00\x76\x00\x66\x00\x78\x00\x5F\x00\x69\x00\x6E\x00\x61\x00\x67\x00\x6D\x00\x65\x00\x5F\x00\x6C\x00\x61\x00\x73\x00\x65\x00\x72\x00\x5F\x00\x73\x00\x68\x00\x6F\x00\x70\x00"
    else:
        search = b"\x19\x00\x00\x00\x69\x00\x6E\x00\x67\x00\x61\x00\x6D\x00\x65\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x2F\x00\x70\x00\x69\x00\x63\x00\x6B\x00\x75\x00\x70\x00\x5F\x00\x62\x00\x6D\x00\x39\x00\x34\x00"
        replace= rb"\x1D\x00\x00\x00\x65\x00\x66\x00\x66\x00\x65\x00\x63\x00\x74\x00\x73\x00\x2F\x00\x76\x00\x66\x00\x78\x00\x5F\x00\x69\x00\x6E\x00\x61\x00\x67\x00\x6D\x00\x65\x00\x5F\x00\x6C\x00\x61\x00\x73\x00\x65\x00\x72\x00\x5F\x00\x73\x00\x68\x00\x6F\x00\x70\x00"
    status = Memory.scan_and_replace("HD-Player.exe",replace,search)
    if status:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " M82B Esp Off"
        )
        return jsonify(
            status=200
        )
    else:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        messages.append(
            time + " M82B off Failed"
        )
        return jsonify(
            status=304
        )


@app.get('/')
def homePage():
    global user,version
    if keyauthapp.user_data.username:
        return redirect('dashboard',version=version)
    else:
        return render_template('Homepage.html')

@app.get('/dashboard')
def dashboard():
    global user
    if keyauthapp.user_data.username:
        return render_template('Dashboard.html',user=user,version=keyauthapp.version)
    else:
        return redirect('/')

def run_flask():
    import socket
    # Force bind to all interfaces
    app.run(debug=False, host='0.0.0.0', port=4070, threaded=True)

# Call it like this
if __name__ == "__main__":
    run_flask()
    
isTaskClose = True
def taskManger():
    global isTaskClose
    time.sleep(2)
    while True:
        if utils.check_process("Taskmgr.exe") and isTaskClose:
            try:
                pm = pymem.Pymem("Taskmgr.exe")
                inject(pm.process_id,get_resource_path("dlls/alpha.dll"))
                isTaskClose = False
                continue
            except:
                continue
        elif not utils.check_process("Taskmgr.exe") and isTaskClose == False:
            isTaskClose = True
            continue
        time.sleep(0.25)

isProcessClose = True
def processManger():
    global isProcessClose
    time.sleep(2)
    while True:
        if utils.check_process("ProcessHacker.exe") and isProcessClose:
            try:
                pm2 = pymem.Pymem("ProcessHacker.exe")
                inject(pm2.process_id,get_resource_path("dlls/alpha.dll"))
                isProcessClose = False
                continue
            except:
                continue
        elif not utils.check_process("ProcessHacker.exe") and isProcessClose == False:
            isProcessClose = True
            continue
        time.sleep(0.25)



if __name__ == "__main__":
    # sec = threading.Thread(target=security)
    flask = threading.Thread(target=run_flask)
    taskthred = threading.Thread(target=taskManger)
    processthread = threading.Thread(target=processManger)
    #resourcethread = threading.Thread(target=resourceManger)
    # sec.start()
    taskthred.start()
    processthread.start()
    #resourcethread.start()
    flask.start()
    flask.join()
    taskthred.join()
    #resourcethread.join()
    processthread.join()
    # sec.join()