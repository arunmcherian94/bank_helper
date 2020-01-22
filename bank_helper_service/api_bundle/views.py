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

def autocomplete(request):
    """ Autocomplete """
    try:
        if request.method == "GET":
            limit = request.GET.get('limit', 0)
            offset = request.GET.get('offset', 0)
            # TODO: Appropriate input validations
            if limit < 0 or offset < 0:
                return JsonResponse({'status':'Error','message': 'Limit/Offset values have to be more than 0'}, status=400)
            search_query = request.GET.get('q', '')
            get_branches_query = "SELECT * FROM branches WHERE branch like '%s%%' ORDER BY ifsc LIMIT %s OFFSET %s"%(search_query,limit,offset)
            response = {"branches":[]}
            db_obj = DB_helper('bank_db',get_branches_query)
            response["branches"] = db_obj.execute()
            return JsonResponse({'status':'Success','message': response}, status=200)
        else:
            return JsonResponse({'status':'Error','message': 'Method Not Allowed.'}, status=405)
    except Exception as excp:
        # TODO: Logger
        return JsonResponse({'status':'Error','message': 'Internal Server Error'}, status=500)