# The Isaac Archive
Full of stuff that I made (with or without AI) for anyone to Fork (Please mention me in readme.md) or use.

If programs do not work, they may need modifying to your system or dependencies may be needed. I would recommend using your AI of choice to solve it.

---

Jarvis.py - This is a Jarvis like bot made for ubuntu. Once downloaded set your telegram bot ID (@BotFather), your Telegram User ID, your desired pincode (Currently 1234) and set your directory for your unauthjarvis.txt file. Additional resources may be required.

---

Syslogs - Inside there are 3 files - syslogs - Ubuntu laptop.py which was made for the Lenovo ideapad 310-15ISK but most functions will work for other Ubuntu laptops, syslogs - Raspberry Pi 4.py which is the same except missing power modes and battery stuff. Made to run on the Raspberry Pi 4 model b running Raspberry Pi OS 64-bit but may work across other boards and other os, and the syslog_graph.html which visualizes the uploaded syslog file. Syslog files are stored as [d.m.y]syslog.txt. Please note that you may need to change the syslog file directory and may need to set up start on boot.

---

HANotify - This useful tool allows sending notifications to a Ubutntu 26 device. Run the 2 commands specified in the README.txt to install all the required dependencies. Then in home assistant, go to Settings -> Automatons & Scenes -> Create Automation -> Create New Automation -> 3 dots in top right corner -> Edit in YMAL and paste in the Base Automation script in the downloaded folder. Finally, in your ha_notify folder, edit it and ensure the MQTT topics are the same (currently Notify/test) and enter in the machine thats running Home Assistant's IP (ifconfig in terminal) and press Ctrl + S to save. To run it, go to terminal and type 'cd /home/YOURUSER/Downloads/HANotify'(change to the download location), then run 'python 3 ha_notify.py'. If everything works, when you run the automation it will send a notification to your computer.
