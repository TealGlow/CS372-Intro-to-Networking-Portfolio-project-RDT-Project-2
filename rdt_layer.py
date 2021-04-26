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
    currentWindowStart = 0          # starting index for the window
    currentWindowEnd = 4            # ending index for current window
    currentSeqNum = 0
    prevAck = 0
    serverData = []

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
        # ############################################################################################################ #
        return ""

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

        seqnum = self.currentSeqNum
        """
        if(len(self.receiveChannel.receiveQueue) > 0):
            # if we got an ack back
            seqnum += 1
            self.currentSeqNum += 1
        """
        if (self.dataToSend != "" and seqnum < len(split_data)):
            segmentSend = Segment()
            # if there is data to send, we make that into a packet of size 4 and send that
            # we then need to make sure that it keeps doing this

            # window will be 5 items long (5 packets) because each packet has a size of 4 characters
            # 15 / 4 = 3.75 and I am rounding up

            data = split_data[seqnum]
            segmentSend.setData(seqnum, data)
            seqnum += 1

            # since I am sending off 4 segments at once, I need to make sure that I receive an ACK before
            # sending 4 segments off again!
            segmentSend.setStartIteration(self.currentIteration)
            segmentSend.setStartDelayIteration(4)
            self.sendChannel.send(segmentSend)
            self.currentSeqNum += 1
        else:
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
        segmentAck = Segment()                  # Segment acknowledging packet(s) received

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        print('processReceive(): Complete this...')

        if(len(listIncomingSegments)>0):
            # if we have received data, we need to deal with them and send back an ack
            currentAck = listIncomingSegments[0].seqnum
            for i in range(0, len(listIncomingSegments)):
                # go through each incoming segment
                print(listIncomingSegments[i].payload)

                segmentAck.setAck(currentAck)
                currentAck += 1
        self.sendChannel.send(segmentAck) # should send cumulative acknum
        print(segmentAck.acknum,segmentAck.seqnum, segmentAck.payload)





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
