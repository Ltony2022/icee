from django.urls import path

from flashcard.api.flashcard import add_flashcard, get_flashcards, update_flashcard, delete_flashcard, update_flashcard_date, update_flashcard_internal
from flashcard.api.flashcardSetList import create_new_set, delete_set, get_flashcard_list, update_set, get_set_metadata
from server.flashcard.api.flashcard import get_practice_flashcards


urlpatterns = [
    path("set", get_flashcard_list),
    path("set/<str:set_id>/", get_flashcards, name='set_id'),
    path("set/<str:set_id>/info", get_set_metadata, name='set_id'),
    path("set/new", create_new_set),
    path("set/update", update_set),
    path("set/delete", delete_set),

    # Flashcard CRUD
    path("set/<str:set_id>/create", add_flashcard, name='set_id'),
    path("set/<str:set_id>/update", update_flashcard, name='set_id'),
    path("set/<str:set_id>/delete", delete_flashcard, name='set_id'),
    path("set/<str:set_id>/updateDate", update_flashcard_internal, name='set_id'),
    path("set/<str:set_id>/updateUserFlashcard", update_flashcard_date, name='set_id'),
    path("set/<str:set_id>/getPracticeFlashcard", get_practice_flashcards, name='set_id')
]
