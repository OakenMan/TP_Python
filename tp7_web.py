import http.server

PORT = 8888
server_adress = ("", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print("serveur actif sur le port ", PORT)

httpd = server(server_adress, handler)
httpd.serve_forever()