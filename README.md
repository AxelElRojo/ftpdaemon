# ftpdaemon
This script implements a daemon that checks filesystem changes and pushes them to an FTP server. On startup, the daemon first checks
the server and downloads any files that are found to be newer in the server, it also uploads any files found to be newer in the local device.

# WARNING!
**This script is still in development and hasn't been tested to work properly.**
I've tested it by running it manually, and it works, but I currently can't test it as a systemd service.

# Why?
I first thought of something like this a while ago. I wanted to emulate games, but I couldn't decide where to play them, my phone has greater portability,
but my desktop has a bigger screen, after debating with myself for a while I thought "Why not both?". 

I'm aware that there are already existing solutions, many people use cloud services like Google Drive, or One Drive to store and sync their saves
across devices, but I found some limitations I didn't like:
1. Some aren't compatible with Linux.
2. Most use propietary services.
3. Some aren't easily compatible with my phone.
4. I want a (mostly) plug & play experience.

While I'm aware point #3 isn't addressed by this script, I'll start working on that after I finish this project.

# Is my computer compatible?
Inotify (a dependency) is only available on Linux, so unless you are using Linux or have a drop-in equivalent, no.

# How does it work?
It's simple:
1. Checks all files in the server and locally:
	1. Downloads (and overwrites) all files that are newer in the server and those that don't currently exist locally.
	2. Uploads (and overwrites) all files that are newer locally and those that don't currently exists remotely.
2. Monitors the directory for changes:
	1. After a program writes to any file, it uploads it to the server.

**Once the script reaches step #2, it stays there, it only goes back to step #1 if restarted.**

# Dependencies
You need to install the following packages in order to run the script:
- Dotenv.
- Inotify.
- Fasteners.

The script uses more libraries, but they should be preinstalled, in case the script doesn't run, try installing these:
- FTPLib.
- Datetime.
- Dateutil.
- OS.
- Atexit.

Make sure they're accesible system-wide, i.e., not installed in an user directory.

# Usage
## Configuration
After you clone/download the repo, create a .env file with the following variables:
```env
FTP_USER="ftpUser"
FTP_PASSWD="userPassword"
FTP_PORT="tcpPortUsed" # It usually is 21
FTP_HOST="ftp.host"
FTP_REMOTE_ROOT="/server/directory/that/holds/your/saves"
FTP_LOCAL_ROOT="/local/directory/that/holds/your/saves/"
FTP_TIME_DIFF="6"
```
The variable `FTP_TIME_DIFF` holds the time difference with the server, in this example, the server time is 6 hours ahead of the local machine.
## Installation
After creating the `.env` file, run the install script:
```console
chmod +x ./install.sh
sudo ./install.sh
```
This will install the script and `.env` in `/var/opt/ftpdaemon/`, along with the corresponding service file in `/etc/systemd/system/`.

After that, just enable the service with systemd:
```console
sudo systemctl enable --now ftpdaemon
```
You may also want to check if it's running:
```console
sudo systemctl status ftpdaemon
```
If you are not using systemd, refer to your init system's documentation on how to create a service.
