__author__ = 'vic'
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import db2html
import re

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>Hello!!!!'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello">' \
                          '<h2>What would you like to say me</h2><input name="message" type="text">' \
                          '<input type="submit" value="Submit"> </form>'
                output += '</body></html>'
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>&#161Hooollaaa!!!! <a href= "/hello"> Back to hello<a>'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello">' \
                          '<h2>What would you like to say me</h2><input name="message" type="text">' \
                          '<input type="submit" value="Submit"> </form>'
                output += '</body></html>'
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<a href="/restaurants/new"> Create new restaront<a>'
                output += db2html.read_restaurants()
                output += '</body></html>'
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/edit'):
                restaurant_path_id = self.path.split('/')[2]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant_name = db2html.get_restaurant_name(restaurant_path_id)
                # it's better to check if exists such id in DB
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/edit">' \
                          '<h2> Edit restaurant %s</h2>' \
                          '<input name="edit_restaurant" placeholder="New name" type="text">' \
                          '<input type="submit" value="Edit"> </form>' % (restaurant_path_id, restaurant_name)
                output += '</body></html>'
                self.wfile.write(output)
                print(output)
                return



            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/new">' \
                          '<h2> New restaurant</h2>' \
                          '<input name="new_restaurant" placeholder="New restaurant name" type="text">' \
                          '<input type="submit" value="Submit"> </form>'
                output += '</body></html>'
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, 'File not found %s' % self.path)
            print('IOError %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') #redirect to page (ignore below html code)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')
                    db2html.create_restaurant(messagecontent[0])
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/new">' \
                          '<h2> New restaurant</h2>' \
                          '<input name="new_restaurant" placeholder="New restaurant name" type="text">' \
                          '<input type="submit" value="Submit"> </form>'
                output += '</body></html>'

                self.wfile.write(output)

            if self.path.endswith('/edit'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_path_id = self.path.split('/')[2]
                    messagecontent = fields.get('edit_restaurant')
                    db2html.edit_restaurant(restaurant_path_id, messagecontent[0])


            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')
            #
            # output = ''
            # output += '<html><body>'
            # output += '<h2> Okay, how about this </h2>'
            # output += '<h1>%s</h1>' % messagecontent[0]
            #
            # output += '<form method="POST" enctype="multipart/form-data" action="/hello">' \
            # '<h2>What would you like to say me</h2><input name="message" type="text">' \
            #           '<input type="submit" value="Submit"></form>'
            # output += '</body></html>'
            #
            # self.wfile.write(output)
            # print(output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print('webserver running on port: {0}'.format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered , stoping webserver')
        server.socket.close()


if __name__ == '__main__':
    main()