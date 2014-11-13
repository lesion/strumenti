from strumenti.done.libs.module import Field, fill_values
from strumenti.libs.field_types import *

class TimelapseModule( ):
    ## values
    values = {}
    n_imgs = 0


    def run( self, values=None ):
        fields = [

            IntField('FPS',{
                'default':25,
                'min':0,
                'max':100,
                'mandatory': True,
            }),

            DirField('sourceDir',{
                'default':'.',
                'mandatory': True,
            }),

            FileField('output',{
                'default': 'timelapse.mp4',
                'mandatory': True,
            }),

        ]
        return ("Encode", self.encode, fields)

    def validate_sourceDir(self,val):
        from os import listdir
        from os.path import splitext
        allowed_ext = ['.jpg','.jpeg','.png']
        found = 0
        for img in listdir(val):
            self.ext = splitext(img)[1]
            if splitext(img)[1].lower() in allowed_ext:
                found+=1
        print found
        return found


    @fill_values
    def encode(self,values):
        command = "mencoder mf://%s/*%s -mf fps=%d -vf scale=1280:-1 -ovc x264 -x264encopts pass=1:bitrate=5000:crf=20:preset=veryslow -nosound -ofps %s -noskip -of rawvideo -o rawoutput.264; ffmpeg -f h264 -i rawoutput.264 -r 30 -vcodec copy %s; rm rawoutput.264" % (values['sourceDir'],self.ext,values['FPS'],values['FPS'],values['output'])
        import os
        os.system(command)

