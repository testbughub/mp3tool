#!/usr/bin/env python3

import os, sys, argparse, glob, re, mimetypes, distutils.spawn, shutil
from subprocess import Popen, PIPE

########################### Init ###########################

text = "A mp3 download & modification helper."
parser = argparse.ArgumentParser(description=text, formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=33))

# Args

parser.add_argument("-d", metavar="<URL>", help="download mp3 from URL", action="store")

parser.add_argument("-i", dest="filename", metavar="<file>", nargs='+', help="input file(s)", action="store")

parser.add_argument("-p", help="create folder(s) based on artist", action="store_true")

parser.add_argument("-l", help="list ID3v2 tags", action="store_true")

parser.add_argument("-g", help="analyze and save replay gain", action="store_true")

parser.add_argument("-a", metavar="<artist>", help="set artist tag", action="store")

parser.add_argument("-t", metavar="<title>", help="set song title tag", action="store")

parser.add_argument("-b", metavar="<album>", help="set album tag", action="store")

parser.add_argument("-e", metavar="<image|URL>", help="embed image (leave blank for default)", action="store")

parser.add_argument("-m", metavar="<playlist name>", help="create m3u playlist", action="store")


args = parser.parse_args()

# No args = help
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(2)

############################################################

YDL = str(distutils.spawn.find_executable("youtube-dl"))
FFM = str(distutils.spawn.find_executable("ffmpeg"))
MID = str(distutils.spawn.find_executable("mid3v2"))
REG = str(distutils.spawn.find_executable("replaygain"))
FIN = str(distutils.spawn.find_executable("find"))

file = ""
files = []
if args.filename:
    if len(args.filename) == 1:
        infile = args.filename[0]
        if not os.path.exists(infile):
            parser.error("The file %s does not exist!" % infile)
        elif not re.match(r".*audio\/mpeg", str(mimetypes.guess_type(infile))):
            parser.error("%s is not an mp3 file!" % infile)
        else:
            file = str(re.escape(args.filename[0]))
    elif len(args.filename) >= 2:
        for i in args.filename:
            infile = i
            if not os.path.exists(infile):
                parser.error("The file %s does not exist!" % infile)
            elif not re.match(r".*audio\/mpeg", str(mimetypes.guess_type(infile))):
                parser.error("%s is not an mp3 file!" % infile)
            else:
                files.append(str(i))

if args.d:
    if not distutils.spawn.find_executable("youtube-dl"):
        print("Couldn't find youtube-dl!")
        print("Install it with 'pip3 install --upgrade youtube-dl'")
        sys.exit()
    if not distutils.spawn.find_executable("ffmpeg"):
        print("Couldn't find ffmpeg!")
        print("Install it with 'sudo apt install ffmpeg'")
        sys.exit()
    if args.filename:
        print("No input files when downloading mp3's")
        sys.exit()
    print("Downloading audio from '" + args.d + "'...")
    ret = os.system(YDL + " --force-ipv4 -x " + args.d)
    if ret == 0:
        list_of_files = glob.glob('./*')
        latest_file = max(list_of_files, key=os.path.getctime)
        newfile = str(re.escape(re.sub(r"\-\w+\..*(?!.*\-+\w\..*)$", ".mp3", latest_file)))
        print("Converting to mp3...")
        os.system(FFM + " -i " + re.escape(latest_file) + " " + newfile)
        os.remove(latest_file)
        list_of_files = glob.glob('./*')
        latest_file = max(list_of_files, key=os.path.getctime)
        fullname = re.sub(r".*\/", '', os.getcwd()) + " - " + re.sub(r"^\.\/", "", latest_file)
        if not re.match(r".*\w\-\w.*.mp3", latest_file):
            termsize = int(re.sub(r"columns\=", "", re.findall(r"columns\=[0-9]+", str(os.get_terminal_size()))[0]))
            if os.path.isfile(fullname):
                print(" ")
                print("#" * termsize)
                print(" ")
                print("The downloaded mp3 doesn't seem to have the artist included")
                print("in it's name, and a file '" + fullname + "' already exists.")
                rename = input("Replace it with the newly downloaded mp3 '" + re.sub(r"^\.\/", "", latest_file) + "'? [Y/n] ")
                print(" ")
                print("#" * termsize)
                if rename == "n":
                    print(" ")
                    print("Skipping rename...")
                    print("New file = " + str(re.sub(r"^\.\/", "", latest_file)))
                    print(" ")
                    print("Done!")
                    sys.exit()
                else:
                    print(" ")
                    print("Replacing " + fullname + " with " + str(re.sub(r"^\.\/", "", latest_file)) + "...")
                    os.rename(latest_file, re.sub(r".*\/", '', os.getcwd()) + " - " + re.sub(r"^\.\/", "", latest_file))
        print(" ")
        print('Done!')
        sys.exit()


