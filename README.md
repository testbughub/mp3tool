## Description
Simple python script for various basic mp3 operations.  
This is just something I made while learning to use argparse for python.

### Dependencies
`youtube-dl` - downloading  
`ffmpeg` - converting/embedding  
`mid3v2` - id3 tagging  
`replaygain` - gain analyzing

### Getting started
```
git clone https://github.com/testbughub/mp3tool
cd mp3tool
chmod +x mp3tool.py
```

### Usage
```
$ ./mp3tool.py -h
usage: mp3tool.py [-h] [-d <URL>] [-i <file> [<file> ...]] [-p] [-l] [-g]
                  [-a <artist>] [-t <title>] [-b <album>] [-e <image|URL>]
                  [-m <playlist name>]

A mp3 download & modification helper.

optional arguments:
  -h, --help              show this help message and exit
  -d <URL>                download mp3 from URL
  -i <file> [<file> ...]  input file(s)
  -p                      create folder(s) based on artist
  -l                      list ID3v2 tags
  -g                      analyze and save replay gain
  -a <artist>             set artist tag
  -t <title>              set song title tag
  -b <album>              set album tag
  -e <image|URL>          embed image (leave blank for unknown)
  -m <playlist name>      create m3u playlist
  ```
  
  ###### 'unknown' image by [Spencer Imbrock](https://unsplash.com/photos/JAHdPHMoaEA)
