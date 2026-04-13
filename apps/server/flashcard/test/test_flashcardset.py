import json
from django.test import TestCase
from server.flashcard.models import Set
from server.flashcard.test.testdata import set_post_json, set_put_json
from django.test import Client

# Create your tests here.


class FlashcardSetTest(TestCase):
    client = Client()

    def setUp(self):
        # Set.objects.create(set_post_json)
        response = self.client.post(
            '/flashcards/set/new', json.dumps(set_post_json), content_type='application/json')

        pass

    def test_set_creation(self):
        """Set creation test"""
        self.assertEqual(Set.objects.filter(
            set_name=set_post_json['set_name']).exists(), True)

    def test_set_update(self):
        """Set update test"""
        self.client.put('/flashcards/set/update',
                        json.dumps(set_put_json), content_type='application/json')
        self.assertEqual(Set.objects.get(
            set_id=1).set_name, 'Updated Set')

    def test_set_deletion(self):
        """Set deletion test"""
        self.client.delete('/flashcards/set/delete', json.dumps(
            {'set_id': 1}), content_type='application/json')
        self.assertEqual(Set.objects.filter(
            set_name='Test Set').exists(), False)
