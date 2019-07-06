# oldingm

Telegram messages joiner

Idea from <https://github.com/SlavikMIPT/opentfd>

## Install

1. `pip3 install telethon pysocks`
2. Setup your credentials in *cred.py.example* and remove *example* from name
3. `python3 oldingm.py` to do authentication (only once, while you have *.session)
4. Change working directory in *oldingm.service*
5. `cp oldingm.service /etc/systemd/system/`
6. `systemctl enable oldingm`
7. `systemctl start oldingm`
