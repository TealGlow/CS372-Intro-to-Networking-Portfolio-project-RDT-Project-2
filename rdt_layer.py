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
        self.role = "server"
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

        """
        if(len(self.receiveChannel.receiveQueue) > 0):
            if(self.receiveChannel.receiveQueue[0].acknum != -1):
                self.role = "client"
                # if this is the client
                acklist = self.receiveChannel.receive()
                print(acklist[0].acknum,len(acklist), self.expectedAck)
                if(acklist[0].acknum != self.expectedAck):
                    print("resending window")
                    self.currentSeqNum = self.currentWindowStart
                    self.expectedAck = self.currentSeqNum + 4
                else:
                    self.expectedAck += 4
        elif(len(self.receiveChannel.receiveQueue) == 0 and self.currentIteration >1 and self.role !="server"):
            print("resending window")
            # we did not rec an ack, it was dropped
            self.currentSeqNum = self.currentWindowStart
        """
        print(self.receiveChannel.receiveQueue)
        if(self.currentIteration > 1 and len(self.receiveChannel.receiveQueue ) == 0):
            # if we have gone 1 iteration without an ack we resend current window
            print("No ack, resending current window")
            self.currentSeqNum = self.currentWindowStart
            #self.role = "Client"
        if (len(self.receiveChannel.receiveQueue) > 0):

            if (self.receiveChannel.receiveQueue[0].acknum != -1):
                print("checking")
                acklist = self.receiveChannel.receive()
                # TODO: advancing window too far
                self.checkReceivedAck(acklist)
        #        self.role = "client"

        seqnum = self.currentSeqNum  # set up the current seqnum
        self.currentWindowStart = seqnum
        self.currentWindowEnd = seqnum + 4

        if(self.role != "server"):



            print("SENDING WINDOW", self.currentWindowStart, self.currentWindowEnd)
            # TODO: make sure only the client sends these
            # TODO: stop the window from advancing every time
            self.sendData(self.currentWindowStart, self.currentWindowEnd, seqnum, split_data)
        """
        for i in range(self.currentWindowStart, self.currentWindowEnd):
            if (self.dataToSend != "" and seqnum < len(split_data)):
                segmentSend = Segment()
                # if there is data to send, we make that into a packet of size 4 and send that
                # we then need to make sure that it keeps doing this

                # window will be 5 items long (5 packets) because each packet has a size of 4 characters
                # 15 / 4 = 3.75 and I am rounding up

                # packet data, packet num in sequence, current window start (index in data that we started), current window end, True if data packet

                #data = [split_data[seqnum],i, self.currentWindowStart, self.currentWindowEnd, True]
                data = split_data[seqnum]
                segmentSend.setData(seqnum, data)
                seqnum += 1

                # since I am sending off 4 segments at once, I need to make sure that I receive an ACK before
                # sending 4 segments off again!
                segmentSend.setStartIteration(self.currentIteration)
                segmentSend.setStartDelayIteration(4)
                self.sendChannel.send(segmentSend)
                self.currentSeqNum += 1
                #self.expectedAck += 1
        """

        #else:
        #    print("Sending nothing")
        #    return


    def checkReceivedAck(self, toCheck):
        # gets an array of the received data
        for i in range(0, len(toCheck)):
            if(toCheck[i].acknum == self.expectedAck):
                self.currentSeqNum += 4
                self.expectedAck+=4
        return True


    def sendData(self, wStart, wEnd, seqnum, dataArr):
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
                self.currentSeqNum += 1
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
            currentAck = self.currentWindowStart

            newList, currentAck = self.processReceivedList(listIncomingSegments) # returns a processed list of packets we actually got
            # check if what we are receiving is an ack,
            # if the item is an ack, then do nothing
            # if the item was not an ack, send an ack
            #currentAck += len(newList)
            print(currentAck, self.expectedAck)


            if(currentAck == self.expectedAck):
                print("advancing the window")
                self.currentWindowStart += 4
                self.expectedAck += 4
                self.addNewListToServerData(newList)
                segmentAck.setAck(currentAck)
                self.sendChannel.send(segmentAck)  # should send cumulative acknum
            #else:
            #    currentAck -= 4
        else:
            return
        """
        resendWindow = False

        if(len(listIncomingSegments)>0):
            # if we have received ANYTHING deal with it here

            currentAck = self.winStart
            print(currentAck)
            #currentAck = self.serverData[len(self.serverData)-1]
            prevData = ""
            segmentAck = Segment()  # Segment acknowledging packet(s) received
            print("QUEUE LENGTH", len(listIncomingSegments))
            for i in range(0, len(listIncomingSegments)):
                currentData = listIncomingSegments[i].payload
                if (listIncomingSegments[i].payload != ""):
                    print(listIncomingSegments[i].payload, listIncomingSegments[i].checkChecksum())
                    print("GOING TO ACK")


                    if (listIncomingSegments[i].checkChecksum() and currentData != prevData):
                        # checksum passed, and the data is unique in the current window
                        # if(listIncomingSegments[i].seqnum == prevSeqNum+1 or prevSeqNum == listIncomingSegments[i].seqnum):
                        #    print("prev ack passed")
                        currentAck += 1

                        if ([listIncomingSegments[i].seqnum, listIncomingSegments[i].payload] not in self.serverData):
                            self.serverData.append([listIncomingSegments[i].seqnum, listIncomingSegments[i].payload])
                    prevData = currentData

            print(currentAck, self.winStart)
            if(currentAck % 4 == 0 and currentAck != 0 and resendWindow == False):
                self.currAck += 4
                self.currentWindowStart = self.currentWindowEnd
                self.currentWindowEnd +=4
                self.winStart +=4
            segmentAck.setAck(currentAck)
            self.sendChannel.send(segmentAck)  # should send cumulative acknum

        else:
            # has not received anything do nothing
            return

        """




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



    def processReceivedList(self, toProcess):
        newList = []
        prevData=""
        newAck = self.currentWindowStart

        for i in range(len(toProcess)):
            currentData = toProcess[i].payload
            if(toProcess[i].payload != "" and toProcess[i].checkChecksum() and prevData != currentData):
                newAck += 1
                newList.append(toProcess[i])

            prevData = currentData

        return newList, newAck



    def addNewListToServerData(self, toAdd):
        print("TO ADD", toAdd)
        for i in range(len(toAdd)):
            if ([toAdd[i].seqnum, toAdd[i].payload] not in self.serverData):
                self.serverData.append([toAdd[i].seqnum, toAdd[i].payload])