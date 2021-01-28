from django.shortcuts import render
from django.views import View

# Create your views here.



class Index(View):
    template_name = 'index.html'

    def get(self, request):
        turn_on_block = True
        current_user = request.user
        return render(request, self.template_name, context={'turn_on_block': turn_on_block, 'current_user': current_user})