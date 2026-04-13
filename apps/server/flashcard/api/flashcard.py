
# A set of API endpoints for the flashcard within a flashcard set

import json
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.utils import timezone
from django.core import serializers
from django.http import JsonResponse
# Models
from flashcard.models import Flashcard
from flashcard.models import Set

# Exceptions and helpers
from flashcard.api.flashcardSetList import filter_learning_card
from src.core.exception.django_exception import method_not_allowed
from src.helpers.flashcard_helper import FlashcardHelper
from django.views.decorators.csrf import csrf_exempt

from src.utils import SM2

# Get the file path of the csv file
# outside src folder
file_path = '../../data/'
# TODO: add a configuration setting for modifying this value
development = True


def get_flashcards(request, set_id):
  if development and set_id == '' or set_id == None:
    set_id = '1'
  if request.method == "GET":
    data_to_return = Flashcard.objects.filter(set_id=set_id)
    # create a return object
    flashcard_list = list()
    # For each flashcard - get the flashcard id, question, answer and next practice date
    for i in data_to_return:
      flashcard = {
          "flashcard_id": i.flashcard_id,
          "question": i.question,
          "answer": i.answer,
          "nextPractice": datetime.strftime(i.nextPractice, '%Y-%m-%d')
      }
      flashcard_list.append(flashcard)
    # Since its already a list of objects, we can return it directly
    return JsonResponse(flashcard_list, safe=False)
  else:
    return method_not_allowed(request)

# def get_metadata_flashcards(request, set_id):
#     if development and set_id == '' or set_id == None:
#         set_id = '1'
#     if request.method == "GET":
#         data_to_return = Flashcard.objects.filter(set_id=set_id)
#         data_to_return = serializers.serialize('json', data_to_return)
#         data_to_return = json.loads(data_to_return)
#         return JsonResponse(data_to_return, safe=False)

# POST method


@csrf_exempt
def add_flashcard(request, set_id):
  if request.method == "POST":
    new_flashcard = json.loads(request.body)
    # initialize the flashcard with the default params
    flashcard_helper = FlashcardHelper()
    new_flashcard = flashcard_helper.init_flashcard(new_flashcard)
    # find the set that has the same id with set_id
    set_obj = Set.objects.get(set_id=set_id)
    flashcard_to_add = Flashcard(set_id=set_obj, EFactor=new_flashcard['EFactor'], interval=new_flashcard['interval'], repetition=new_flashcard['repetition'],
                                 nextPractice=new_flashcard['nextPractice'], lastPractice=None, question=new_flashcard['question'], answer=new_flashcard['answer'])
    flashcard_to_add.save()
    # Retrieve the flashcards again
    # Change the method to GET
    request.method = "GET"
    return get_flashcards(request, set_id)
  else:
    return method_not_allowed(request)

# PUT method
# Usually we will update the question and answer of the flashcard
# But also we can update the next practice date of the flashcard based on the user's input


@csrf_exempt
def update_flashcard(request, set_id):
  if request.method == "PUT":
    updated_data = json.loads(request.body)
    flashcard_to_update = Flashcard.objects.get(
        flashcard_id=updated_data['flashcard_id'])
    # flashcard_to_update = updated_data
    # replace the data in db with the new data
    flashcard_to_update.question = updated_data['question']
    flashcard_to_update.answer = updated_data['answer']
    flashcard_to_update.save()
    return JsonResponse({"status": "success"})
  else:
    return method_not_allowed(request)


# API endpoint for user
# to update the next practice date of the flashcard
@csrf_exempt
def update_flashcard_date(request, set_id):
  if request.method == "PUT":
    # convert the request data -> json
    updated_data = json.loads(request.body)

    # assuming the data contains
    # how well the user knows the flashcard

    # get the flashcard
    flashcard_to_update = Flashcard.objects.get(
        flashcard_id=updated_data['flashcard_id'])

    # get the user grade
    user_grade = updated_data['user_grade']

    # calculate the new date using SM2 algorithm
    number_of_dates = SM2.SM2(user_grade, flashcard_to_update.repetition,
                              flashcard_to_update.EFactor, flashcard_to_update.interval)

    # update data in the database with respect to the new data
    flashcard_to_update.lastPractice = datetime.now()
    flashcard_to_update.nextPractice = datetime.now() + timezone.timedelta(days=number_of_dates[2])
    flashcard_to_update.repetition = number_of_dates[0]
    flashcard_to_update.EFactor = number_of_dates[1]
    flashcard_to_update.interval = number_of_dates[2]

    # save the new data
    flashcard_to_update.save()
    return JsonResponse({"status": "success"})
  else:
    return method_not_allowed(request)

# Get flashcards that are due for practice


def get_practice_flashcards(request, set_id):
  if request.method == "GET":
    # get the current date and next practice date
    current_date = timezone.now()

    # retrieve the list of flashcard within the set
    flashcard_list = filter_learning_card(Flashcard.objects.filter(set_id=set_id))
    JsonResult = list()
    # convert the result to json
    for i in flashcard_list:
      flashcard = {
          "flashcard_id": i.flashcard_id,
          "question": i.question,
          "answer": i.answer,
          "nextPractice": datetime.strftime(i.nextPractice, '%Y-%m-%d')
      }
      JsonResult.append(flashcard)

    return JsonResponse(JsonResult, safe=False)
  else:
    return method_not_allowed(request)


# TODO: Update branch for updating the new date of the flashcard


def update_flashcard_internal(request, set_id):
  if request.method == "PUT":
    updated_data = json.loads(request.body)
    flashcard_to_update = Flashcard.objects.get(
        flashcard_id=updated_data['flashcard_id'])
    # flashcard_to_update = updated_data
    processed_time = datetime.strptime(
        updated_data['nextPractice'], '%Y-%m-%d')
    next_practice = make_aware(processed_time)
    flashcard_to_update.nextPractice = next_practice
    flashcard_to_update.save()
    return JsonResponse({"status": "success"})
  else:
    return method_not_allowed(request)


# DELETE method

@csrf_exempt
def delete_flashcard(request, set_id):
  if request.method == "DELETE":
    # convert the request data -> json
    print(request.body)
    flashcard_to_delete = json.loads(request.body)
    flashcard_to_update = Flashcard.objects.get(
        flashcard_id=flashcard_to_delete['flashcard_id'])
    flashcard_to_update.delete()
    # Refetch the flashcards
    request.method = "GET"
    return get_flashcards(request, set_id)
  else:
    return method_not_allowed(request)
