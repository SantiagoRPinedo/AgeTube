import requests
import json

# Programmtically delete (total purge) a Facial ID, its associated payload data, 
# and biometric hash from a given FACEIO application - Refer to https://faceio.net/facialid for additional information
req = requests.get('https://api.faceio.net/deletefacialid',params={
	"fid":"4e9167924b6245b0a9078829e65e6cdc", # Target Facial ID to purge from this FACEIO application. Find out more information about the Facial ID on https://faceio.net/facialid
	"key": "02ac9a039fc8775b2f0002b61bd68974" # Your FACEIO Application API Key. Retrieve this key from the Application Manager on the console at: https://console.faceio.net
})
reply = req.json()
if reply['status'] != 200:
	print (reply['error'])
	exit()
# Success
print("Given Facial ID, payload data, and Biometrics hash purged from this application")

