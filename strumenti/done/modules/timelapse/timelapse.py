from strumenti.done.libs.module import Field, fill_values

BLUE = "\x1b[1;32m"
RED = "\x1b[1;36m"
WHITE = "\x1b[1;0m"

class TimelapseModule( ):
    ## values
    values = {}
    n_imgs = 0


    @staticmethod
    def args():
        return {'sourceDir':'.','fps':20}

    def info(msg):
        return "\t" + BLUE + msg + WHITE

    def warning(msg):
        return "\t" + RED + msg + WHITE

    def run( self, values=None ):
        fields = [Field('FPS',default=25),
                  Field('sourceDir',default='.',validate=self.validate_sourceDir),
                  Field('output',default='timelapse.mp4')]
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

