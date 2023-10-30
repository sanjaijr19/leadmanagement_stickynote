# # myapp/middleware.py
# from django.http import JsonResponse
#
#
# class InternetConnectionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Check if the user has no internet connection
#         if not request.META.get('HTTP_CONNECTION'):
#             return JsonResponse({'error': 'No internet connection.'}, status=400)
#         # if user has internet connection
#         response = self.get_response(request)
#         return response
#
#
