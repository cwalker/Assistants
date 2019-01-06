import snowboydecoder
import sys
import signal
import subprocess
from time import  sleep
import sys
import posix_ipc
import json
import time
from MMMApi import MMMApi
from Respeaker import Respeaker

interrupted = False

ALEXA = 0
GOOGLE_ASSISTANT = 1
MMMApiInstance = MMMApi()
RespeakerInstance = Respeaker()

def signal_handler(signal, frame):

    assistantsControl_mq.close()
    posix_ipc.unlink_message_queue("/AssistantsControlQueue")
    global interrupted
    interrupted = True


def interrupt_callback():

    global interrupted
    return interrupted

def alexa_callback():

    print('alexa detected!')
    communicateAssistant(ALEXA)
    print('alexa finished')
    
def google_callback():

    print('google detected!')
    communicateAssistant(GOOGLE_ASSISTANT)
    print('google finished')

    
def communicateAssistant(AssistantNo):

    RespeakerInstance.wakeup(AssistantNo)
    MMMApiInstance.wakeup(AssistantNo)

    # remove a messages of queue if have a message before Assistantcotrol sends wakeup to Assistant
    # (status synchronization)
    if assistantsControl_mq.current_messages != 0:
        # print('assistantsControl_mq is not empty')
        while assistantsControl_mq.current_messages != 0:
            msg = assistantsControl_mq.receive(timeout=3)
            # print(msg)

    print('wakeup')
    assistantMessageQueue[AssistantNo].send('wakeup')
    
    while True:
        try:
            # receive with timeout. 
            # If Assistant already finished. Assistant controller receives no message from Assistant and finishes after timeout.
            msg = assistantsControl_mq.receive(timeout=15)
            if msg[0] == b'finish':
                MMMApiInstance.finish(AssistantNo)
                break
            elif msg[0] == b'speak':
                MMMApiInstance.speak(AssistantNo)
                RespeakerInstance.speak(AssistantNo)
            elif msg[0] == b'think':
                MMMApiInstance.think(AssistantNo)
                RespeakerInstance.think(AssistantNo)
        except posix_ipc.BusyError:
            break
    sleep(0.5)

    RespeakerInstance.off()
    MMMApiInstance.off()

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.6,0.6]
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [alexa_callback, google_callback]
print('Listening... Press Ctrl+C to exit')

assistantMessageQueue = [ posix_ipc.MessageQueue("/AlexaQueue", posix_ipc.O_CREAT),posix_ipc.MessageQueue("/GoogleAssistantQueue", posix_ipc.O_CREAT)]
assistantsControl_mq = posix_ipc.MessageQueue("/AssistantsControlQueue",posix_ipc.O_CREAT,read=True)


# main loop
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

