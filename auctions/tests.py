from django.test import TestCase

from auctions.models import Listing, Bid, Comment
from auctions.utils import Utils


class TestListing(Utils):

    def test_listing_registration(self):
        #register and login to access the newlisting view
        self.register_and_login('tony','t@gmail.com','1234','1234') 

        #register a new listing 
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        
        #verify registration of the listing
        listing = Listing.objects.first() 

        self.assertEqual(len(Listing.objects.all()),1)
        self.assertEqual(listing.title,"titre")
        self.assertEqual(listing.id,1)
        self.assertEqual(listing.description,"here is the description")
        self.assertEqual(listing.price,10.2)
        self.assertEqual(listing.url,"http://test")
        self.assertEqual(listing.category,"toys")
        self.assertEqual(listing.creator.username, 'tony') 

    def test_listing(self): 
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        response = self.client.get("/listing/1") 
        self.assertTemplateUsed(response,"auctions/listing.html")

    def test_add_to_watchlist(self):
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
 
        self.assertNotIn('tony',Listing.objects.first().followers)
        self.client.get('/toggletowatchlist/1')
        self.assertIn('tony',Listing.objects.first().followers) 
        self.client.get('/toggletowatchlist/1') 
        self.assertNotIn('tony',Listing.objects.first().followers)

    def test_two_followers_of_a_watchlist(self):
        """
        Here two persons add the same listing to their watchlist and are registered as followers.
        """
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys")
        self.client.get('/toggletowatchlist/1')
        self.assertListEqual(Listing.objects.first().followers, ['tony'])
        self.logout()
        self.register_and_login('marine','m@gmail.com','5678','5678')
        self.client.get('/toggletowatchlist/1')
        self.assertListEqual(Listing.objects.first().followers, ['tony','marine'])
        self.logout()

    def test_submit_inferior_bid(self):
        """In this case, there should be no bid saved in the database"""
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys")
        self.assertEqual(len(Bid.objects.all()), 0)
        self.submit_a_bid("10.", 1)
        self.assertEqual(len(Bid.objects.all()), 0)

    def test_submit_superior_bid(self):
        """A new bid must be saved in the database for the corresponding listing"""
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys")
        self.assertEqual(len(Bid.objects.all()), 0)
        self.submit_a_bid("20.", 1)
        self.assertEqual(len(Bid.objects.all()), 1)
        self.submit_a_bid("22.", 1)
        self.assertEqual(len(Bid.objects.all()), 2)

    def test_other_user_submit_bid(self):
        """
        A person different from the listing creator submits a bid and the bidder is correctly registered.
        """
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.logout()
        self.register_and_login('marine','m@gmail.com','5678','5678') 
        self.submit_a_bid("100",1) 
        self.assertEqual(Bid.objects.last().bidder.username, 'marine')
        self.logout()

    def test_delete_listing(self):
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.assertEqual(len(Listing.objects.all()), 1)
        self.assertEqual(Listing.objects.first().winner, "")
        self.client.get("/listing/1/deletelisting") 
        self.assertNotEqual(Listing.objects.first().winner, "")

    def test_register_comment(self):
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.submit_a_comment('Ceci est un commentaire', '1')
        self.submit_a_comment('Ceci est un commentaire encore', '1')
        self.submit_a_comment('Ceci est un commentaire encore une fois', '1')
        self.assertIn('Ceci est un commentaire', [comment.text for comment in Comment.objects.all()])
        self.assertIn('Ceci est un commentaire encore', [comment.text for comment in Comment.objects.all()]) 
        comment = Comment.objects.first()
        self.assertEqual(comment.listing, Listing.objects.first())
        self.assertEqual(comment.writer.username, 'tony')
        




        



