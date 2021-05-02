!python -m pip install --upgrade pip setuptools wheel
!python -m pip install lbry-libtorrent
!apt-get -qq install -y python3-libtorrent libtorrent-rasterbar-dev #for utilities used inside
!apt-get -qq install -y zip

import tensorflow as tf
import requests
import libtorrent as lt
from google.colab import drive
import re
from google.colab import files
import time


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

drive.mount('/content/drive')  #mounts your Drive 

start_time = time.time()
# set flagsto  true if you want to download from torrent and/or url (file server)
tor_flag = True 
url_flag = True

url_link = """
https://dl5.filehippo.com/f12/758/cc8e3a7a1a520c08e649c07f150e7ff708/uTorrent.exe?Expires=1590691228&Signature=fa7538cb965ad9d9cc03fea06cfbd4836f9de4a0&url=https://filehippo.com/download_utorrent/&Filename=uTorrent.exe
"""
#url file link
tor_link = """
magnet:?xt=urn:btih:98D60FCF4989155D3F9E88BF53EBA7EA55C09F86&dn=%5BHR%5D+Plunderer+20+%5B1080p+HEVC%5D+HR-GZ&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Fbt1.archive.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fbt2.archive.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.yoshi210.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.nyap2p.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.si%3A1337%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce
"""
#torrent magnet link



urlName =""
torName =""
if url_flag:
    r = requests.get(url_link, allow_redirects=True)
    filename = getFilename_fromCd(r.headers.get('content-disposition'))
    open(filename, 'wb').write(r.content)
    # !wget $url_link
    urlName = filename

if tor_flag:
    #torrenting 
    ses= lt.session()   #get session handle
    ses.listen_on(6896,6884)

    tparams = {"save_path":".",
            "storage_mode":lt.storage_mode_t(2),
            "paused":False,
            "auto_managed":True,
            "duplicate_is_error":False} #Torrent physical Parameters


    tor_handle = lt.add_magnet_uri(ses, tor_link, tparams) #initializing torrent with parameters
    ses.start_dht()
    print("Fetching Metadata...")    #torrent activity starts
    while(not tor_handle.has_metadata()):
        time.sleep(1)
    torName  = tor_handle.get_torrent_info()

    print("Starting the Torrent...")
    while(tor_handle.status().state != lt.torrent_status.seeding ):   #download progress 
        s = tor_handle.status()
        tor_status = ['queued','checking','fetching metadata',\
                    'downloading','finished', 'seeding', 'allocating']
        print("Progress:",s.progress*100, \
            "Down_speed:",s.download_rate/1000 ,"UP_Speed", s.upload_rate/1000,"Peers:", s.num_peers,"Status:",tor_status[s.state])
        time.sleep(5)
    #/torrenting
    print("---Torrent Downloaded in  %s seconds ---" % (time.time() - start_time))
    print("Downloading Done beero !")

    print("Loading into your drive")
    pathstr= (torName.files().file_path(0)).split("/")
    torName=pathstr[0]
#!mv $sostr "/content/drive/My Drive/"




 print("Loading into your drive")
 print(torName)
 print(urlName)
if tor_flag :
    !rsync -ar "$torName" "/content/drive/My Drive/"
if url_flag :
    !rsync -ar "$urlName" "/content/drive/My Drive/"

print("Please check your drive for content !!!")


#!mv $sostr "/content/drive/My Drive/"
