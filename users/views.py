from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import authenticate, login


# VERIFICATION
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator

# IMPORTING MY MODELS
from .forms import TeacherRegisterForm, TeacherProfileForm
from .models import TeachersProfile, Relationship
from classroom.models import TimeTable


def email_verification(request, pk):
    user = User.objects.filter(pk=pk).first()
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    link = reverse('verification-view', kwargs={'uidb64': uidb64,
                                                'token': token_generator.make_token(
                                                    user)})
    activate_url = 'http://' + domain + link
    email_subject = 'Account Verification'
    email_body = 'Hello ' + user.username + \
                 ' Please use this link to verify your account ' + activate_url
    send_mail(
        email_subject,
        email_body,
        'django@admin.com',
        ['davit.kv8@gmail.com'],
        fail_silently=False
    )

    return redirect('teacher-profile', request.user.teachersprofile.pk)


def register(request):
    form = TeacherRegisterForm
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            registered_user = User.objects.filter(username=form.cleaned_data['username']).first()

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            if request.POST['user'] == 'teacher':
                registered_user.is_staff = True
                registered_user.save()
                return redirect('complete-user', registered_user.pk)
            else:
                return redirect('main-view')

    return render(request, 'users/register.html', {'form': form})


@login_required
def complete_user_registration(request, pk):  # User's Primary key
    if request.user.pk != pk:
        return redirect('main-view')
    try:
        if request.user.teachersprofile:
            return redirect('teacher-profile', request.user.teachersprofile.pk)
    except:
        pass
    form = TeacherProfileForm
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            teacher_profile_object = TeachersProfile(birth_date=form_data['birth_date'],
                                                     full_name=form_data['full_name'],
                                                     lecture_price=form_data['lecture_price'],
                                                     description=form_data['description'],
                                                     platform=form_data['platform'],
                                                     subject=form_data['subject'],
                                                     image=request.FILES['image'], user=request.user)
            teacher_profile_object.save()
            return email_verification(request, pk)

    return render(request, 'users/complete_user.html', {'form': form})


class UpdateTeacherProfileView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = TeachersProfile
    template_name = 'users/profile.html'
    context_object_name = 'object'
    fields = ['full_name', 'lecture_price', 'description',
              'platform', 'subject']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friendRequest'] = Relationship.objects.filter(receiver=self.object, status='send').all()
        context['hasTimeTable'] = TimeTable.objects.filter(user=self.object.user).first()
        context['feedbacks'] = self.object.feedback.all().order_by('date')[:10]
        context['verification_request'] = email_verification(request=self.request, pk=self.request.user.pk)
        return context

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            rel = Relationship.objects.get(receiver=request.user.teachersprofile,
                                           sender=request.POST["user"], status="send")
            if request.POST["type"] == "approve":
                rel.status = "Approve"
                rel.save()
            else:
                rel.delete()
            return HttpResponse()
        else:
            return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('teacher-profile', kwargs={'pk': self.object.pk})


def search_result(request, subject, min_price=0, max_price=10000, rating=0):
    final_result = []
    search_results = TeachersProfile.objects.filter(subject=subject).all().order_by('-feedback__rating')
    for result in search_results:
        if result not in final_result and result.lecture_price in range(int(min_price), int(max_price))\
                and result.feedback_rating() >= int(rating):
            final_result.append(result)
    results_number = final_result.__len__()
    return render(request, 'users/search_result.html', {'teachers': final_result, 'result_number': results_number})


def lectures_detailed(request, subject, pk):
    profile = TeachersProfile.objects.get(pk=pk)
    feedbacks = profile.feedback.all()
    if request.user == profile.user:
        return redirect("teacher-profile", request.user.teachersprofile.pk)
    if request.method == "POST":
        return redirect("time_table", profile.user.pk)
    return render(request, 'users/profile.html', {'object': profile, 'feedbacks': feedbacks})


def relationships(request):
    receiver = TeachersProfile.objects.get(pk=request.user.teachersprofile.pk)
    relationship = Relationship.objects.filter(receiver=receiver, status="send").all()

    if request.method == "POST":
        for i in relationship:
            if str(i.sender.pk) in request.POST:
                approved_relationship = Relationship.objects.filter(receiver=receiver, sender=i.sender).first()
                approved_relationship.status = "Approve"
                approved_relationship.save()
    return render(request, 'users/relationships.html', {'requests': relationship})


class VerificationView(View):
    def get(self, request, uidb64, token):
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        teacher_profile = TeachersProfile.objects.get(user=user)
        teacher_profile.is_active = True
        teacher_profile.save()
        return redirect('teacher-profile', request.user.teachersprofile.pk)
