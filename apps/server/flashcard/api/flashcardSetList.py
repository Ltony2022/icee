from datetime import UTC, date, datetime, tzinfo
import json
import sys

from django.http import JsonResponse
from django.core import serializers
from django.utils.timezone import make_aware


from flashcard.models import Flashcard, Set
from src.core.exception.django_exception import method_not_allowed
from django.views.decorators.csrf import csrf_exempt


# Get the name of the flashcard in the directory
path_to_src = sys.path[0]
path_to_data = "/../../data/"

# GET Method
# 1. All method


def get_flashcard_list(request):
  if (request.method == 'GET'):
    # tweak to get only the fields that we want
    query = list(Set.objects.all().values(
        'set_id', 'set_name', 'nearest_practice'))
    

    # Define new dictionary to store the data
    data_to_return = list()
    # Loop through the query and add it to the dictionary
    for i in query:
      # Fields to get
      set_name = i['set_name']
      set_id = i['set_id']
      
      # retrieve the flashcards that are in the set
      queryFlashcard = Flashcard.objects.filter(set_id=set_id)      
      # count the number of flashcards that is after the date (todo)
      flashcard_need_review = filter_learning_card(queryFlashcard)

      # Process the date
      next_practice_date = i['nearest_practice']
      if next_practice_date is not None:
        next_practice_date = datetime.strftime(
            next_practice_date, '%d-%m-%Y')
      else:
        next_practice_date = "Not set"
      #  Get flashcards count
      flashcards = Flashcard.objects.filter(set_id=set_id)
      flashcards_count = flashcards.count()
      # New object and rename the field to match the frontend
      json_object = {"setId": set_id, "name": set_name, "numberOfCards": flashcards_count,
                     "nextLearningDay": next_practice_date, "needReview": len(flashcard_need_review)}
      data_to_return.append(json_object)
    print(data_to_return)
    return JsonResponse(data_to_return, safe=False)


# def flashcard_object(flashcards_len, next_learning_day, title):
#     flashcard_info = {"name": title, "numberOfCards": flashcards_len,
#                       "nextLearningDay": next_learning_day}
#     return flashcard_info


def get_set_metadata(request, set_id):
  """This function will return the metadata of the set

  Args:
      request (django.Request): Request object of django
      set_id (string): The set id

  Returns:
      JSONResponse: data sent to client
  """
  if (request.method == 'GET'):
    # query the set with id only
    query = Set.objects.get(set_id=set_id)
    # Query the flashcards with the set id
    queryFlashcard = Flashcard.objects.filter(set_id=set_id)
    # count the number of flashcards that is after the date (todo)
    flashcard_need_review = filter_learning_card(queryFlashcard)
    # Return the data
    data_to_return = {
        "setName": query.set_name,
        # "nextLearningDay": query.nearest_practice,
        # count total flashcards
        "totalFlashcards": queryFlashcard.count(),
        "needReview": len(flashcard_need_review)
    }
    return JsonResponse(data_to_return, safe=False)
  return method_not_allowed()


def filter_learning_card(queryFlashcard):
  '''
  This utility function will filter the flashcard by the next practice date
  @param queryFlashcard: Queryset of flashcard
  @return: filtered set of flashcard
  '''
  filtered_set = list()
  current_time = make_aware(datetime.now())
  # Loop through the query and add it to the dictionary
  for i in queryFlashcard:
    if i.nextPractice <= current_time or i.lastPractice is None:
      # print(i.nextPractice)
      filtered_set.append(i)
    else:
      continue
  return filtered_set

# POST request


@csrf_exempt
def create_new_set(request):
  if (request.method == 'POST'):
    data_to_add = json.loads(request.body)
    set_to_add = Set(
        set_name=data_to_add.get('set_name'))
    set_to_add.save()
    return JsonResponse({"status": "success"})
  return method_not_allowed()

# PUT request


def update_set(request):
  if (request.method == 'PUT'):
    # Get the data from id

    data_to_update = json.loads(request.body)
    set_being_updated = Set.objects.get(set_id=data_to_update['set_id'])
    date_to_update = data_to_update['nearest_practice']
    # convert the date to datetime object (add the timezone info)
    date_to_update = make_aware(datetime.strptime(
        date_to_update, '%Y-%m-%d'))
    # update the date
    set_being_updated.nearest_practice = date_to_update
    # update the set
    set_being_updated.set_name = data_to_update['set_name']
    set_being_updated.save()
    return JsonResponse({"status": "success"})
  return method_not_allowed()

# DELETE request


def delete_set(request):
  if (request.method == 'DELETE'):
    data_to_delete = json.loads(request.body)
    set_being_deleted = Set.objects.get(set_id=data_to_delete['set_id'])
    set_being_deleted.delete()
    return JsonResponse({"status": "success"})
  return method_not_allowed()
