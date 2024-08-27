from django.test import TestCase


class Utils(TestCase):

    def register(self,username,email,password,confirmation):
        self.client.post("/register", data={'username':username,
                                        'email':email,
                                        'password':password,
                                        'confirmation':confirmation})
        
    def login(self,username,password):
        self.client.post("/login", data={'username':username,
                                         'password':password})
        
    def logout(self):
        self.client.post("/logout")
        
    def register_and_login(self,username,email,password,confirmation):
        self.register(username, email, password, confirmation)
        self.login(username,password)

    def create_a_listing(self,title,description,price,url,category):
        self.client.post("/newlisting", data={'title':title,
                                             "description":description,
                                             "price":price,
                                             "url":url,
                                             "category":category}) 
        
    def submit_a_bid(self, price, id):
        self.client.post(f"/listing/{id}/submitbid", data={'bid':price})

    def submit_a_comment(self, text, id):
        self.client.post(f"/listing/{id}/savecomment", data={'text':text})