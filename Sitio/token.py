from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six 

class ProjectTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, project):
        return(
            six.text_type(project)
        )
        
class ClientTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, client):
        print(client)
        return(
            six.text_type(client)
        )