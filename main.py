import time
from plugins.Microdot import Microdot
from modules.TemperatureController import TemperatureController

app = Microdot()

registeredModules = [TemperatureController]
moduleInstances = []
def load_config(path='config.json'):
    with open(path) as f:
        return json.load(f)
#Load config data
config = load_config()

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"[WiFi] Connecting to {ssid}...")
        wlan.connect(ssid, password)
        timeout = 10  # seconds
        for _ in range(timeout * 10):
            if wlan.isconnected():
                break
            time.sleep(0.1)
    if wlan.isconnected():
        print(f"[WiFi] Connected! IP: {wlan.ifconfig()[0]}")
    else:
        print("[WiFi] Connection failed.")
    return wlan

wlan = connect_wifi(config.wifi.ssid, config.wifi.password)

def init_modules():
    global moduleInstances
    moduleInstances = []

    for module_class in registeredModules:
        instance = module_class()
        instance.ready()
        moduleInstances.append(instance)

# Initial load
init_modules()

@app.route('/reload-modules')
def reload_modules(request):
    print("[SYSTEM] Reloading modules...")
    init_modules()
    return 'Modules reloaded', 200

# Run web server in background
import _thread
def start_server():
    app.run()

_thread.start_new_thread(start_server, ())

# Main loop
while True:
    for instance in moduleInstances:
        instance.process()
    time.sleep(1)
