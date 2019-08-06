#!/usr/bin/env python

from __future__ import absolute_import
import time

from .lib.feedbackcontroller import FeedbackController
from .lib import bcixml


play_signal = bcixml.BciSignal(None, [bcixml.CMD_PLAY], bcixml.INTERACTION_SIGNAL)
    
    

def main():
    fc = FeedbackController()
    feedbacks = fc.fbProcCtrl.get_feedbacks()
    
    for fb in feedbacks:
        print "Starting %s" % fb
        fc.fbProcCtrl.start_feedback(fb)
        
        fc.handle_signal(play_signal)
        time.sleep(1)
        
        print "Stopping %s" % fb
        fc.fbProcCtrl.stop_feedback()
        
        failstop = []
        try:
            if fc.fbProcCtrl.currentProc.is_alive():
                failstop.append(fb)
        except:
            pass
        

    print "Done testing Feedbacks, the following feedbacks failed to stop correctly:"
    for fb in failstop:
        print fb
    
    


if __name__ == "__main__":
    main()
