# -*- coding: utf-8 -*-

from toolkit.Mediakit import MediaInfo


medd = MediaInfo(filename = "/home/codenewman/Videos/e0021hke41y.m1.mp4")

print medd.get_duration()
print type(medd.get_duration())

