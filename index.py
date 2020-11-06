#!/usr/bin/python3
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

login_page = """<!DOCTYPE html>
<head>
    <title>Mon programme</title>
</head>
<body>
    <form action="index.py" method="get">
        <input type="text" name="data" value="" />
        <input type="submit" name="sendata" value="Send data" />
    <form>
    </br></br></br>
    <form action="login.py" method="post">
        <input type="submit" name="send" value="Log in" />
    </form>
</body>
</html>    
"""

print(login_page)


