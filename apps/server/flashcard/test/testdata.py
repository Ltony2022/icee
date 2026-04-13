from server import flashcard


set_post_json = {
    "set_name": "Test Set",
    "nearest_practice": "10/10/2021"
}

set_put_json = {
    'set_id': 1,
    'set_name': 'Updated Set',
    'nearest_practice': '2022-01-12'
}

flashcard_post_json = {
    "question": "What is the capital of France?",
    "answer": "Paris"
}

flashcard_put_internal_json = {
    "flashcard_id": 1,
    "nextPractice": "2022-01-12"
}
