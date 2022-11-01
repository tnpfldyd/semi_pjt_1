from django.shortcuts import render, redirect, get_object_or_404
from .models import MessageRoom, DirectMessage
from django.contrib.auth.decorators import login_required
from .forms import DirectMessageForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

# Create your views here.

def test(request):
    form = DirectMessageForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('chats:index')
    return render(request, 'chats/test.html', {'form':form})

@login_required
def index(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    send = user.send_user.all()
    receiver = user.receiver_user.all()
    context = {"messagerooms": send.union(receiver, all=False).order_by("-updated_at")}
    return render(request, "chats/index.html", context)


@login_required
def detail(request, room_pk):
    room_info = get_object_or_404(MessageRoom, pk=room_pk)
    if request.user == room_info.to_user or request.user == room_info.from_user:
        user = get_user_model().objects.get(pk=request.user.pk)
        send = user.send_user.all()
        receiver = user.receiver_user.all()
        messages = DirectMessage.objects.filter(room_number_id=room_pk)
        room_info = get_object_or_404(MessageRoom, pk=room_pk)
        form = DirectMessageForm()
        context = {
            "room_info": room_info,
            "messagerooms": send.union(receiver, all=False).order_by("-updated_at"),
            "messages": messages,
            "form": form,
        }
        return render(request, "chats/detail.html", context)
    return redirect("chats:index")


@require_POST
def send(request, pk):
    form = DirectMessageForm(request.POST)
    if form.is_valid():
        if MessageRoom.objects.filter(to_user_id=request.user.id, from_user_id=pk).exists():
            room = MessageRoom.objects.get(to_user_id=request.user.id, from_user_id=pk)
            temp = form.save(commit=False)
            temp.room_number_id = room.id
            temp.who_id = pk
            temp.save()
            room.last_user = request.user.username
            room.last_message = temp.content
            room.count += 1
            room.save()
            return redirect("chats:detail", room.pk)
        else:
            if MessageRoom.objects.filter(to_user_id=pk, from_user_id=request.user.id).exists():
                room = MessageRoom.objects.get(to_user_id=pk, from_user_id=request.user.id)
                temp = form.save(commit=False)
                temp.room_number_id = room.id
                temp.who_id = pk
                temp.save()
                room.last_user = request.user.username
                room.last_message = temp.content
                room.count += 1
                room.save()
                return redirect("chats:detail", room.pk)
            else:
                temp = form.save(commit=False)
                room = MessageRoom.objects.create(
                    to_user_id=request.user.id,
                    from_user_id=pk,
                    count=1,
                    last_user=request.user,
                    last_message=temp.content,
                )
                temp.room_number_id = room.id
                temp.who_id = pk
                temp.save()
                return redirect("chats:detail", room.pk)
    return render(request, "chats/detail.html", {"form": form})


@login_required
def first_send(request, pk):
    form = DirectMessageForm(request.POST or None)
    if form.is_valid():
        if MessageRoom.objects.filter(to_user_id=request.user.id, from_user_id=pk).exists():
            room = MessageRoom.objects.get(to_user_id=request.user.id, from_user_id=pk)
            temp = form.save(commit=False)
            temp.room_number_id = room.id
            temp.who_id = pk
            temp.save()
            room.last_user = request.user.username
            room.last_message = temp.content
            room.count += 1
            room.save()
            return redirect("chats:detail", room.pk)
        else:
            if MessageRoom.objects.filter(to_user_id=pk, from_user_id=request.user.id).exists():
                room = MessageRoom.objects.get(to_user_id=pk, from_user_id=request.user.id)
                temp = form.save(commit=False)
                temp.room_number_id = room.id
                temp.who_id = pk
                temp.save()
                room.last_user = request.user.username
                room.last_message = temp.content
                room.count += 1
                room.save()
                return redirect("chats:detail", room.pk)
            else:
                temp = form.save(commit=False)
                room = MessageRoom.objects.create(
                    to_user_id=request.user.id,
                    from_user_id=pk,
                    count=1,
                    last_user=request.user,
                    last_message=temp.content,
                )
                temp.room_number_id = room.id
                temp.who_id = pk
                temp.save()
                return redirect("chats:detail", room.pk)
    return render(request, "chats/send.html", {"form": form})
