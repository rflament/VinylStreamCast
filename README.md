# VinylStreamCast

VinylStreamCast is a system designed to seamlessly blend the nostalgic charm of vinyl records with the convenience of modern streaming technology. 
Using a Raspberry Pi, this application enables the streaming of audio from a vinyl player connected via Bluetooth and facilitates control over Chromecast devices, including Google Nest speakers set in stereo mode.

## Features

- **Vinyl to Digital Streaming**: Convert audio from vinyl records into a digital format using a Raspberry Pi.
- **Chromecast Integration**: Stream the converted audio to Chromecast-enabled devices for enhanced playback.
- **Web Interface**: Control streaming and view real-time playback information via a Flask-based web interface.
- **Google Nest Stereo Support**: Specifically supports streaming to a stereo pair of Google Nest speakers.

## Getting Started

### Prerequisites

- A Raspberry Pi with Bluetooth capability.
- A vinyl player with Bluetooth output.
- Chromecast or Google Nest speakers.
- Python 3 and relevant libraries.

### Installation

1. **Prepare Your Raspberry Pi**: 
   Ensure your Raspberry Pi is set up with the latest OS and connected to your network.

2. **Install Dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip
   pip3 install Flask pychromecast

3. **Pair the turntable**:

   ```bash
   sudo bluetoothctl
   power on
   pairable on
   scan on
   pair TABLE_MAC_ADDRESS
   connect TABLE_MAC_ADDRESS
   
   

4. **Clone the Repository:**:
   ```bash
   git clone https://github.com/your-username/VinylStreamCast.git
   cd VinylStreamCast
   
5. **Configure DarkIce::**:
 Adjust /home/pi/turntable/darkice.cfg with your specific DarkIce configuration.



## Contributing

Contributions to VinylStreamCast are welcome! If you've got ideas for improvements or found a bug, don't hesitate to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

Inspired by https://maker.pro/raspberry-pi/projects/how-to-build-an-internet-radio-station-with-raspberry-pi-darkice-and-icecast and https://dupontgu.medium.com/how-to-stream-your-record-player-throughout-your-home-for-cheap-fb044368a240
