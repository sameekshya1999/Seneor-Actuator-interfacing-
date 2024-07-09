
import RPi.GPIO as GPIO  
import time

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
LED = 17

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

def get_distance():
    """Measure and return the distance from the ultrasonic sensor."""
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    
    # Send a short pulse to trigger the measurement
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    # Wait for the echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    # Wait for the echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound at sea level: 34300 cm/s
    return distance

try:
    while True:
        distance = get_distance()
        if distance <= 5:
            # If an obstacle is detected within 5 cm, turn on the LED
            GPIO.output(LED, True)
            print("Obstacle detected within 5 cm, LED ON")
        else:
            # Otherwise, turn off the LED
            GPIO.output(LED, False)
            print("No obstacle within 5 cm, LED OFF")
        time.sleep(0.5)  # Short delay before next measurement

except KeyboardInterrupt:
    print("Program stopped by user")
    GPIO.cleanup()  # Clean up GPIO settings

