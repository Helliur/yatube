from django.shortcuts import render


def AboutAuthorView(request):
    template_name = 'about/author.html'
    return render(request, template_name, {'author_about': True})


def AboutTechView(request):
    template_name = 'about/tech.html'
    return render(request, template_name, {'tech_about': True})
