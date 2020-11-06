#!/usr/bin/python3
import cgi

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

login_page = """<!DOCTYPE html>
<head>
    <title>Mon programme</title>
</head>
<body>
    <form action="login.py" method="post">
        <input type="text" name="username" value="Username" />
        <input type="text" name="password" value="Password" />
        <input type="submit" name="send" value="Log in" />
    </form>
</body>
</html>    
"""

data_page = """<!DOCTYPE html>
<head>
    <title>Mon programme</title>
</head>
<body>
    <p> Woah plein de données </p>
</body>
</html>    
"""

if form.getvalue("username") == "tom" and form.getvalue("password") == "suchel":
    print(data_page)
else:
    print(login_page)


