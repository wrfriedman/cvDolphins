'''
Created on Feb 10, 2012
  
@authors: Whitney Friedman and Edwin Hutchins
A module to read frames from a video file and write a new video consisting of frames 
that include a prespecified ROI
'''

from cv import QueryFrame, CaptureFromFile, CreateVideoWriter, NamedWindow, GetCaptureProperty, \
CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT, CV_CAP_PROP_FPS, SetImageROI, GetSize, CreateImage, ShowImage, \
DestroyWindow, WriteFrame, Copy, ResetImageROI, CV_CAP_PROP_FOURCC, WaitKey

def extractROI(videoIn, videoOut, ROI):
    '''Read from videoIn, select pixels in ROI (a region) and write to videoOut '''
    
    cap = CaptureFromFile(videoIn)
    fourcc=int(GetCaptureProperty(cap,CV_CAP_PROP_FOURCC))
    print fourcc
    writer = CreateVideoWriter(videoOut,fourcc,GetCaptureProperty(cap,CV_CAP_PROP_FPS),(ROI[2],ROI[3]),is_color=1)
    NamedWindow("regionView")
    
    frame = QueryFrame(cap)
    
    while frame:
        SetImageROI(frame,ROI)
        size = GetSize(frame)
        region = CreateImage(size,frame.depth,frame.channels)
        Copy(frame,region)
        
        ShowImage("regionView",region)
        key=WaitKey(1)
        
        WriteFrame(writer,region)
        
        ResetImageROI(frame)
        frame = QueryFrame(cap)
        
    DestroyWindow("regionView")
    print 'File written to: '
    print videoOut
    
if __name__ == "__main__":
    input = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort.mov"
    output = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort_ROI"
    roi = (600,125,550,450) # cvRect(int x; int y; int width; int height)
    extractROI(input, output, roi)
    
    