
class userAccount:
    def __init__(self, role, wallet, name, email):
        self.role = role
        self.wallet = wallet
        self.name = name
        self.email = email
        self.validated = False
        
        if role == 0:
            #READER ROLE [PART OF PUBLIC BLOCKCHAIN]
            validated = True
            
    
    def validate(self, verification):
        #VERIFY USING A CERTIIFICATE OBTAINED FROM AUTHENTICATION SERVICE
        self.validated = True
        
    