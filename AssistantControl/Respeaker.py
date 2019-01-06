from mic_hat_4 import pixels
from mic_hat_4 import alexa_led_pattern
from mic_hat_4 import google_home_led_pattern

assistantPattern = [ alexa_led_pattern.AlexaLedPattern(show=pixels.pixels.show),google_home_led_pattern.GoogleHomeLedPattern(show=pixels.pixels.show)]

class Respeaker:

    def speak(self,assistantNo):
        pixels.pixels.pattern = assistantPattern[assistantNo]
        pixels.pixels.speak()

    def think(self,assistantNo):
        pixels.pixels.pattern = assistantPattern[assistantNo]
        pixels.pixels.think()

    def wakeup(self,assistantNo):
        pixels.pixels.pattern = assistantPattern[assistantNo]
        pixels.pixels.wakeup()
    
    def off(self):
        pixels.pixels.off()
        print("off")
    
    
    
    
    