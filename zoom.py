import jwt
import requests
import json
from time import time



API_KEY = 'UKNIUukcRjqe4uqC4Dk-sg'
API_SEC = 'db1z5klumPMllARFsIg5yVkIf4byPNI6popI'

def generateToken():
	token = jwt.encode(
		
		{'iss': API_KEY, 'exp': time() + 5000},
		
		API_SEC,
		
		algorithm='HS256'
	)
	return token


meetingdetails = {"topic": "Noar Zoom Meeting",
				"type": 2,
				"start_time": "2020-11-17T10: 21: 57",
				"duration": "45",
				"timezone": "Europe/Tirana",
				"agenda": "Noar's Presentation",

				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud"
							}
				}

def createMeeting():
	headers = {'authorization': 'Bearer %s' % generateToken(),
			'content-type': 'application/json'}
	r = requests.post("https://api.zoom.us/v2/users/me/meetings",headers=headers, data=json.dumps(meetingdetails))

	print("\n creating zoom meeting ... \n")
	y = json.loads(r.text)
	join_URL = y["join_url"]
	#meetingPassword = y["password"]
	return join_URL




