'''
Created on Feb 28, 2012
 last updated: April 2
@author: friedman
'''

from cv import CaptureFromFile, CreateImage, QueryFrame, IPL_DEPTH_32F, IPL_DEPTH_8U, createImage,\
    GetCaptureProperty, CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT, Zero, Split, CV_RGB2HSV,\
    CaptureFromCAM, getSize, NamedWindow, Max, Min,

class backgroundRemover():

    def setup(self,background,target):
        self.backgroundCapture = CaptureFromFile(background)
        self.targetCapture = CaptureFromFile(target)

        self.size = (int(GetCaptureProperty(self.backgroundCapture, CV_CAP_PROP_FRAME_WIDTH)),
                     int(GetCaptureProperty(self.backgroundCapture, CV_CAP_PROP_FRAME_HEIGHT)))
        self.HSV = createImage(self.size, IPL_DEPTH_32F,3)

        self.H = CreateImage(self.size, IPL_DEPTH_8U,1)
        self.Hmax = CreateImage(self.size, IPL_DEPTH_8U,1)
        self.Hmin = CreateImage(self.size, IPL_DEPTH_8U,1)

        self.S = CreateImage(self.size, IPL_DEPTH_8U,1)
        self.Smax = CreateImage(self.size, IPL_DEPTH_8U,1)
        self.Smin = CreateImage(self.size, IPL_DEPTH_8U,1)

        self.V = CreateImage(self.size, IPL_DEPTH_8U,1)                                                                 PL_DEPTH_8U,1)
        self.Vmax = CreateImage(self.size, IPL_DEPTH_8U,1)
        self.Vmin = CreateImage(self.size, IPL_DEPTH_8U,1)


        #===============================================================================
        # Setup codebook structure by creating some boxes in HSV space
        # self should be the codebook
        #===============================================================================

        # Use the first frame to create the initial codebook, which will be updated by the
        # subsequent frames.
        def createCodebook(self,bgI):
            self.HSV = CV_RGB2HSV(bgI)
        Split(bgI, self.H, self.S, self.V, None) #split out the channels
        # Assign values from the first frame to max & min codebook values
        self.Hmax = Max(self.H)
        self.Hmin = min(self.H)

        self.Smax = self.S
        self.Smin = self.S

        self.Vmax = self.V
        self.Vmin = self.V


        def updateCodebook(self,bgI):
            self.HSV = CV_RGB2HSV(bgI)
        Split(self.HSV, self.H, self.S, self.V, None) #split out the channels
        # probably need an if loop in here, so if the pixel value is high within a learning
        # threshold, (learnHigh, learnLow)
        # elif the pixel value is outside a learning threshold, begin a new codeElement for
        # that pixel location
        if self.Hmax < self.H:
        self.Hmax = self.H
        if self.Hmin > self.H:
        self.Hmin = self.H

        if self.Smax < self.S:
        self.Smax = self.S
        if self.Smin > self.S:
        self.Smin = self.S

        if self.Vmax < self.V:
        self.Vmax = self.V
        if self.Vmin > self.V:
        self.Vmin = self.V


        def learnBackground(self, learningVideo):
            cap = self.backgroundCapture
        bgFrame = QueryFrame(cap)

        createCodebook(bgFrame)

        while bgFrame:
            self.updateCodebook(bgFrame)
        bgFrame = QueryFrame(cap)

        print "Background Codebooks have been created"

        def backgroundDiff(self,fgI):
            fgHSV = createImage(self.size, IPL_DEPTH_32F,3)
        H = CreateImage(self.size, IPL_DEPTH_8U,1)
        S = CreateImage(self.size, IPL_DEPTH_8U,1)
        V = CreateImage(self.size, IPL_DEPTH_8U,1)

        fgHSV = CV_RGB2HSV(fgI)
        Split(fgHSV,H,S,V,None)

        if H>self.Hmin and H<self.Hmax:
        H = 255
        if S>self.Hmin and S<self.Hmax:
        S = 255
        if V>self.Hmin and V<self.Hmax:
        V = 255

        def findForeground(self, fgSource):
            if source ==-1:
        cap = CaptureFromCAM(fgSource) # is this necessary? CaptureFromFile instead?
        else:
        cap = self.targetCapture

        fgFrame = QueryFrame(cap)
        self.size = GetSize(fgFrame)
        NamedWindow("Foreground")

        while fgFrame:
            self.backgroundDiff(fgFrame)

            # Subtract foreground from codebook, show image

            if __name__ == "__main__":

        learningVideo = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort_ROI.mov"
        dataVideo = "/Users/Whitney/Temp/AerialClips/dolphinAerialShort_ROI.mov"

        br = backgroundRemover()
        br.setup(learningVideo,dataVideo)
        br.learnBackground(learningVideo)
        br.findForeground(dataVideo)