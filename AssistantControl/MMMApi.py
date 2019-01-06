import requests

assistantData = [['Alexa','https://images-na.ssl-images-amazon.com/images/G/01/mobile-apps/dex/avs/docs/ux/branding/mark1._TTH_.png'],
['Google%20Assistant','https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_HOR.png']]

class MMMApi:

    def showAlert(self,title,message,imgUrl):
        postRequestURL = 'http://localhost:8080/api/v1/modules/alert/SHOW_ALERT?title=' + title + '&message=' + message + '&imageUrl=' + imgUrl
        try:
            response = requests.post(postRequestURL)
        except requests.exceptions.RequestException:
            print("Magic Mirror is not connected.")
            return
        print(response.text)

    def hideAlert(self):
        postRequestURL = 'http://localhost:8080/api/v1/modules/alert/HIDE_ALERT'
        try:
            response = requests.post(postRequestURL)
        except requests.exceptions.RequestException:
            print("Magic Mirror is not connected.")
            return

        print(response.text)

    def wakeup(self,assistantNo):
        message = "Please%20speak%20your%20request."
        self.showAlert(assistantData[assistantNo][0] ,message,assistantData[assistantNo][1])
        
    
    def think(self,assistantNo):
        message = "thinking..."
        self.showAlert(assistantData[assistantNo][0] ,message,assistantData[assistantNo][1])
        
    def speak(self,assistantNo):
        message = "speaking..."
        self.showAlert(assistantData[assistantNo][0] ,message,assistantData[assistantNo][1])

    def finish(self,assistantNo):
        message = "finish."
        self.showAlert(assistantData[assistantNo][0] ,message,assistantData[assistantNo][1])
    

    def off(self):
        self.hideAlert()

