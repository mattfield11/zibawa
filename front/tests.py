from django.test import TestCase,Client
from django.conf import settings
from stack_configs.ldap_functions import getLDAPConn,removeFromLDAPGroup
import logging
#from chardet.test import result

logger = logging.getLogger(__name__)

#front tests
# Create your tests here.

testuser='sprog4'
testuseremail=testuser+"@autotest.com"

class CreateAccountTestCase(TestCase):
#note test which start in capitals only run when called by a test starting in small letter
#this is to force the tests to run in sequence
    
    
    def Test_create_client(self):
                
        logger.info('test start setUpCreateAccountTest ' )
        # First check for the default behavior
        #will need to delete user from LDAP...
        logger.info('test calling create_account')
        response=self.client.post('/create_account/', {'username': testuser, 'password': 'secret', 'first_name':'fred','last_name':'test', 'email':testuseremail})
        self.assertRedirects(response, '/thanks/')
        
        #ensure cant login with a username that already exists
        logger.info('test trying to create username which already exists')
        response=self.client.post('/create_account/', {'username': testuser, 'password': 'secret', 'first_name':'fred','last_name':'test', 'email':'fred2@me.com'})
        self.assertEqual(response.status_code, 200)
        #ensure cant login with email that already exists
        logger.info('test trying to create username with email which already exists')
        response=self.client.post('/create_account/', {'username': 'differenttestuser', 'password': 'secret', 'first_name':'fred','last_name':'test', 'email':testuseremail})
        self.assertEqual(response.status_code, 200)
        
    def Test_passwordChange(self):
        
        
        logger.info('test starting test password change')
        logger.info('test logging in')
        response= self.client.login(username=testuser, password='secret')
        logger.info('test post to change password')
        response=self.client.post('/change_password/', {'old_password': 'secret', 'new_password1': 'verysecret', 'new_password2':'verysecret'})
        self.assertRedirects(response, '/change_password/done/')
        logger.info('test logging out')
        response=self.client.get('/logout/')
        self.assertRedirects(response, '/login/')
        logger.info('test get login page')
        response=self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        logger.info('test login with new password')
        response= self.client.login(username=testuser, password='verysecret')
             
    def Test_all_pages(self):
        #get all pages
        response= self.client.login(username=testuser, password='verysecret')
        
        #make sure user has permissions, in zibawa and ldap!
        admin_pages = [
            "/create_account/",
            "/thanks/",
            "/account_create_error/",
            "/change_password/done/",
            "/password_reset/",
            "/password_reset_done/",
            "/login/",
           
        ]
        for page in admin_pages:
            logger.info('testing GET page %s',page)
            response = self.client.get(page)
            self.assertEqual(response.status_code, 200)
      
        response= self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
    
    
    
          
    def test_All(self):
        self.Test_create_client()
        self.Test_passwordChange()
        self.Test_all_pages()
        
    
    def tearDown(self):
        logger.info('test teardown CreateAccount')
        removeFromLDAPGroup(testuser,'active')
        removeFromLDAPGroup(testuser,'editor')
        
        dn= str("cn=")+str(testuser)+str(",")+str(settings.AUTH_LDAP_USERS_OU_DN)
        con= getLDAPConn()
        result=con.delete(dn)
        logger.info('delete result in test_cleanup %s', result)
        self.assertEqual(result,True)    
