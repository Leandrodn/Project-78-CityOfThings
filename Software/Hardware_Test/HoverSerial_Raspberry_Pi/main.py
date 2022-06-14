from HoverSerial import*
import time

#Constants
SERIAL_PORT = '/dev/serial0'
SERIAL_BAUD = 115200
HOVER_SERIAL = Hoverboard_serial (SERIAL_PORT, SERIAL_BAUD)

SPEED_MAX_TEST = 300 
SPEED_STEP = 2  
TIME_SEND = 0.2 

#Variables
stepCount, steer, speed, startTime = 0 * 4

try:
    while True:
    #Send Data:
        elapsedTime = time.time() - startTime
        if elapsedTime < TIME_SEND:
            continue
        startTime = time.time()

        # Calculate test command speed
        speed = SPEED_MAX_TEST - 2 * abs(stepCount)

        # Send commands
        HOVER_SERIAL.send_command(steer, speed)
        print('Sending:\tsteer: '+str(steer)+'speed: '+str(speed))

        # invert step if SPEED_MAX_TEST is reached
        stepCount += SPEED_STEP
        if (stepCount >= SPEED_MAX_TEST or stepCount <= -SPEED_MAX_TEST):
            step = -step
            
        #Receive Data
        feedback = HOVER_SERIAL.receive_feedback()

        if feedback == None: #no feedback> -> go to next loop iteration
            continue
        
        print('Receiving:\t', feedback)
    
except KeyboardInterrupt:
    print("Keyboard interrupt...")

except Exception as e:
    print("Error: " + str(e))

finally:
    HOVER_SERIAL.close()
