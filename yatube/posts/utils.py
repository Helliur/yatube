from django.core.paginator import Paginator


def paginator(posts, SHOW_COUNT, request):
    paginator = Paginator(posts, SHOW_COUNT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
