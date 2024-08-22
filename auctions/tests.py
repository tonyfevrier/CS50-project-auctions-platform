from django.test import TestCase

from auctions.models import Listings


class TestListing(TestCase):

    def test_listing_registration(self):

        #register and login to access the newlisting view
        self.register('tony','t@gmail.com','1234','1234') 
        self.login('tony','1234')

        #register a new listing 
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        
        #verify registration
        listing = Listings.objects.first() 

        self.assertEqual(len(Listings.objects.all()),1)
        self.assertEqual(listing.title,"titre")
        self.assertEqual(listing.id,1)
        self.assertEqual(listing.description,"here is the description")
        self.assertEqual(listing.price,10.2)
        self.assertEqual(listing.url,"http://test")
        self.assertEqual(listing.category,"toys")

    def test_listing(self): 
        self.register('tony','t@gmail.com','1234','1234') 
        self.login('tony','1234')
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        response = self.client.get("/listing/1") 
        self.assertTemplateUsed(response,"auctions/listing.html")


    def register(self,username,email,password,confirmation):
        self.client.post("/register",data={'username':username,
                                        'email':email,
                                        'password':password,
                                        'confirmation':confirmation})
        
    def login(self,username,password):
        self.client.post("/login", data={'username':username,
                                         'password':password})
    
    def create_a_listing(self,title,description,price,url,category):
        self.client.post("/newlisting",data={'title':title,
                                             "description":description,
                                             "price":price,
                                             "url":url,
                                             "category":category}) 
        



