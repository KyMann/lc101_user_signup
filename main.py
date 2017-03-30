#user-input main file
import webapp2
import cgi
import re

error_dict={'empty_name':"", 'space_name':"", 'password_match':"", 'email_unparsable':""} #initialize the error dict
#content_dict

def write_content(error_dict, content_dict = {'username_key':'', 'email_key':''}):
    '''for each field, put in use write_input to put in label and textarea, then use error_insert to check for errors and insert them, then break line'''    
    header = "<h1>Signup</h1>"
    name_submit = write_input('Username', content_dict['username_key']) + error_insert(error_dict['empty_name']) + error_insert(error_dict['space_name'])+'<br>'
    pass_submit = write_input('Password') + error_insert(error_dict['password_match']) + '<br>'
    verify_pass_submit = write_input('Verify_Password') + '<br>'
    email_submit = write_input('Email(optional)', content_dict['email_key']) + error_insert(error_dict['email_unparsable'])+'<br>'
    button = "<input type='submit'/>"
    content = header + name_submit + pass_submit + verify_pass_submit +email_submit +button
    return content 

def write_input(box_label, contents=""):   #box label a string
    """creates a textarea input using the input string as both the 
    name and the label for the textarea"""
    ht_field = "<label>" + box_label + "</label>" + "<textarea name=" + box_label + ">" + contents + "</textarea>"
    return ht_field

def error_insert(error_string):
    if error_string == '':
        return ""
    else:
        error_string = '<span style="color: red">' + error_string + "</span>"
        return error_string
 
def valid_email(email):
    '''If valid email, return True, else return False '''
    if '@' in email and '.' in email:
        for count, char in enumerate(email): # symbols@symbols.symbols
            if count == 0:
                if char == '@' or char == '.':
                    return False
            if char == '@':
                address_positon = count
            if char =='.': #yes, there can be multiple .'s but the point is to capture the last one, which this should do since it will overwrite and get the last one
                domain_position = count
        if domain_position < address_positon + 1:
            return False
        else:
            return True
    else:
        return False

def valid_username(username):
    special_symbols = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
    for char in username: 
        if char in special_symbols:
            return False
    else:
        return True
        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        form = "<form method='post'>" + write_content(error_dict) + "</form>"
        self.response.write(form)
        
    def post(self):
        username = self.request.get('Username')
        password = self.request.get('Password')
        verify_password = self.request.get('Verify_Password')
        email = self.request.get('Email(optional)')
        
        #validation here
        success = True
        errors={'empty_name':"", 'space_name':"", 'password_match':"", 'email_unparsable':""}
        
        if username == "":
            success = False
            errors['empty_name'] = "The username cannot be empty."
            
        if len(username) < 3:
            success = False
            if errors['empty_name'] == "":
                errors['empty_name'] = "The username is too short"
            else:
                pass
            
        if not valid_username(username):
            success = False
            errors['space_name'] = "The username cannot contain special characters or spaces"
            
        if len(password) < 3:
            success = False
            errors['password_match'] = 'The password is too short!'
        
        if password != verify_password or password == '':
            success = False
            if errors['password_match'] == '':
                errors['password_match'] = 'The passwords do not match!'
            else:
                pass
            
        if email == '':
            pass
        else:
            if not valid_email(email):
                success = False
                errors['email_unparsable'] = 'This email is not valid'
        
        #put url escaping here
        username = cgi.escape(username)
        email = cgi.escape(email)
            
        if success:
            self.redirect('/welcome?name=' + username)
        else:
            content_dict = {}
            content_dict['username_key'] = username
            content_dict['email_key'] = email # need some way to port content back into boxes, save some inputs
      
            form = "<form method='post'>" + write_content(errors, content_dict) + "</form>"
            self.response.write(form)
            
class WelcomeHandler(webapp2.RequestHandler):        
        def get(self):
            username = self.request.get('name')
            welcome_page = "<h1> Welcome </h1> <p>" + username + "</p>"
            self.response.write(welcome_page)
                   
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler),
], debug=True)
