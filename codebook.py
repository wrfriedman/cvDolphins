'''
Created on Feb 28, 2012
Last Modified: April 12, 2012

@author: friedman
'''

from cv import

class backgroundRemover():

    def defCodebook(self, channels):
    #===============================================================================
    # Setup codebook structure by creating some boxes in YUV space
    # self should be the codebook
    #===============================================================================

        self.codeElement = None
        self.numEntries = None # track how many codebook entries we have

        # these seem like they need to be part of a different function
        self.HiCh = learnHigh(channels)
        self.LoCh = learnLow(channels)
        self.max = max(channels)
        self.min = min(channels)


    def learnHigh(self):


    def learnLow(self):

    def updateCodebook(self,p,c,cbBounds,numChannels):
    #===========================================================================
    # for each pixel, updateCodebook()is called for as many images as are sufficient
    # to capture the relevant changes in the background.
    # Updates the codebook entry with a new data point (element)
    #===========================================================================

        return codebookIndex


    def clearStaleEntries(self):
    #===========================================================================
    # clearStaleEntries() can be used to learn the background in the presence of
    # (small numbers of) moving foreground objects. this is possible because
    # the seldom used "stale" entries induced by a moving foreground will be deleted
    #===========================================================================

    def learnBackground(self,learningVideo):
        cap = self.backgroundCapture

if __name__ == "__main__":

    learningVideo = "/Users/Whitney/Temp/AerialClips/dolphinBackgroundShort_ROI.mov"
    dataVideo = "/Users/Whitney/Temp/AerialClips/dolphinAerialShort_ROI.mov"

    br = backgroundRemover()
    br.setup(learningVideo, dataVideo)
    br.learnBackground(learningVideo)
    br.findForeground(dataVideo)