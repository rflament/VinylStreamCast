import subprocess
import time
import pychromecast
import threading
import os
import socket
import fcntl
import struct
from flask import Flask, jsonify, send_from_directory

PORT = 5000
os.environ['DISPLAY'] = ':0.0'
app = Flask(__name__)
cast_connection = None


## Functions

def start_darkice():
    command = ["/usr/bin/darkice", "-c", "/home/pi/turntable/darkice.cfg"]
    try:
        subprocess.run(command, check=True)
        print("Darkice started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Darkice: {e}")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

def init_chromecast_connection():
    global cast_connection
    services, browser = pychromecast.discovery.discover_chromecasts()
    pychromecast.discovery.stop_discovery(browser)
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Stereo"])
    if not chromecasts:
        print("chromecast not found")
        return "No Chromecast with specified name found"
    castaudio = chromecasts[0]
    print("chromecast found");
    castaudio.wait()
    print(castaudio.status)
    cast_connection = castaudio

def start_cast():
    global cast_connection
    ip_address = get_ip_address('wlan0')
    stream_url = 'http://' + ip_address + ':8000/rapi.mp3'
    print('casting '+stream_url)

    cast_connection.wait()
    cast_connection.set_volume(0.40)
    mc = cast_connection.media_controller
    mc.stop()
    mc.play_media(stream_url, 'audio/mp3')
    mc.block_until_active()
    print(mc.status)
#    pychromecast.discovery.stop_discovery(browser)

def get_chromecast_song_status():
    global cast_connection
    image_url = "https://coloredvinylrecords.com/pictures/w/wu-tang-clan-enter-the-wu-tang-36-chambers.png"
    try:
        cast_connection.wait()
        media_status = cast_connection.media_controller.status
#        print(media_status)
        if media_status:
            if media_status.images and len(media_status.images) > 2:
                image_url = media_status.images[2].url
            return {"title": media_status.title, "artist": media_status.artist, "image": image_url, "source": media_status.content_type , "status": media_status.player_state }
        else:
            return {"status":"stopped", "image": image_url}
    except Exception as e:
        return {"status":"error", "image": image_url}

def hide_cursor():
    try:
        # Start unclutter with idle time set to 0
        subprocess.Popen(["unclutter", "-idle", "0"])
    except Exception as e:
        print(f"Error starting unclutter: {e}")

def launch_chromium():
    url = f"http://localhost:{PORT}/"
    print(url)
    command = f"chromium-browser --noerrdialogs --disable-infobars --start-maximized --incognito --touch-events=enabled --overscroll-history-navigation=0 --disable-pinch --autoplay-policy=no-user-gesture-required --touch-devices=6 --kiosk {url}"
    subprocess.run(command, shell=True)

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')

@app.route('/api/status', methods=['GET'])
def api_example():
    status = get_chromecast_song_status()
    return jsonify(status)

@app.route('/api/play', methods=['POST'])
def log_play_pressed():
    print("Play pressed")
    start_cast()
    return jsonify({"status": "Logged Play Pressed"}), 200



def start_flask_app():
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)



hide_cursor()
flask_thread = threading.Thread(target=start_flask_app)
chromium_thread = threading.Thread(target=launch_chromium)
flask_thread.start()
start_darkice()

# Wait for a short period to allow the server to start
time.sleep(2)
chromium_thread.start()
init_chromecast_connection()

# cast
#cast.cast();
