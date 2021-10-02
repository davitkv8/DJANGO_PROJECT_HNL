from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Relationship
from .models import TimeTable, Feedback, ChatRoom
from classroom.today import find_nearest_lecture_time
from users.models import TeachersProfile
import json


def classroom(request):
    lecturers = Relationship.objects.filter(sender=request.user, status="Approve").all()
    lectures_list = []
    for lecture in lecturers:
        nearest_lesson = find_nearest_lecture_time(lecture.available_time)
        lectures_list.append({"TeacherObject": lecture, "nearestLesson": nearest_lesson})

    if request.is_ajax() and request.method == "POST":
        feedback_text = request.POST['feedbackText']
        feedback_rating = int(request.POST['feedbackRating'])
        lecturer_id = int(request.POST['lecturer'])

        Feedback.objects.create(rating=feedback_rating, textFeedback=feedback_text,
                                sender=request.user, receiver_id=lecturer_id)

    return render(request, 'classroom/classroom.html', {'lecturers': lectures_list})


def redirecter(request, student, lecturer):
    room_name = student + '_' + lecturer
    return redirect('chat_room', room_name)


@login_required
def chat_room(request, room_name):
    room = ChatRoom.objects.filter(roomName=room_name).first()
    if room is None:
        room = ChatRoom.objects.create(roomName=room_name)
        chat_members = room_name.split('_')
        for chat_member in chat_members:
            user = User.objects.filter(username=chat_member).first()
            room.members.add(user)

    if request.user not in room.members.all():
        return HttpResponse(status=404)

    chattingwith = ''
    for user in room.members.all():
        if request.user != user:
            chattingwith = user

    message = ChatRoom.objects.get(roomName=room_name)
    messages = message.get_messages()
    total_messages = message.count_messages()

    if request.user.is_staff:
        relationships = Relationship.objects.filter(status="Approve", receiver=request.user.teachersprofile).all()

    else:
        relationships = Relationship.objects.filter(status="Approve", sender=request.user).all()

    if request.is_ajax() and request.method == "POST":

        request_user = User.objects.filter(username=request.POST['request_user']).first()
        chat_member = User.objects.filter(username=request.POST['chat_member']).first()
        new_room_name = request_user.username + '_' + chat_member.username
        response = {'status': 1, 'message': "Ok", 'url': new_room_name}
        if ChatRoom.objects.filter(roomName=new_room_name).first() is None:
            new_room = ChatRoom.objects.create(roomName=new_room_name)
            new_room.members.add(chat_member, request_user)
            new_room.save()
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            return HttpResponse(json.dumps(response), content_type='application/json')

    return render(request, 'classroom/chatroom.html', {'room_name': room_name, 'messages': messages,
                                                       'chattingWith': chattingwith, 'totalMessages': total_messages,
                                                       'chatMembers': relationships})


class AjaxTimeTable(View):

    def get(self, request, user_pk):
        user_table = TimeTable.objects.filter(user=user_pk).first()
        if user_table is None:
            return render(request, 'classroom/time_table.html', {"object": int(user_pk)})
        return render(request, 'classroom/time_table.html', {'days': user_table.available_time,
                                                             "object": int(user_pk)})

    def post(self, request, user_pk):
        user_pk = int(user_pk)
        user = User.objects.get(pk=user_pk)
        days = request.POST['availableDays']
        days = json.loads(days)
        created = TimeTable.objects.filter(user=request.user).first()

        if request.user == user:
            if created is None:
                created = TimeTable.objects.create(user=request.user)
                created.available_time = []
            for day in days['availableDays']:
                created.available_time.append(day)

            for day in days['unavailableDays']:
                if day in created.available_time:
                    created.available_time.remove(day)

            created.save()

        else:
            relationship = Relationship.objects.create(sender=request.user,
                                                       receiver=TeachersProfile.objects.get(pk=user.teachersprofile.pk),
                                                       status="send")
            relationship.available_time = []
            for day in days['availableDays']:
                relationship.available_time.append(day)
            relationship.save()
        return HttpResponse()


def requested_table(request, student_user, teacher_user):
    relationship = Relationship.objects.get(receiver__full_name=teacher_user, sender__username=student_user)
    return render(request, "classroom/time_table.html", {'days': relationship.available_time,
                                                         'object': None})
