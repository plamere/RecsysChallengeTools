
"""
    iterates over the million playlist dataset and outputs info
    about what is in there.

    Usage:

        python stats.py path-to-mpd-data
"""
import sys
import json
import re
import collections
import os
import datetime


ntitles = collections.Counter()
max_files_for_quick_processing = 10

def process_mpd(path):
    count = 0
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            process_info(mpd_slice['info'])
            for playlist in mpd_slice['playlists']:
                process_playlist(playlist)
            count += 1

            if quick and count > max_files_for_quick_processing:
                break


def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.,\/#!$%\^\*;:{}=\_`~()@]", ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def process_playlist(playlist):
    nname = normalize_name(playlist['name'])
    ntitles[nname] += 1

def process_info(_):
    pass


def process_challenge(path):
    f = open(path)
    challenge = json.loads(f.read())
    cnames = collections.Counter()

    for playlist in challenge['playlists']:
        if 'name' in playlist:
            if not just_empty or len(playlist['tracks']) == 0:
                cname = normalize_name(playlist['name'])
                cnames[cname] += 1
    out = []
    for cname, count in cnames.most_common():
        out.append( (ntitles[cname], count, cname) )

    out.sort()
    for mpd_count, challenge_count, name in out:
        print mpd_count, challenge_count, name


if __name__ == '__main__':
    quick = False
    just_empty = False
    path = sys.argv[1]
    challenge = sys.argv[2]

    remaining_args = sys.argv[3:]

    while remaining_args:
        arg = remaining_args.pop(0)
        if arg == '--quick':
            quick = True
        elif arg == '--empty':
            just_empty = True

    process_mpd(path)
    process_challenge(challenge)