# Files req
elif len(files) >= 1 or not file == "":
    if args.l:
        if not distutils.spawn.find_executable("mid3v2"):
            print("Couldn't find mid3v2!")
            print("Install it with 'pip3 install --upgrade mutagen'")
            sys.exit()
        os.system(MID + " " + file)
        sys.exit()

    if args.g:
        if not distutils.spawn.find_executable("replaygain"):
            print("Couldn't find replaygain!")
            print("Install it with 'pip3 install --upgrade rgain3'")
            sys.exit()
        os.system(REG + " " + file)

    if args.a:
        if not distutils.spawn.find_executable("mid3v2"):
            print("Couldn't find mid3v2!")
            print("Install it with 'pip3 install --upgrade mutagen'")
            sys.exit()
        os.system(MID + ' -a ' + str(re.escape(args.a)) + ' ' + re.sub(r"\'", "\\'", file))

    if args.t:
        if not distutils.spawn.find_executable("mid3v2"):
            print("Couldn't find mid3v2!")
            print("Install it with 'pip3 install --upgrade mutagen'")
            sys.exit()
        os.system(MID + ' -t ' + str(re.escape(args.t)) + ' ' + re.sub(r"\'", "\\'", file))

    if args.b:
        if not distutils.spawn.find_executable("mid3v2"):
            print("Couldn't find mid3v2!")
            print("Install it with 'pip3 install --upgrade mutagen'")
            sys.exit()
        os.system(MID + ' -A ' + str(re.escape(args.b)) + ' ' + re.sub(r"\'", "\\'", file))

    if args.e:
        if not distutils.spawn.find_executable("ffmpeg"):
            print("Couldn't find ffmpeg!")
            print("Install it with 'sudo apt install ffmpeg'")
        if len(args.e) == 0:
            DEF = "/home/lamarca/L4/Musik/div/unknown.png"
            os.system(FFM + " -i " + file + " -i " + DEF + " -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Cover' -metadata:s:v comment='Cover (front)' out.mp3")
        elif re.match(r"(^https\:|^http\:)", str(args.e)):
            ext = str(re.findall(r"\.\w+(?!.*\.\w+)$", str(args.e))[0])
            os.system(distutils.spawn.find_executable("wget") + " -O image" + ext + " " + str(args.e))
            os.system(FFM + " -i " + file + " -i " + "image" + ext + " -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Cover' -metadata:s:v comment='Cover (front)' out.mp3")
            os.remove("image" + ext)
        else:
            os.system(FFM + " -i " + file + " -i " + re.escape(args.e) + " -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Cover' -metadata:s:v comment='Cover (front)' out.mp3")
        os.replace("out.mp3", str(args.filename[0]))

    if args.p:
        if not distutils.spawn.find_executable("mid3v2"):
            print("Couldn't find mid3v2!")
            print("Install it with 'pip3 install --upgrade mutagen'")
            sys.exit()
        if len(args.filename) == 1:
            filename = args.filename[0]
            matched_lines = []
            artist = ""
            for file in filename:
                cmd_process = Popen([MID, filename], stdout=PIPE)
                with cmd_process.stdout:
                    for line in iter(cmd_process.stdout.readline, b''):
                        if re.match(br'^TPE1\=.*\n$', line):
                            matched_lines.append(line)
                            artist = re.sub(r"TPE1\=", "", matched_lines[0].decode().strip())
                cmd_process.wait()
                print(artist)
                if len(artist) == 0:
                    if not os.parh.exist('unknown'):
                        os.mkdir('unknown')
                        shutil.move(filename, 'unknown')
                    else:
                        shutil.move(filename, 'unknown')
                else:
                    if not os.path.exists(artist):
                        artistclean = re.sub(r"(\,|\/)", " ", artist)
                        os.mkdir(artistclean)
                        shutil.move(filename, artistclean)
                    else:
                        shutil.move(filename, artistclean)
        else:
            for file in files:
                matched_lines = []
                cmd_process = Popen([MID, str(file)], stdout=PIPE)
                with cmd_process.stdout:
                    for line in iter(cmd_process.stdout.readline, b''):
                        if re.match(br'^TPE1\=.*\n$', line):
                            matched_lines.append(line)
                            artist = re.sub(r"TPE1\=", "", matched_lines[0].decode().strip())
                cmd_process.wait()
                print(artist)
                if not os.path.exists(artist):
                    artistclean = re.sub(r"(\,|\/)", " ", artist)
                    os.mkdir(artistclean)
                shutil.move(file, artistclean)
    print(" ")
    print('Done!')


# Playlist
elif args.m:
    playlistclean = re.sub(r"(\,|\/)", " ", args.m)
    os.system(FIN + " . -iname '*.mp3' > " + re.escape(playlistclean) + ".m3u")
    print('Done!')

# # No files = error
# else:
#     parser.error("Missing input file(s)!")
#     sys.exit()
