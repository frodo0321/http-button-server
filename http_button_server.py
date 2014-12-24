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
    def __init__(self, port=8000):
        self.buttons=dict()
        self.textboxes=dict()
        self.xtrahtml=""
        self.port = port
        self.server = None
	
    def add_button(self, name, callback, newhtml=""):
        if not hasattr(callback, '__call__'):
    	    raise TypeError("fn not callable!")
	self.buttons[name]=callback

    def add_textbox(self, name, inittext=""):
        self.textboxes[name]=inittext
    

    def html_string(self):
        html= """
        <script>
        function ajax(button_name)
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
        var tbs="";
        xmlhttp.onreadystatechange=function()
        {
            if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
                var key;
                obj=JSON.parse(xmlhttp.responseText);
                for(key in obj.textboxes)
                {
                    if(obj.textboxes.hasOwnProperty(key))
                    {
                        var name = obj.textboxes[key].name
                        tbs+=("&" + name + "=" + document.getElementById(name).value);
                    }
                }
            xmlhttp.open("GET","ajax?action="+button_name+tbs,true);
            xmlhttp.send();
            }
        }
        xmlhttp.open("GET","tbnames",true);
        xmlhttp.send();
        }
        </script>"""

        but=""
        tb=""
        for e in self.buttons.keys():
            but+=str("""<button type='button' value='%s' name='action' onclick='ajax("%s")'>%s</button>""" % (e, e, e))
        for e in self.textboxes.keys():
            tb+=str("""<input id='%s' type='text' name='%s' value='%s'>""" % (e, e, self.textboxes[e]))
        return html + "<form action='.' method='GET'>" + but + tb + "</form>"
	
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
                fn=self.buttons.get(qs.pop('action'))
                if hasattr(fn, '__call__'):
                    fn(qs)
                return

            if basename(self.path)=="tbnames":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                jsonstr=[]
                for e in self.textboxes.keys():
                    jsonstr.append(str('{"name":"%s"}' % (e)))
                jsonstr='{"textboxes":[' + ",".join(jsonstr) + ']}'

                self.wfile.write(jsonstr)
                return
#########################SEND RESPONSE PAGE#############################
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(self.html_string())
            return


        HTTPHandler.do_GET=get
        HTTPHandler.html_string=self.html_string
        HTTPHandler.textboxes=self.textboxes
        HTTPHandler.buttons=self.buttons


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
	b=ButtonServer()
	def p(qs):
		print "BUTTON PRESSED", qs
	b.add_button("Up", p)
	b.add_button("Down", p)
        b.add_textbox("tb", "yo")
        b.add_textbox("tb2", "howdy")
	b.run()
