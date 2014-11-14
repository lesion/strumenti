from strumenti.done.libs.module import Field, fill_values, finish
from strumenti.libs.field_types import *
from strumenti.libs.image import *

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

            'size': Field({
                'default':'1280x720',
                'completer': self.size_completer,
                'mandatory': True
            })
        }
        self.fields.update(fields)
        return ("Encode", self.encode, fields)

    def size_completer(self,text,state):
        from os import listdir
        from strumenti.libs.image import get_image_size

        # get size of first image in source directory
        (orig_w,orig_h) = get_image_size(listdir(self.fields['sourceDir'].value)[0])
        self.orig_w = orig_w
        self.orig_h = orig_h

        list_valid_res = [ ( 1280,720 ), (1920,1080)] #[ "1280x720","1920x1080", "%dx%d" % ( orig_w,orig_h) ]
        # prima faccio la proporzione per capire come scalare l'immagine originale mantenendo la proporzione
        # quindi vedo se la proporzione e' uguale

        valid_res = ["scale=%d:%d" % (orig_w,orig_h)]

        if not float(orig_w)/orig_h==16.0/9.0: # if images are 16/9 yet we do not need to crop
            for (dest_w,dest_h) in list_valid_res:
                valid_h = orig_h*dest_w/orig_w
                # select how to crop
                valid_res.append("scale=%s:%s,crop=%s:%s:0:0" % (dest_w,valid_h,dest_w,dest_h))
                # crop to bottom
                valid_res.append("scale=%s:%s,crop=%s:%s:0:%s" % (dest_w,valid_h,dest_w,dest_h,valid_h-dest_h))
                valid_res.append("scale=%s:%s,crop=%s:%s:0:%s" % (dest_w,valid_h,dest_w,dest_h,(valid_h-dest_h)/2))


        for t in valid_res:
            if t.startswith(text):
                if not state:
                    return t
                else:
                    state -= 1
        #if state > len(valid_res): 
            #state-=1
            #return None
        #else: return valid_res[state]


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
        options = ''
        options += " mf://%s/*%s" % ( self.fields['sourceDir'].value, self.ext )
        options += " -ovc x264 -nosound -noskip -of rawvideo "
        options += " -mf fps=%s"% self.fields['FPS'].value
        options += " -o %s " % self.fields['output'].value
        options += " -aspect %s " % (float(self.orig_w)/float(self.orig_h))
        options += " -x264encopts pass=1:bitrate=5000:crf=20:preset=veryslow" 
        options += " -vf %s " % self.fields['size'].value

        command = "mencoder %s " % options
        print command
        import os
        os.system(command)
        return finish

