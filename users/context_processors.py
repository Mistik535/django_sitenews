from news.utils import menu


def get_news_context(request):
    return {'mainmenu': menu}
