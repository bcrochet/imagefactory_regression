#!/usr/bin/env python
# encoding: utf-8
#   Copyright 2011 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#        Regression test for Image Factory #bug745445 - Relevant message should be displayed while stopping iwhd.
#        Created by koca (mkoci@redhat.com)
#        Date: 15/12/2011
#        Modified: 15/12/2011
#        Issue: https://bugzilla.redhat.com/show_bug.cgi?id=745445
# return values:
# 0 - OK: everything OK
# 1 - Fail: setupTest wasn't OK
# 2 - Fail: bodyTest wasn't OK
# 3 - Fail: cleanTest wasn't OK
# 4 - Fail: any other error (reserved value)

#necessary libraries
import os
import sys
from syck import *
configuration = load(file("configuration.yaml", 'r').read())
#constants 
SUCCESS=0
FAILED=1
RET_SETUPTEST=1
RET_BODYTEST=2
RET_CLEANTEST=3
RET_UNEXPECTED_ERROR=4
ROOTID=0
#setup
LogFileIWH=configuration["LogFileIWH"]

def setupTest():
    print "=============================================="
    print "Setup of the regression test based on bug745445 - Relevant message should be displayed while stopping iwhd"
    print "See the bug for further information - https://bugzilla.redhat.com/show_bug.cgi?id=745445"
    print "Checking if you have enough permission..."
    if os.geteuid() != ROOTID:
        print "You must have root permissions to run this script, I'm sorry buddy"
        return False #exit the test
    print "Cleanup configuration...."
    print "Clearing log file for Image Warehouse"
    os.system("> " + LogFileIWH)
    return True
   
#body
def bodyTest():
#check if aeolus-cleanup removes directory. /var/tmp and /var/lib/iwhd/images
    print "=============================================="
    print "test being started"
    print "stopping/starting iwhd daemon and expecting relevant message... "
    if os.system("service iwhd stop|grep \"Stopping iwhd\" ") == SUCCESS:
        if os.system("service iwhd start|grep \"Starting iwhd\" ") == SUCCESS:
            return True
    print "See the "+LogFileIWH+" file: "
    outputtmp = os.popen("cat " + LogFileIWH).read()
    print outputtmp
    return False
 
#cleanup after test
def cleanTest():
    print "=============================================="
    print "Cleaning the mess after test"    
    return True
 
#execute the tests and return value (can be saved as a draft for future tests)
if setupTest(): 
    if bodyTest():
        if cleanTest():
            print "=============================================="
            print "Test PASSED entirely !"
            sys.exit(SUCCESS)
        else:
            print "=============================================="
            print "Although Test was successful, cleaning after test wasn't successful !"
            sys.exit(RET_CLEANTEST)
    else:
        print "=============================================="
        print "Test Failed !"
        cleanTest()
        sys.exit(RET_BODYTEST)
else:
    print "=============================================="
    print "Test setup wasn't successful ! Test didn't even proceed !"
    cleanTest()
    sys.exit(RET_SETUPTEST)
