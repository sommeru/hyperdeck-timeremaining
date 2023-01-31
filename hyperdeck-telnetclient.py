#!/usr/bin/env python

import socketio
import socket
from datetime import datetime
import time

broker_url = 'http://127.0.0.1:1313/'
hyperdeck_url = '10.0.1.40'
hyperdeck_port = 9993

sio = socketio.Client()

@sio.event
def connect():
    print('connected to socketio broker')

def get_current_time():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    # connect to remote host
    try :
        s.connect((hyperdeck_url, hyperdeck_port))
    except :
        print ('Unable to connect')
        return (0, 0, '', 'noconnection')

    #print ('Connected to remote host')

    def readline():
        request_line = b''
        while not request_line[-1:] == b'\n':        
            request_line += s.recv(1)
        return (request_line)

    def readblock(message):
        s.sendall(message)
        endoftranfer = False    
        block = []
        while endoftranfer == False:
            try:
                line = readline()
                #print (line)
            except TimeoutError as e:
                print(e)
                endoftranfer = True
                return (0, 0, '', 'error')
            if (line == b'\r\n'):
                endoftranfer = True
                return(block)
            else:
                block.append(line)            

    # Initializing the connection 
    answer = readblock(b'')

    answer = readblock(b'clips get\r\n')
    clips = []
    for line in answer:        
        try:
            line = line.decode(encoding='UTF-8',errors='ignore')
            filenumber = int(line.split(':',1)[0].strip())        
            line = line.split(':',1)[1].strip()
            filename = line.split(' ')[0].strip()
            starttime = line.split(' ')[1].strip()
            stoptime = line.split(' ')[2].strip()
            starttime = datetime.strptime(starttime[:-3], "%H:%M:%S") - datetime.strptime("00:00:00","%H:%M:%S")
            duration = datetime.strptime(stoptime[:-3], "%H:%M:%S") - datetime.strptime("00:00:00","%H:%M:%S")

            #clips.append([filenumber,filename,starttime,duration])
            clips.append({'filenumber': filenumber, 'filename': filename, 'starttime': starttime, 'duration': duration})
        
        except ValueError as e:
            pass

        except Exception as e:
            return (0, 0, '', 'error')        

    answer = readblock(b'transport info\r\n')
    #print (answer)


    for line in answer:
        try:
            line = line.decode(encoding='UTF-8',errors='ignore')    
            if line.startswith('status'):
                status = line.split(':',1)[1].strip()
                #print("Status: " + status)
            if line.startswith('clip id'):
                clipid = int(line.split(':',1)[1].strip())
                #print("Clip id: " + str(clipid))
            if line.startswith('timecode'):
                line = line.split(':',1)[1].strip()
                timecode = datetime.strptime(line[:-3], "%H:%M:%S") - datetime.strptime("00:00:00","%H:%M:%S")        
                #print("Timecode: " + str(timecode))
                duration = clips[clipid-1]['duration']
                time_elapsed = timecode - clips[clipid-1]['starttime']
                time_remaining = duration - time_elapsed
                file_name = clips[clipid-1]['filename']
                print(status + " - timeremaining: " + str(time_remaining.total_seconds()) + 's')
        except Exception as e:
            return (0, 0, '', 'error')

    return (time_remaining.total_seconds(), duration.total_seconds(), file_name, status)

sio.connect(broker_url)

while True:
    try:
        (remaining, duration, filename, status) = get_current_time()
        json = {
            'remaining': remaining,
            'duration': duration,
            'filename': filename,
            'status': status
        }
        sio.emit('send_update', json)
    except Exception as e:
        raise
        print(e)
    time.sleep(1)