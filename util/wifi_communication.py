import network
import urequests
import ujson
from lib.base64 import b64encode

_WEBHOOK_URL = 'https://owi-server.onrender.com/webhook/publish'

class WiFiCommunication:
    def __init__(self, *, ssid, password):
        self.sta_if = network.WLAN(network.STA_IF)
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
            self.sta_if.connect(ssid, password)
            while not self.sta_if.isconnected():
                pass
        print('wifi connected. network config:', self.sta_if.ifconfig())

    def send(self, data):
        data = b64encode(ujson.dumps(data, separators=(',', ':')).encode('utf8')).decode('utf8')
        #return urequests.post(
        #    _WEBHOOK_URL,
        #    headers={ 'content-type': 'application/json' },
        #    data=ujson.dumps({ 'end_device_ids': None, 'uplink_message': { 'rx_metadata': None, 'frm_payload': data } }, separators=(',', ':')),
        #)
        return urequests.get('http://example.com')
