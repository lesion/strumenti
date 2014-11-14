from strumenti.done.libs.module import Field, fill_values, finish
from strumenti.libs.field_types import *

class TimelapseModule( ):
    ## values
    n_imgs = 0
    ext = ''
    fields={}


    def run( self, values=None ):
        fields = {

            'FPS': IntField({
                'default':25,
                'min':0,
                'max':100,
                'mandatory': True,
            }),

            'sourceDir': DirField({
                'default':'.',
                'mandatory': True,
                'validate_fn': self.validate_sourceDir
            }),

            'output': FileField({
                'default': 'timelapse.mp4',
                'mandatory': True,
            }),

            ''
        }
        self.fields.update(fields)
        return ("Encode", self.encode, fields)

    def validate_sourceDir(self):
        from os import listdir
        from os.path import splitext
        allowed_ext = ['.jpg','.jpeg','.png']
        found = False
        for img in listdir(self.fields['sourceDir'].value):
            self.ext = splitext(img)[1]
            if splitext(img)[1].lower() in allowed_ext:
                found+=1
        return found

    def encode(self):
        values = self.fields
        command = "echo mencoder mf://%s/*%s -mf fps=%d -vf scale=1280:-1 -ovc x264 -x264encopts pass=1:bitrate=5000:crf=20:preset=veryslow -nosound -ofps %s -noskip -of rawvideo -o rawoutput.264; ffmpeg -f h264 -i rawoutput.264 -r 30 -vcodec copy %s; rm rawoutput.264" % (values['sourceDir'].value,self.ext,values['FPS'].value,values['FPS'].value,values['output'].value)
        import os
        os.system(command)
        return finish

