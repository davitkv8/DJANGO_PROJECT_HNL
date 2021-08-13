from django.shortcuts import render, redirect


def main_view(request):
    if request.method == "POST":
        subject = request.POST['subject']
        min_price = request.POST['price']
        rating = request.POST['rating'] or '0'
        return redirect('search_result', subject, min_price, int(min_price)+50, rating)
    return render(request, 'blog/index.html', {'title': 'HIRE & LEARN'})
