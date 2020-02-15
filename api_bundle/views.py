# Django imports
from django.http import JsonResponse
from django.conf import settings

# Utility imports
import requests
import traceback
import logging
#logger = logging.getLogger("app")
import json

from db_helper import DB_helper

def home_view(request):
    return JsonResponse({'status':'Success','message': 'Bank_helper home view'}, status=200)

def autocomplete(request):
    """ Autocomplete """
    try:
        if request.method == "GET":
            try:
                limit = int(request.GET.get('limit', 1))
                offset = int(request.GET.get('offset', 0))
            except Exception as err:
                return JsonResponse({'status':'Error','message': 'Limit and Offset parameters have to be numeric'}, status=400)
            # TODO: Appropriate input validations
            if limit < 0 or offset < 0:
                return JsonResponse({'status':'Error','message': 'Limit/Offset values have to be more than 0'}, status=400)
            search_query = request.GET.get('q', '')
            # below query was prone to SQL injection, so using named parameters instead.
            # get_branches_query = "SELECT * FROM branches WHERE branch ILIKE '%s%%' ORDER BY ifsc LIMIT %s OFFSET %s"%(search_query,limit,offset)
            get_branches_query = "SELECT * FROM branches WHERE branch ILIKE %(search_query)s ORDER BY ifsc LIMIT %(limit)s OFFSET %(offset)s"
            query_replacements = {'search_query': search_query+'%', 'offset': offset, 'limit': limit}
            response = {"branches":[]}
            db_obj = DB_helper('bank_db',get_branches_query, query_replacements)
            response["branches"] = db_obj.execute()
            return JsonResponse({'status':'Success','message': response}, status=200)
        else:
            return JsonResponse({'status':'Error','message': 'Method Not Allowed.'}, status=405)
    except Exception as excp:
        # TODO: Logger
        return JsonResponse({'status':'Error','message': 'Internal Server Error'}, status=500)


def branch_search(request):
    """ branch_search 
        TODO: Needs a better implementation.
    """
    try:
        if request.method == "GET":
            try:
                limit = int(request.GET.get('limit', 1))
                offset = int(request.GET.get('offset', 0))
            except Exception as err:
                return JsonResponse({'status':'Error','message': 'Limit and Offset parameters have to be numeric'}, status=400)
            # TODO: Appropriate input validations
            if limit < 0 or offset < 0:
                return JsonResponse({'status':'Error','message': 'Limit/Offset values have to be more than 0'}, status=400)
            search_query = request.GET.get('q', '')
            # below query was prone to SQL injection, so using named parameters instead.
            # get_branches_query = "SELECT * FROM branches WHERE %s ORDER BY ifsc LIMIT %s OFFSET %s"%(hacky_where_clause,limit,offset)
            get_branches_query = """SELECT * FROM branches WHERE ifsc ILIKE %(search_query)s OR branch ILIKE %(search_query)s
             OR address ILIKE %(search_query)s ORDER BY ifsc LIMIT %(limit)s OFFSET %(offset)s"""
            query_replacements = {'search_query': search_query+'%', 'offset': offset, 'limit': limit}
            response = {"branches":[]}
            db_obj = DB_helper('bank_db', get_branches_query, query_replacements)
            response["branches"] = db_obj.execute()
            return JsonResponse({'status':'Success','message': response}, status=200)
        else:
            return JsonResponse({'status':'Error','message': 'Method Not Allowed.'}, status=405)
    except Exception as excp:
        # TODO: Logger
        return JsonResponse({'status':'Error','message': 'Internal Server Error'}, status=500)