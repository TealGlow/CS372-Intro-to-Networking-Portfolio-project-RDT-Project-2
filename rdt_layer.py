from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed
    currentWindow =[0,4]
    currentSeqNum = 0
    expectedAck = 4
    iterationsWithoutAck = 0
    serverData = []
    resendWindow = False

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed
        self.countSegmentTimeouts = 0
        self.currAck = 0
        self.winStart = 0
        self.winEnd = 4
        self.role = "server"
        self.waitTime = 0
        currentWindowStart = 0  # starting index for the window
        currentWindowEnd = 4  # ending index for current window

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...
        print('getDataReceived(): Complete this...')
        sortedData = sorted(self.serverData)
        print("SERVER DATA",self.serverData)
        print("SORTED SERVER DATA", sortedData)
        sortedString = ""
        for i in range(len(sortedData)):
            sortedString += sortedData[i][1]
        # ############################################################################################################ #
        return sortedString

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):

        # ############################################################################################################ #
        print('processSend(): Complete this...')
        if(self.dataToSend != ""):
            self.role = "Client"
        print("ROLE", self.role)
        print("CURRENT WINDOW", self.currentWindow)

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        # splitting data string into segments of size self.DATA_LENGTH from
        # https://pythonexamples.org/python-split-string-into-specific-length-chunks/
        split_data = [self.dataToSend[i:i + self.DATA_LENGTH] for i in range(0, len(self.dataToSend), self.DATA_LENGTH)]


        # professor says from the ED discussions https://edstem.org/us/courses/5258/discussion/392838:
        # look if there is something in queue to send
        # create the segment
        # send the segment


        print(self.receiveChannel.receiveQueue,"hi")
        if(self.currentIteration > 1 and len(self.receiveChannel.receiveQueue ) == 0):
            # if we have gone 1 iteration without an ack we resend current window
            print("No ACK, resending current window")
            if(self.waitTime == 3):
                # resend the window if we hit the timeout window
                self.currentSeqNum = self.currentWindow[0]
            else:
                print("Waiting")
                self.waitTime += 1
                return


        if (len(self.receiveChannel.receiveQueue) > 0 and self.role == "Client"):
            # if the rec queue has an item in it
            # DO NOT BASE IT ON THE FIRST ITEM BEING AN ACK
            #if (self.receiveChannel.receiveQueue[0].acknum != -1):
                # if the received channel first item is an ack
            acklist = self.receiveChannel.receive() # check the entire acklist
            self.checkReceivedAck(acklist)

        # else set the seqnum that we are iterating thru to the currentSeqNum
        seqnum = self.currentSeqNum  # set up the current seqnum
        self.winStart = seqnum
        self.winEnd = seqnum + 4

        if(self.role != "server"):



            print("SENDING WINDOW", self.winStart, self.winEnd)
            self.sendData(self.winStart, self.winEnd, seqnum, split_data)



    def checkReceivedAck(self, toCheck):
        """
        Checks the acknums if any of them is the expected acknum then advance the window
        :param toCheck:
        :return:
        """
        # gets an array of the received data
        for i in range(0, len(toCheck)):
            print(toCheck[i].acknum)
            if(toCheck[i].acknum == self.expectedAck):
                self.currentSeqNum += 4
                self.expectedAck += 4
                self.currentWindow[0] += 4
                self.currentWindow[1] += 4
        return


    def sendData(self, wStart, wEnd, seqnum, dataArr):
        """
        Iterates through a loop, makes the packet of items from window start to window end and sends them on the
        channel.

        :param wStart:
        :param wEnd:
        :param seqnum:
        :param dataArr:
        :return:
        """
        for i in range(wStart, wEnd):
            if (self.dataToSend != "" and seqnum < len(dataArr)):
                segmentSend = Segment()
                # if there is data to send, we make that into a packet of size 4 and send that
                # we then need to make sure that it keeps doing this

                # window will be 5 items long (5 packets) because each packet has a size of 4 characters
                # 15 / 4 = 3.75 and I am rounding up

                # packet data, packet num in sequence, current window start (index in data that we started), current window end, True if data packet

                #data = [split_data[seqnum],i, self.currentWindowStart, self.currentWindowEnd, True]
                data = dataArr[seqnum]
                segmentSend.setData(seqnum, data)
                seqnum += 1

                # since I am sending off 4 segments at once, I need to make sure that I receive an ACK before
                # sending 4 segments off again!
                segmentSend.setStartIteration(self.currentIteration)
                segmentSend.setStartDelayIteration(4)
                self.sendChannel.send(segmentSend)
                #self.currentSeqNum += 1
        return


    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):



        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        print('processReceive(): Complete this...')
        print(listIncomingSegments)



        if(len(listIncomingSegments) > 0):
            segmentAck = Segment()  # Segment acknowledging packet(s) received

            print("THINGS ARE HAPPENING)")
            self.tempDisplayDataRec(listIncomingSegments)
            currentAck = self.currentWindow[0]
            self.expectedAck = self.currentWindow[1]
            print("CURRENTACK", currentAck)

            newList, recAck = self.processReceivedList(listIncomingSegments) # returns a processed list of packets we actually got
            # check if what we are receiving is an ack,
            # if the item is an ack, then do nothing
            # if the item was not an ack, send an ack
            print("RECACK", recAck)
            currentAck += recAck
            print(currentAck, self.expectedAck)


            if(currentAck == self.expectedAck):
                print("advancing the window")
                self.winStart += 4
                print(self.winStart)
                self.currAck = self.currAck + 4
                #self.addNewListToServerData(newList)
                #segmentAck.setAck(currentAck)
                #self.sendChannel.send(segmentAck)  # should send cumulative acknum
                self.addNewListToServerData(newList)
                segmentAck.setAck(currentAck)
                self.sendChannel.send(segmentAck)  # should send cumulative acknum
            #else:
            #    currentAck -= 4
        else:
            return




        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?
        #print('processReceive(): Complete this...')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...



        # ############################################################################################################ #
        # Display response segment
        #segmentAck.setAck(acknum)
        #print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
        #self.sendChannel.send(segmentAck)


    def tempDisplayDataRec(self, toDisplay):
        """
        Function that displays the current payloads for all the items in the list if they exist
        :param toDisplay:
        :return:
        """
        for i in range(len(toDisplay)):
            if(toDisplay[i].payload !=""):
                print(toDisplay[i].seqnum,toDisplay[i].payload)


    def processReceivedList(self, toProcess):
        """
        Function that removes duplicate items, and items that do not pass the check sum, returns the list of
        unique items along with the acknum
        :param toProcess:
        :return:
        """
        uniqueToProcess = []
        temp = []
        newList = []
        prevData=""
        newAck = self.winStart

        for i in range(len(toProcess)):
            if(toProcess[i].payload != ""):
                # if the payload is not an ack, keep it
                temp.append(toProcess[i])

        for j in range(len(temp)):
            if(temp[j].checkChecksum() == True):
                # if it passes the checksum
                uniqueToProcess.append(temp[j])
        print("displaying uni", uniqueToProcess)
        self.tempDisplayDataRec(uniqueToProcess)
        temp = []
        for h in range(len(uniqueToProcess)):
            # if it belongs in this window
            if(self.currentWindow[0]<=(uniqueToProcess[h].seqnum)<= self.currentWindow[1]):
                temp.append(uniqueToProcess[h])
        print("TEMP", temp)
        uniqueToProcess = []
        for n in range(len(temp)):
            if(temp[n] not in newList):
                newList.append(temp[n])

        if(len(newList) > 4):
            return newList, 0
        print("NEW LEN", len(newList))
        return newList, len(newList)




    def addNewListToServerData(self, toAdd):
        """
        Goes through the list passed in and adds it to the server data variable with
        sequence number and payload so that it can be sorted
        :param toAdd:
        :return:
        """
        print("TO ADD", toAdd)
        for i in range(len(toAdd)):
            if ([toAdd[i].seqnum, toAdd[i].payload] not in self.serverData):
                self.serverData.append([toAdd[i].seqnum, toAdd[i].payload])