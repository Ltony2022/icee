from datetime import date, tzinfo
import datetime
import json
from django.test import TestCase
from server.flashcard.models import Flashcard
from server.flashcard.test.testdata import set_post_json, flashcard_post_json, flashcard_put_internal_json
from django.test import Client

from server import flashcard


class FlashcardTest(TestCase):
    client = Client()

    def setUp(self):
        # Set.objects.create(set_post_json)
        self.client.post(
            '/flashcards/set/new', json.dumps(set_post_json), content_type='application/json')
        self.client.post('/flashcards/set/1/create',
                         json.dumps(flashcard_post_json), content_type='application/json')
        pass

    def test_create_a_flashcard(self):
        """Flashcard creation test"""
        # response = self.client.get('/flashcards/set/1')
        self.assertEqual(Flashcard.objects.filter(set_id=1).exists(), True)

    def test_get_flashcards(self):
        """Get flashcards test"""
        response = self.client.get('/flashcards/set/1/')
        self.assertEqual(response.status_code, 200)

    def test_update_flashcard(self):
        """Update flashcard test"""
        self.client.put('/flashcards/set/1/update', json.dumps(
            {"flashcard_id": 1, "question": "Whast is the capital of France?", "answer": "Paris"}), content_type='application/json')
        self.assertEqual(Flashcard.objects.get(
            flashcard_id=1).question, "Whast is the capital of France?")
        pass

    def test_remove_flashcard(self):
        """Remove flashcard test"""
        self.client.delete('/flashcards/set/1/delete',
                           json.dumps({"flashcard_id": 1}), content_type='application/json')
        self.assertEqual(Flashcard.objects.filter(set_id=1).exists(), False)
        pass

    def test_updateDate_flashcard(self):
        self.client.put('/flashcards/set/1/updateDate', json.dumps(
            flashcard_put_internal_json), content_type='application/json')
        self.assertEqual(Flashcard.objects.get(
            flashcard_id=1).nextPractice, datetime.datetime(2022, 1, 12, 0, 0, tzinfo=datetime.timezone.utc))
