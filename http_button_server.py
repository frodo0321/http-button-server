from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from socket import socket, AF_INET, SOCK_DGRAM
from os.path import basename, splitext

class HTTPHandler(BaseHTTPRequestHandler):

    def query_string(self):
        d=dict()
        if "?" in self.path:
            for e in self.path[self.path.index('?')+1:].split('&'):
                var, val=e.split('=')
                d[var]=val
        return d

class ButtonServer():
    def __init__(self, callback, port=8000):
        self.callback=callback
        self.buttons=dict()
        self.textboxes=dict()
        self.xtrahtml=""
        self.port=port
        self.server=None
	
    def add_button(self, name, html_attribute_string=""):
	self.buttons[name]=html_attribute_string

    def add_textbox(self, name, html_attribute_string=""):
        self.textboxes[name]=html_attribute_string
    
    def add_html(self, html):
        self.xtrahtml=html

    def button_html_string(self):
        s=""
        for e in self.buttons.keys():
            s+=str("""<button type='button' id='%s' %s>%s</button>""" % (e, self.buttons[e], e))
        return s

    def textbox_html_string(self):
        s=""
        for e in self.textboxes.keys():
            s+=str("""<input id='%s' type='text' %s>""" % (e, self.textboxes[e]))
        print s
        return s

    def html_string(self):
        tbs='var tbs=""'
        if len(self.textboxes)>0:
            tb=[]
            for e in self.textboxes.keys():
                tb.append('"&%s="+document.getElementById("%s").value' % (e, e))
            tbs = "var tbs=" + "+".join(tb) + ";"
        el=""
        for e in self.buttons.keys():
            el+='document.getElementById("%s").addEventListener("click", ajax);' % (e)
        html=  """
        <script>
        function ajax(evt)
        {
        var xmlhttp;
        if (window.XMLHttpRequest)
        {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
        }
        else
        {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        """ + tbs + """
        xmlhttp.open("GET", "ajax?action="+evt.target.id+tbs, true);
        xmlhttp.send();
        }
        """ + el + "</script>"
        
        return "<form action='.' method='GET'>" + self.button_html_string() + self.textbox_html_string() + "</form>" + self.xtrahtml + html
	
    def run(self):
        def get(self):
#####################STOP THE FAVICON GET REQUEST#######################
            if splitext(basename(self.path))[0]=='favicon':
                return
##############################AJAX######################################
            if '?' in self.path and basename(self.path[:basename(self.path).index('?')+1])=="ajax":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("")
#########################CALL BUTTON FUNCTION###########################
                qs=self.query_string()
                if hasattr(self.callback[0], '__call__'):
                    self.callback[0](qs)
                return
#########################SEND RESPONSE PAGE#############################
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(self.html_string())
            return

        HTTPHandler.callback=[self.callback]
        HTTPHandler.do_GET=get
        HTTPHandler.html_string=self.html_string
        HTTPHandler.xtrahtml=self.xtrahtml
        HTTPHandler.textboxes=self.textboxes
        HTTPHandler.buttons=self.buttons
        HTTPHandler.button_html_string=self.button_html_string
        HTTPHandler.textbox_html_string=self.textbox_html_string


        try:
            self.server = HTTPServer(('0.0.0.0', self.port), HTTPHandler)
            ###get local ip
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(("8.8.8.8",80))
            ip = s.getsockname()[0]
            s.close()            
            print 'Started httpserver at ' + str(ip) + ':' + str(self.port)
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.socket.close()

if __name__=='__main__':
	def p(qs):
		print "BUTTON PRESSED", qs
	b=ButtonServer(p)
	b.add_button("Up", 'style="position: absolute; top: 0px; left: 0px;width: 60px;"')
	b.add_button("Down", 'style="position: absolute; top: 20px; left: 0px; width: 60px;"')
        b.add_textbox("tb", 'style="position: absolute; left: 200px; top: 0px"')
        b.add_textbox("tb2", 'style="position: absolute; top: 0px; left: 60px"')
	b.run()
