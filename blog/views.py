from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist


def main_view(request):
    if request.user.is_authenticated:
        if request.user.userstatus.status == 'None':
            return redirect('user-status')

    if request.method == "POST":
        subject = request.POST['subject']
        min_price = request.POST['price']
        rating = request.POST['rating'] or '0'
        return redirect('search_result', subject, min_price, int(min_price)+50, rating)
    return render(request, 'blog/index.html', {'title': 'HIRE & LEARN'})
