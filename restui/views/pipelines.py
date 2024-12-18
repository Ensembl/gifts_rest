from celery.result import AsyncResult

from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import connection

class CheckJobStatus(APIView):

    def get_search_path(self):
        with connection.cursor() as cursor:
            cursor.execute("SHOW search_path;")
            search_path = cursor.fetchone()
            return search_path

    def get(self, request, task_id):
        result = AsyncResult(task_id)
        task_status = result.status
        # result.info is a read-only property in the AsyncResult class, we cannot modify it directly
        # otherwise we get the error AttributeError: can't set attribute
        task_info = result.info

        # To avoid ERROR: Object of type 'ProgrammingError' is not JSON serializable
        if not isinstance(task_info, str):
            task_info = str(task_info)

        task_info = f"[search_path is: {self.get_search_path()}] " + task_info

        # Possible task status: PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED, <CUSTOM STATE>
        return Response({"status": task_status, "info": task_info})
