# Tailscale-Linux-Tray-Icon
This is a simple Tailscale tray icon for connecting to a Tailscale exit node. Very rudimentary, but it also stops the Tailscale service for saving battery life!

This runs on Python3 and it is used to connect to a Tailscale exit node. At the moment, you can only insert the node manually once! That is because this works for me and 
i don`t need anything else

Requirements: curl and libnotify-bin, and of course python3!

When it stops the connection it also stops the tailscaled systemd service! this is to save battery!

limitations: 

At the moment, you need to insert the exit-node ip directly in the script. Aw rolso the exit node external ip, which is used for verify the connection.
will change this maybe in the future!
Sudo needs to be setup without a password. It can be easiley change in the script in multiple ways. But this works for me!

how to run:
just extract the directory into a path (e.g.: /home/)
create a startup sh script that has
python3 VPNTraY.py
Add that script to startup from the DE. ( not using cron!)
I use KDE autostart feature.
That`s it!
n`joy



