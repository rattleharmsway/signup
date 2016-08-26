#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import codecs
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")



page_header = """
<!DOCTYPE html>
<html lang="en"> <!-- lang="en" is for bootstrap-->
<head>


    <!-- bootstrap links-->
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

    <style type="text/css">
        .error {
            color: red;
        }
        #inner {
            width: 50%;
            margin: 0 auto;
            text-align: center;
        }
        #inner2 {
            width: 50%;
            margin: 0 auto;
            text-align: center;
        }


        #innerThanks {
            margin: 0 auto;
            text-align: center;
            background-color: red;
        }
    </style>

    <title>Sign UP^^</title>
    <meta charset="utf-8"> <!-- for bootstrap-->
    <meta name="viewport" content="width=device-width, initial-scale=1">  <!-- for bootstrap mobile responsiveness-->

</head>
<body>
    <div class="container">
        <h1 id="inner">
            <a href="/">sign UP!!</a>
        </h1>
        <br>
    </div>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

form = """
<div class="container"> <!-- for bootstrap, body must be in this class -->
<form method = "post" id = "inner">
    <div class="form-group">
    <h2 id="inner">SignUp</h2><div></div>
    <br>
    <label><strong>Username<strong>
        <input type="text" name ="username" value="%(username)s">
    </label>
    <div style = "color:red">%(error_user)s</div>
    <div></div>
    <br>
    <br>
    <label><strong>PassWord<strong>
        <input type="password" name ="pass1">
    </label>
    <div style = "color:red">%(error_pass)s</div>
    <br>
    <br>
    <label><strong>Verify PassWord<strong>
        <input type="password" name ="pass2">
    </label>
    <div style = "color:red">%(error_pass2)s</div>
    <br>
    <br>
    <label><strong>email @ddress<strong>
        <input type="text" name ="email" value="%(email)s">
    </label>
    <div style = "color:red">%(error_email)s</div>
    <div></div>
    <br>
    <br>
    <input class="btn btn-success btn-block" type="submit">
    </div>
</form>
</div>
"""

thanks = """
<body id = "innerThanks">
<div id = "inner2"> <!-- for bootstrap, body must be in this class -->
    <h1>Welcome, <strong>%(username)s</strong>!</h1>
    <br>
    <div >
        <iframe allowfullscreen height="450" src="https://www.youtube.com/embed/oHg5SJYRHA0?autoplay=1&iv_load_policy=3&rel=0" width="600"></iframe>
    </div>

</div>
</body>
"""

def is_digit(n):
    if n and n.isdigit():
        num = int(n)
        return num

def escape_html(s):
    return cgi.escape(s, quote = True)

def caesar(string, shift):
    cipherText = ""
    for ch in string:
        if ch.isalpha():
            stayInAlphabet = ord(ch) + shift
            if ch.islower():
                if stayInAlphabet > ord('z'):
                    stayInAlphabet -= 26
            elif ch.isupper():
                    if stayInAlphabet > ord('Z'):
                        stayInAlphabet -= 26
            finalLetter = chr(stayInAlphabet)
            cipherText += finalLetter
        else:
            cipherText += ch
    return cipherText

def valid_username(username):
    return USER_RE.match(username)

def valid_pass(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_user="",error_pass="",error_pass2="", error_email="", username="", email=""):
        self.response.write(page_header + form % {"error_user" : error_user, "error_pass" : error_pass, "error_pass2" : error_pass2, "error_email" : error_email, "username" : username, "email" : email} + page_footer)

    def get(self):
        self.write_form()

    def post(self):
        username_input = self.request.get(escape_html('username'))
        password1 = self.request.get('pass1')
        password2 = self.request.get('pass2')
        email = self.request.get(escape_html('email'))
        user = username_input
        if username_input and password1 and password2 and email:
            if valid_username(username_input) and valid_pass(password1) and password1 == password2 and valid_email(email): #and valid_email(email)   took this out
                self.redirect('/thanks?username=' + username_input)

            elif not valid_username(username_input):
                self.write_form("Invalid UserName", "", "","", username_input, email)

            elif not valid_pass(password1):
                self.write_form("", "This Pass Word is not valid","", "", username_input, email)
            #self.write_form("", "", "", username_input, email)

            elif password1 != password2:
                self.write_form("", "","These Passwords Do Not Match", "", username_input, email)

            elif not valid_email(email):
                self.write_form("", "","", "This email is invalid", username_input, email)

        else:
            if valid_username(username_input) and valid_pass(password1) and password1 == password2: #and valid_email(email)   took this out
                self.redirect('/thanks?username=' + username_input)

            elif not valid_username(username_input):
                self.write_form("Invalid UserName", "", "","", username_input, email)

            elif not valid_pass(password1):
                self.write_form("", "This Pass Word is not valid","", "", username_input, email)
            #self.write_form("", "", "", username_input, email)

            elif password1 != password2:
                self.write_form("", "","These Passwords Do Not Match", "", username_input, email)



class ThanksHandler(webapp2.RequestHandler):

    def write_form(self, username=""):
        self.response.write(page_header + thanks % {"username" : username} + page_footer)


    def get(self):
        username_input = self.request.get(escape_html('username'))
        self.write_form(username_input)
        #self.response.write("Thanks for Signing Up, " + username_input + "!!!!!!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
