from django.views import generic


class IndexView(generic.ListView):
    template_name = 'league/home_page.html'

    def get_queryset(self):
        """
        Gives an empty queryset to allow loading of the home page.
        """
        return None
