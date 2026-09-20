Before you start sending notifications, you need to run these commands, 1 for your pc or laptop thats receiving the notification and your home assistant device thats sending the notifications. 

Receiving Side run:
sudo apt update && sudo apt install -y python3 python3-pip libnotify-bin mosquitto-clients && pip3 install paho-mqtt

Sending Side (Home Assistant side) run:
sudo apt update && sudo apt install -y mosquitto mosquitto-clients
(optional): sudo systemctl enable mosquitto && sudo systemctl start mosquitto

