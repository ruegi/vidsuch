'''
Klassendefinition der Klasse videoFile
rg, 2021-07-30
'''
import os
from pymediainfo import MediaInfo
# from pprint import pprint

class videoFile:
    def __init__(self, fullPathName):        
        self.fullPathName = fullPathName
        _, tail = os.path.split(fullPathName)
        fname, fext = os.path.splitext(tail)
        self.name = fname
        self.ext = fext[1:]     # den Punkt übergehen        self.duration = 0   # FilmLänge in ms
        self.frameCount = 0
        self.fps = 0.0
        self.bitRate = 0
        self.weite = "1280"
        self.hoehe = "768"
        self.typ = "HD"
        self.g_track = None
        self.v_track = None
        self.a_tracks = []
        self.t_tracks = []
        self.duration = 0.0
        self.getVideoDetails()

    def getVideoDetails(self):
        try:
            media_info = MediaInfo.parse(self.fullPathName)            
            # pprint(MediaInfo.to_data(media_info) )
            for track in media_info.tracks:
                # print(track.track_type)
                if track.track_type == "Video":
                    v_track = track
                elif track.track_type == "Audio":
                    self.a_tracks.append(track) 
                elif track.track_type == "Text":              
                    self.t_tracks.append(track)
                elif track.track_type == "General":
                    self.g_track = track
            # g_track = media_info.general_tracks[0]
            # 
            # v_track = media_info.video_tracks[0]
            # print(3)
            # t_track = media_info.text_tracks[0]
            # print(4)
            # for i in range(0, len(media_info.audio_tracks)):
            #     self.a_tracks.append = media_info.audio_tracks[i]
            if v_track is None:
                pass
            else:
                v_fr = v_track.frame_rate
                v_fc = v_track.frame_count
                v_br = v_track.bitrate
                g_du = self.g_track.duration
                # print("Video-FC =", v_fc)        
                self.fps = float(v_fr)
                self.weite = v_track.width
                iWeite  = int(self.weite)
                self.hoehe = v_track.height
                self.bitRate = v_track.bit_rate
                self.duration = float(g_du)
                self.frameCount = int(self.duration / 1000 * self.fps + 0.5)
                if iWeite < 1280:
                    self.typ = "SD"
                    return
                elif iWeite < 1920:
                    self.typ = "HD"
                    return
                else:
                    self.typ = "FullHD"
                    return 
        except:
            print("Abbruch!")         
            return