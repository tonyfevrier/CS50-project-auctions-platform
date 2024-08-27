from django.test import TestCase

from auctions.models import Listings, Bids, Comments
from auctions.utils import Utils


class TestListing(Utils):

    def test_listing_registration(self):
        #register and login to access the newlisting view
        self.register_and_login('tony','t@gmail.com','1234','1234') 

        #register a new listing 
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        
        #verify registration of the listing
        listing = Listings.objects.first() 

        self.assertEqual(len(Listings.objects.all()),1)
        self.assertEqual(listing.title,"titre")
        self.assertEqual(listing.id,1)
        self.assertEqual(listing.description,"here is the description")
        self.assertEqual(listing.price,10.2)
        self.assertEqual(listing.url,"http://test")
        self.assertEqual(listing.category,"toys")
        self.assertEqual(listing.creator, 'tony')

    def test_bid_initialization(self):
        self.register_and_login('tony','t@gmail.com','1234','1234') 
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.create_a_listing('titre2',"here is the description","100","http://test","toys") 

        bid1 = Bids.objects.first()
        bid2 = Bids.objects.last()

        self.assertEqual(bid1.price, 10.2)
        self.assertEqual(bid1.listing, Listings.objects.get(id=1))
        self.assertEqual(bid1.bidder, 'tony')
        self.assertEqual(bid2.price, 100)
        self.assertEqual(bid2.listing, Listings.objects.get(id=2))
        self.assertEqual(bid2.bidder, 'tony')

    def test_listing(self): 
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        response = self.client.get("/listing/1") 
        self.assertTemplateUsed(response,"auctions/listing.html")

    def test_add_to_watchlist(self):
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
 
        self.assertNotIn('tony',Listings.objects.first().followers)
        self.client.get('/toggletowatchlist/1')
        self.assertIn('tony',Listings.objects.first().followers) 
        self.client.get('/toggletowatchlist/1') 
        self.assertNotIn('tony',Listings.objects.first().followers)

    def test_two_followers_of_a_watchlist(self):
        """
        Here two persons add the same listing to their watchlist and are registered as followers.
        """
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys")
        self.client.get('/toggletowatchlist/1')
        self.assertListEqual(Listings.objects.first().followers, ['tony'])
        self.logout()
        self.register_and_login('marine','m@gmail.com','5678','5678')
        self.client.get('/toggletowatchlist/1')
        self.assertListEqual(Listings.objects.first().followers, ['tony','marine'])
        self.logout()

    def test_submit_inferior_bid(self):
        """In this case, there should be no bid saved in the database"""
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys")
        self.assertEqual(len(Bids.objects.all()), 1)
        self.submit_a_bid("10.", 1)
        self.assertEqual(len(Bids.objects.all()), 1)

    def test_submit_superior_bid(self):
        """A new bid must be saved in the database for the corresponding listing"""
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys")
        self.assertEqual(len(Bids.objects.all()), 1)
        self.submit_a_bid("20.", 1)
        self.assertEqual(len(Bids.objects.all()), 2)
        self.submit_a_bid("22.", 1)
        self.assertEqual(len(Bids.objects.all()), 3)

    def test_other_user_submit_bid(self):
        """
        A person different from the listing creator submits a bid and the bidder is correctly registered.
        """
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.logout()
        self.register_and_login('marine','m@gmail.com','5678','5678') 
        self.submit_a_bid("100",1)
        self.assertEqual(Bids.objects.first().bidder, 'tony')
        self.assertEqual(Bids.objects.last().bidder, 'marine')
        self.logout()

    def test_delete_listing(self):
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.assertEqual(len(Listings.objects.all()), 1)
        self.assertEqual(Listings.objects.first().winner, "")
        self.client.get("/listing/1/deletelisting") 
        self.assertNotEqual(Listings.objects.first().winner, "")

    def test_register_comment(self):
        self.register_and_login('tony','t@gmail.com','1234','1234')  
        self.create_a_listing('titre',"here is the description","10.2","http://test","toys") 
        self.submit_a_comment('Ceci est un commentaire', '1')
        self.submit_a_comment('Ceci est un commentaire encore', '1')
        self.submit_a_comment('Ceci est un commentaire encore une fois', '1')
        self.assertIn('Ceci est un commentaire', [comment.text for comment in Comments.objects.all()])
        self.assertIn('Ceci est un commentaire encore', [comment.text for comment in Comments.objects.all()]) 
        comment = Comments.objects.first()
        self.assertEqual(comment.listing, Listings.objects.first())
        self.assertEqual(comment.writer, 'tony')
        




        



