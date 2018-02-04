from django.shortcuts import render
from django.views import View


class Index(View):

    user = False

    def get(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user
        context = {
            'user': user,
        }
        return render(request, 'homepage/homepage.html', context)
