#!/usr/bin/env python
# encoding: utf-8
import wx, os
from pyo import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

########################
###soundbank##############
snds = ["smpl/01.wav", "smpl/02.wav", "smpl/03.wav"]
########################
###dictionnaire presets########
presets = {"khalif": {"taps": 5, "pulses": 2},
                "cumbia": {"taps": 4, "pulses": 3},
                "ruchenitza": {"taps": 7, "pulses": 3},                
                "tresillo": {"taps": 8, "pulses": 3},
                "ruchenitza2": {"taps": 7, "pulses": 4},
                "aksak": {"taps": 9, "pulses": 4},
                "zappa": {"taps": 11, "pulses": 4},
                "york": {"taps": 6, "pulses": 5}, 
                "nawakhat": {"taps": 7, "pulses": 5},
                "cinquillo": {"taps": 8, "pulses": 5},
                "agsag": {"taps": 9, "pulses": 5},
                "moussorgsky": {"taps": 11, "pulses": 5},
                "venda": {"taps": 12, "pulses": 5},
                "bossa": {"taps": 16, "pulses": 5},
                "bendir": {"taps": 8, "pulses": 7},
                "west-africa": {"taps": 12, "pulses": 7},
                "central-africa": {"taps": 16, "pulses": 9},
                "preset1": {"taps": 7, "pulses": [5, 3, 4]},
                "preset2": {"taps": 16, "pulses":[6, 8, 9]},
                "preset3": {"taps": 11, "pulses": [4, 5, 9]},
                "silence":{"taps": 0, "pulses": 0},
                }
prePresets = ["silence", "bossa", "tresillo", "cinquillo", "cumbia", "ruchenitza", "ruchenitza2", "khalif", "aksak", "york", "nawakhat",
                    "agsag", "venda", "bendir", "west-africa", "central-africa", "zappa", "moussorgsky", "preset1", "preset2",
                    "preset3"]



########################
########################               
class Voix :
    def __init__(self, path=snds[0], vol=0.75, pan=.5, bpm=160, taps=12, pulses=7, pitch=1, HPfreq=40, LPfreq=20000) :
        self.sample= SndTable(path)
        self.dur= self.sample.getDur()
        self.volume = Sig(vol)
        self.pan = Sig(pan)
        self.bpm = Sig(bpm)
        self.pitch = Sig(pitch)
        self.HPfreq = Sig(HPfreq)
        self.LPfreq = Sig(LPfreq)
        self.time = (30000/self.bpm)*0.001
        self.tap = taps
        self.pulse = pulses
        self.pitpit= self.dur * self.pitch
        self.trig= Euclide(time=self.time, taps=taps, onsets=pulses).play()
        self.tuti= TrigEnv(self.trig, self.sample, dur=self.pitpit, mul=self.volume)
        self.HPbandpass = ButHP(self.tuti, freq=self.HPfreq)
        self.LPbandpass = ButLP(self.HPbandpass, freq = self.LPfreq)
        self.ou = Pan(self.LPbandpass, outs=2, pan=self.pan).out()
        
    def setPath(self, x):
        self.sample.path = x   

    def setVol(self, x):
        self.volume.value = x

    def setPan(self, x):
        self.pan.value = x

    def setBPM(self, x):
        self.bpm.value = x
        
    def setPitch(self, x):
        self.pitch.value = x

    def setHP(self, x):
        self.HPfreq.value = x

    def setLP(self, x):
        self.LPfreq.value = x

    def setTaps(self, x):
        self.trig.taps = x
    
    def setPulses(self, x):
        self.trig.onsets = x
        
    def choose(self, preset_name):
        preset = presets[preset_name]
        taps = preset["taps"]
        pulses = preset["pulses"]
        self.setTaps(taps)
        self.setPulses(pulses)        

    def stop(self):
        self.trig.stop()
        return self    

    def play(self):
        self.trig.play()
        
    def out(self):
        self.ou.out()
        return self
 """      
########################################
#####GRAPHIQUES#########################

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size, audio):
        wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)
        self.audio = audio
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("#LSD12V")

        self.onOffText = wx.StaticText(self.panel, id=-1, label="tic tic toc tic", 
                                                    pos=(200,220), size=wx.DefaultSize)
        self.onOff = wx.ToggleButton(self.panel, id=-1, label="I-O", 
                                                pos=(190,185), size=wx.DefaultSize)
        self.onOff.Bind(wx.EVT_TOGGLEBUTTON, self.handleAudio)



###choose sample###       
        sample = [f for f in os.listdir(os.getcwd()) if f[-4:] in ['.wav']]
 
        self.popupText = wx.StaticText(self.panel, id=-1, label="Sample", 
                                                    pos=(120,15), size=wx.DefaultSize)
        self.popup = wx.Choice(self.panel, id=-1, pos=(120,38), 
                                        size=wx.DefaultSize, choices=sample)
                                        
        self.popup.Bind(wx.EVT_CHOICE, self.setSound)

###choose rythm###
        self.popupText = wx.StaticText(self.panel, id=-1, label="Rythmique", 
                                                    pos=(10,15), size=wx.DefaultSize)
        self.popup = wx.ListBox(self.panel, id=-1, pos=(8,38), size=(100, 430), 
                                        choices=prePresets)

        self.popup.Bind(wx.EVT_CHOICE, self.setRythm)

    def handleAudio(self, evt):
        if evt.GetInt() == 1:
            self.audio.trig.play()
        else:
            self.audio.trig.stop()
        
    def setSound(self, evt): 
         self.audio.sample.path = evt.GetString()
         self.audio.dur= self.audio.sample.getDur()
        
    def setRythm(self, evt):
         self.audio.choose(evt.GetString(preset_name))
        


app = wx.App()

audio = Voix()

mainFrame = MyFrame(self, parent=None, title="watch le popo qui coule pas", pos=(700,200), size=(500,550), audio)
mainFrame.Show()

app.MainLoop()

"""
##########################################
#####JETPACK_PROBOOSTER##############################
rt = Voix(path=snds[0], pulses=4)
tt = Voix(path=snds[1], taps=8, pulses=3).out()

#dly=Delay(tt)#



s.gui(locals())

