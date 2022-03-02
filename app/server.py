import os
import random
import string
import threading
import uuid

import cherrypy
from .gui import *


@cherrypy.expose
class Root(object):
    def GET(self, param=None, method=None, *args, **kwargs):
        print(f'ddd param:{param} method:{method} args:{args} kwargs:{kwargs}')
        if param == 'description.xml':
            return load_xml('description.xml').format(
                friendly_name='NOTAG',
                manufacturer="notag.cn",
                manufacturer_url="https://github.com/dushan555",
                model_description="LiveTV and DLNA Media Renderer",
                model_name="Live",
                model_url="https://notag.cn",
                model_number='0.3',
                uuid=str(uuid.uuid4()),
                serial_num=1024,
                header_extra='''<qq:X_QPlay_SoftwareCapability xmlns:qq="http://www.tencent.com">QPlay:2.1</qq:X_QPlay_SoftwareCapability>''',
                service_extra='''<service>
                    <serviceType>urn:schemas-upnp-org:service:PrivateServer:1</serviceType>
                    <serviceId>urn:upnp-org:serviceId:PrivateServer</serviceId>
                    <controlURL>_urn:schemas-upnp-org:service:PrivateServer_control</controlURL>
                    <SCPDURL>_urn:schemas-upnp-org:service:PrivateServer_scpd.xml</SCPDURL>
                    <eventSubURL>_urn:schemas-upnp-org:service:PrivateServer_event</eventSubURL>
                    </service>
                    <service>
                    <serviceType>urn:schemas-tencent-com:service:QPlay:1</serviceType>
                    <serviceId>urn:tencent-com:serviceId:QPlay</serviceId>
                    <controlURL>_urn-schemas-upnp-org-service-QPlay_control</controlURL>
                    <SCPDURL>_urn-schemas-upnp-org-service-QPlay_scpd.xml</SCPDURL>
                    <eventSubURL>_urn-schemas-upnp-org-service-QPlay_event</eventSubURL>
                    </service>'''
            ).encode()
        if param == 'dd':
            return self.GetHexdigits()
        cherrypy.response.headers['Content-Type'] = 'text/html'
        return f'{param} {kwargs}'
        # cherrypy.response.headers['Content-Type'] = 'text/html'
        # return '''<html><script>location.href='https://notag.cn'</script></html>'''.encode()

    def POST(self, param=None, *args, **kwargs):
        method = kwargs.get('method', None)
        print(f'ddd param:{param} method:{method} args:{args} kwargs:{kwargs}')
        return self.GetHexdigits()

    def SUBSCRIBE(self, service='', param=''):
        print(f'SUBSCRIBE service {service} param {param}')
        return b''

    def GetHexdigits(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        return some_string


class Service:
    def __init__(self):
        self.conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/xml'), ('Server', 'Live/0.3')],
                'tools.staticdir.root': os.path.abspath(os.getcwd()),
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'public',
            }
        }
        self.thread = None
        self.app = cherrypy.tree.mount(Root(), '/', config=self.conf)
        cherrypy.server.bind_addr = ('0.0.0.0', 10980)
        cherrypy.engine.signals.subscribe()

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.start_service, name="SERVICE_THREAD")
            self.thread.start()

    def close(self):
        if self.thread is not None:
            self.thread.join()

    @staticmethod
    def start_service():
        cherrypy.engine.start()
        _, port = cherrypy.server.bound_addr
        print(f'cherrypy starting {port}')
        cherrypy.engine.block()


if __name__ == '__main__':
    Service()
