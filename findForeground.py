'''
Created on Sep 27, 2011

@author: hutchins
(modified by whitney on 4/19)
'''

from cv import CreateImage, IPL_DEPTH_32F, Zero, IPL_DEPTH_8U, ConvertScale, Acc, Abs, Split,\
    Copy, AbsDiff, Add, Sub, AddS, Scalar, CvtScale, InRange, Or, SubRS, CaptureFromFile, CaptureFromCAM,\
    QueryFrame, NamedWindow, MorphologyEx, ShowImage, DestroyWindow, WaitKey, SaveImage, CV_MOP_OPEN, CV_MOP_CLOSE,\
    GetCaptureProperty, CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT, GetSize, WriteFrame,CV_CAP_PROP_FOURCC,\
    CreateVideoWriter,CV_CAP_PROP_FPS


class backgroundRemover():
    targetCapture = None
    backgroungCapture = None
    size = (550, 480)  # a placeholder.  Setup gets this from the backgroundCapture. 
    cleanupIterations = 2

    def setup(self, background, target):
        #===============================================================================
        # Setting up as globals all of the images that will be needed.
        #===============================================================================
        self.backgroundCapture = CaptureFromFile(background)
        self.targetCapture = CaptureFromFile(target)
        self.size = (int(GetCaptureProperty(self.backgroundCapture, CV_CAP_PROP_FRAME_WIDTH)),
                     int(GetCaptureProperty(self.backgroundCapture, CV_CAP_PROP_FRAME_HEIGHT)))
        print self.size
        self.IavgF = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.IdiffF = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.IprevF = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.IhiF = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.IlowF = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.Ilow1 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Ilow2 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Ilow3 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Ihi1 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Ihi2 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Ihi3 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        Zero(self.IavgF)
        Zero(self.IdiffF)
        Zero(self.IprevF)
        Zero(self.IhiF)
        Zero(self.IlowF)
        self.Icount = 0.00001  #protect against divide by zero

        self.Iscratch = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.Iscratch2 = CreateImage(self.size, IPL_DEPTH_32F, 3)
        self.Igray1 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Igray2 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Igray3 = CreateImage(self.size, IPL_DEPTH_32F, 1)
        self.Imaskt = CreateImage(self.size, IPL_DEPTH_8U, 1)
        Zero(self.Iscratch)
        Zero(self.Iscratch2)

    #===========================================================================
    # Learning the background  
    #===========================================================================
    def accumulateBackground(self, I):
        '''Learn background statistics for one more frame. 
        Run this across all frames from the video. A more complex version could take a sample of frames.'''
        ConvertScale(I, self.Iscratch, 1, 0) #convert the input image to floating point 
        Acc(self.Iscratch, self.IavgF)  #accumulate the images
        AbsDiff(self.Iscratch, self.IprevF, self.Iscratch2)  #compute the differences between current and previous image. 
        Acc(self.Iscratch2, self.IdiffF) #accumulate the differences
        self.Icount += 1
        Copy(self.Iscratch, self.IprevF)


    def setHighThreshold(self, scale):
        ConvertScale(self.IdiffF, self.Iscratch, scale)
        Add(self.Iscratch, self.IavgF, self.IhiF)
        Split(self.IhiF, self.Ihi1, self.Ihi2, self.Ihi3, None)

    def setLowThreshold(self, scale):
        ConvertScale(self.IdiffF, self.Iscratch, scale)
        Sub(self.IavgF, self.Iscratch, self.IlowF)
        Split(self.IlowF, self.Ilow1, self.Ilow2, self.Ilow3, None)

    def createModelsfromStats(self):
        '''Compute the expected ranges of values for each pixel.  Average +/- scaled difference from average.'''
        ConvertScale(self.IavgF, self.IavgF, 1.0/self.Icount)
        ConvertScale(self.IdiffF, self.IdiffF, 1.0/self.Icount)

        AddS(self.IdiffF, Scalar(1.0, 1.0, 1.0), self.IdiffF)
        self.setHighThreshold(4.0)
        self.setLowThreshold(4.0)

        #===========================================================================
        # Computing the difference between what's in the frame and the background -> Imask pixels containing foreground information
        #===========================================================================
    def backgroundDiff(self, I, Imask):
        '''Create a binary 0,255 mask where 255 means foreground pixel. I is input image 3-channel, 8U; Imask to be created is 1-ch, 8u'''

        CvtScale(I, self.Iscratch, 1.0)  #Convert to I to float
        Split(self.Iscratch, self.Igray1, self.Igray2, self.Igray3, None) #split out the channels

        #===========================================================================
        # For each channel find pixels in the current image that are in the expected ranges and accumulate those pixels in the mask
        #===========================================================================
        #channel 1
        InRange(self.Igray1, self.Ilow1, self.Ihi1, Imask)
        #channel 2
        InRange(self.Igray2, self.Ilow2, self.Ihi2, self.Imaskt)
        Or(Imask, self.Imaskt, Imask)
        #channel 3
        InRange(self.Igray3, self.Ilow3, self.Ihi3, self.Imaskt)
        Or(Imask, self.Imaskt, Imask)

        #Imask is the background, so invert the result to get the foreground

        SubRS(Imask, 255, Imask)

        return Imask

        #===========================================================================
        # This mask, one for every frame in the movie, can be used to do object detection processing. 
        # Probably should do open and close morphology 
        # on it before finding blobs and labeling their centers.  
        # Could be used to filter the original movie frames showing dolphins only, we hope. 
        #===========================================================================



    def learnBackground(self, learningVideo):
        cap = self.backgroundCapture
        #        self.size = (int(GetCaptureProperty(cap, CV_CAP_PROP_FRAME_WIDTH)),
        #                     int(GetCaptureProperty(cap, CV_CAP_PROP_FRAME_HEIGHT)))

        #=======================================================================
        # Learn the background
        #=======================================================================

        frame = QueryFrame(cap)
        ConvertScale(frame, self.IprevF, 1, 0) #convert the first input image to floating point and save in IprevF so there is a previous

        while frame:
            self.accumulateBackground(frame)
            frame = QueryFrame(cap)

        self.createModelsfromStats()
        print "Background has been learned."


    def findForeground(self, source, videoOut):  #This should operate on real-time camera input.

        if source == -1:
            cap = CaptureFromCAM(source)
        else:
            cap = self.targetCapture

        #=======================================================================
        # Subtract the learned background from each frame of the video and save a mask for each frame
        #=======================================================================
        frame = QueryFrame(cap)
        self.size = GetSize(frame)
        NamedWindow("Mask view")
        #ngMask = CreateImage(GetSize(frame), IPL_DEPTH_8U, 3) 
        Imask = CreateImage(self.size, IPL_DEPTH_8U, 1)
        outImage = CreateImage(self.size, IPL_DEPTH_8U, 1)


        fourcc=int(GetCaptureProperty(cap,CV_CAP_PROP_FOURCC))
        # print fourcc
        writer = CreateVideoWriter(videoOut,fourcc,GetCaptureProperty(cap,CV_CAP_PROP_FPS),self.size,is_color=1)

        while frame:
            newMask = self.backgroundDiff(frame, Imask)

            #===================================================================
            # Here we use morphological operations to clean up the mask
            #===================================================================

            MorphologyEx(newMask, newMask, None, None, CV_MOP_CLOSE, self.cleanupIterations)
            MorphologyEx(newMask, newMask, None, None, CV_MOP_OPEN, self.cleanupIterations)

            ShowImage("Mask View", newMask)
            #WriteFrame(writer,newMask)


            #===================================================================
            # Do the processing to find connected shapes, bounding boxes and centers in newMask
            #===================================================================
            #FindConnectedObjects(newMask, bbs, ctrs)
            #===================================================================
            # Write or return (x, y) for center of first connected shape found in each frame
            #===================================================================

            #            c = WaitKey(10)
            #            if c == 27: break
            key = WaitKey(10)
            if key == 27: # esc
                break
            elif key == 32: # space 
                while True:
                    command = WaitKey(100)
                    if command == 13:  # carriage return
                        print "Saving image"
                        Copy(newMask, outImage)
                        SaveImage("/Users/hutchins/Dropbox/AerialClips/BlobTestFrame.jpg", outImage)
                    elif command == 32 or command == 27:
                        break
            frame = QueryFrame(cap)



        DestroyWindow("regionView")
        print 'File written to: '
        print videoOut


if __name__ == "__main__":

    #===========================================================================
    # Aim the builtin camera at the empty scene and use the captureBackgroundMovie.py module 
    # to capture the background learning video.
    #===========================================================================

    learningVideo = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort_ROI"
    dataVideo = "/Users/Whitney/Temp/AerialClips/dolphinAerialShort_ROI"
    output = "/Users/Whitney/Temp/AerialClips/dolphinBackground_removed"

    #===========================================================================
    # Make a backgroundRemover object.  
    # Then learn the statistics of the background from the learning video.
    # Finally, without moving the builtin camera, find the foreground objects in 
    # the live camera input stream. 
    #===========================================================================

    br = backgroundRemover()
    br.setup(learningVideo, dataVideo)
    br.learnBackground(learningVideo)
    br.findForeground(dataVideo,output)
        
    
    
    
