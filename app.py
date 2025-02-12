from flask import Flask, request, jsonify
import base64
import speech_recognition as sr
import wave
from ast import literal_eval


def speechRecognition(data, params):
    print("sr starts")
    r = sr.Recognizer()

    audioFileName = 'test.wav'
    data = base64.b64decode(data)
    params = base64.b64decode(params)
    params = literal_eval(params.decode("utf-8"))

    wave_write = wave.open(audioFileName, "w")
    wave_write.setparams(params)
    wave_write.writeframes(data)
    wave_write.close()

    audioFile = None
    with sr.AudioFile(audioFileName) as source:
        audioFile = r.record(source)

    try:
        print("sr try")
        text = r.recognize_google(audioFile, language="fr-FR")
        return text
    except Exception as e:
        print (e)

app = Flask(__name__)

@app.route('/')
def hello_world(): 
    return 'Hello World!'

@app.route("/google", methods=["POST","GET"])
def transcribe():
    print("google starts")
    req_data = request.get_json(force=True)

    result_from_google = speechRecognition(req_data['data'], req_data['params'])


    print(result_from_google)
    reply = {"sentence": result_from_google}

    return reply #jsonify(reply)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
