__author__ = 'Whitney'

#highThres=
#lowThres=
#maxPixelValue=
#minPixelValue=
#
#newPixelValue=
#
#if newPixelValue <= maxPixelValue & >= minPixelValue
#    do nothing
#if newPixelValue

from cv import CaptureFromFile, CreateImage, QueryFrame, IPL_DEPTH_32F, IPL_DEPTH_8U,\
    GetCaptureProperty, CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT, Zero, Split, CV_RGB2HSV

class backgroundRemover():

    def initCodebook(self,background):
        cap = CaptureFromFile(background)
        frame = QueryFrame(cap)

        size = (int(GetCaptureProperty(cap, CV_CAP_PROP_FRAME_WIDTH)),
                int(GetCaptureProperty(cap, CV_CAP_PROP_FRAME_HEIGHT)))

        # split here doesn't work because can't add these values to IPLImage
        # need to create a different matrix strucutre? 
        frame.R = CreateImage(size,IPL_DEPTH_32F,1)
        frame.G = CreateImage(size,IPL_DEPTH_32F,1)
        frame.B = CreateImage(size,IPL_DEPTH_32F,1)

        Split(frame,frame.R,frame.G,frame.B, None)

        # so this probably won't work either
        cb = CreateImage(size,IPL_DEPTH_32F,3)
        cb.R = CreateImage(size,IPL_DEPTH_32F,1)
        cb.G = CreateImage(size,IPL_DEPTH_32F,1)
        cb.B = CreateImage(size,IPL_DEPTH_32F,1)

        # no such thing as p in frame. how do access pixels? 
        # whether to access pixels? 
        cb.R.max=frame.R
        cb.R.min=frame.R

        cb.G.max=frame.G
        cb.G.min=frame.G

        cb.B.max=frame.B
        cb.B.min=frame.B

        self.cb = cb
        self.bgCap = cap

    def updateCodebook(self,background):
        threshold = 5
        frame = QueryFrame(self.bgCap)
        cb = self.cb

        while frame:
            Split(frame,frame.R,frame.G,frame.B, None)


            e = 0
            while e:
                if frame.R <= cb.R[e].max & frame.R >=cb.R[e].min:
                    break
                elif frame.R - cb.R[e].max <= threshold:
                    cb.R[e].max = frame.R
                elif cb.R[e].min - frame.R <= threshold:
                    cb.R[e].min = frame.R

                elif frame.R - cb.R[e].max > threshold:
                    e +=1
                    cb.R[e].max = frame.R
                    cb.R[e].min = frame.R
                elif cb.R[e].min - frame.R > threshold:
                    e +=1
                    cb.R[e].max = frame.R
                    cb.R[e].min = frame.R


            e = 0
            while e:
                if frame.G <= cb.G[e].max & frame.G >=cb.G[e].min:
                    break
                elif frame.G - cb.G[e].max <= threshold:
                    cb.G[e].max = frame.G
                elif cb.G[e].min - frame.G <= threshold:
                    cb.G[e].min = frame.G

                elif frame.G - cb.G[e].max > threshold:
                    e +=1
                    cb.G[e].max = frame.G
                    cb.G[e].min = frame.G
                elif cb.G[e].min - frame.G > threshold:
                    e +=1
                    cb.G[e].max = frame.G
                    cb.G[e].min = frame.G

            e = 0
            while e:
                if frame.B <= cb.B[e].max & frame.B >=cb.B[e].min:
                    break
                elif frame.B - cb.B[e].max <= threshold:
                    cb.B[e].max = frame.B
                elif cb.B[e].min - frame.B <= threshold:
                    cb.B[e].min = frame.B

                elif frame.B - cb.B[e].max > threshold:
                    e +=1
                    cb.B[e].max = frame.B
                    cb.B[e].min = frame.B
                elif cb.B[e].min - frame.B > threshold:
                    e +=1
                    cb.B[e].max = frame.B
                    cb.B[e].min = frame.B

        self.cb = cb



if __name__=="__main__":
    learningVideo = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort_ROI"
    #dataVideo = "/Users/Whitney/Temp/AerialClips/dolphinAerialShort_ROI"
    #output = "/Users/Whitney/Temp/AerialClips/dolphinBackground_codebook"

    br = backgroundRemover()
    br.initCodebook(learningVideo)
    br.updateCodebook(learningVideo)