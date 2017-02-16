#!/usr/bin/env python
# encoding: utf-8
from pyo import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

########################
soundbank paths :
              'create SOUNDBANK file in project path'
########################
class Sampler():
    def__init__(self, snd, pitch, volume, dcy)
        'self.snd = snd'
        self.sf = SfPlayer(path=SOUNDBANK+'snd', speed='pitch', mul='env')

        snd = 'select-sound-from-soundbank-here' 
        pitch = 'pitch-control-here' [0.5,1.5]
        volume = [0, 1.2]
        dcy = 'create decay ctrls here'
        env = Adsr(attack=0.01, decay = dcy, sustain=.2, release=.1, dur=2, mul = volume)
        'create-volume-control-here'


s.gui(locals())
