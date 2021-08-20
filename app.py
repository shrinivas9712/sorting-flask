from flask import Flask,jsonify
import paho.mqtt.client as mqtt
import json
import datetime
message={"devmac":"","EPC":"","Formatted UTC time":""}
def on_connect(client,userdata,flags,rc):
    print("the device is connected to the server successfully wit rc:"+str(rc))
    client.subscribe("Technologics_sorting1")
def on_message(client,userdata,msg):
    global message
    my_str=str(msg.payload)
    my_str=my_str[2:len(my_str)-1]
    json_data=json.loads(my_str)
    message["devmac"]=json_data["devmac"]
    message["EPC"]=json_data["reads"][0]["EPC"]
    message["Formatted UTC time"]=datetime.datetime.now()
client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.connect("broker.hivemq.com",1883,60)
app= Flask(__name__)
@app.route("/") 
def fun():
    global message
    return jsonify(message)
client.loop_start()
try:
    if __name__  ==  "__main__":
        app.run(debug=True)
except:
    client.loop_stop(force=False)