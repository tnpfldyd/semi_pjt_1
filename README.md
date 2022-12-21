배포 사이트 주소: https://semipjt1.herokuapp.com/ 무료 종료로 더이상 이용불가..
## Semi Project 01

- **기간**: 2022.10.31 ~ 2022.11.07
- **팀명**: 중고의 집
- **주제**: 상품 정보 및 후기 공유 커뮤니티 서비스


### 📌 맡은 역할

- 이용환 회원app, 채팅app, 전반적인 BE, 발표



### 📌 서비스 화면

![중고의집](README.assets/중고의집.gif)



### 📌 맡은 기능 소개

- 채팅 app

  - models.py

    ```python
    from django.db import models
    from django.conf import settings
    
    class MessageRoom(models.Model):
        to_user = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="send_user"
        )
        from_user = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver_user"
        )
        count = models.IntegerField(default=0)
        last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='last')
        last_message = models.TextField()
        updated_at = models.DateTimeField(auto_now=True)
    
    class DirectMessage(models.Model):
        room_number = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)
        recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipient_name")
        content = models.TextField()
        create_at = models.DateTimeField(auto_now_add=True)
        read = models.BooleanField(default=False)
    ```

  - urls.py

    ```python
    from django.urls import path
    from . import views
    
    app_name = 'chats'
    
    urlpatterns = [
        path("", views.index, name="index"), # 메인페이지
        path("<int:pk>/send/", views.send, name="send"), #detail 에서 보낼 때 사용
        path("<int:room_pk>/", views.detail, name="detail"), #채팅 상세보기 페이지
        path("<int:pk>/first_send/", views.first_send, name="first_send"), #DM 버튼을 누르고 메세지를 보낼 때 사용
        path('<int:pk>/delete/', views.delete, name='delete'), # 채팅방 삭제 버튼
    ]
    ```

  - views.py

    ```python
    from django.shortcuts import render, redirect, get_object_or_404
    from .models import MessageRoom, DirectMessage
    from django.contrib.auth.decorators import login_required
    from .forms import DirectMessageForm
    from django.contrib.auth import get_user_model
    from django.views.decorators.http import require_POST
    from django.http import JsonResponse
    # Create your views here.
    
    @login_required
    #메인 페이지. 내가 받는 사람일 때, 내가 보낸 사람일 때의 모든 방을 인덱스 페이지로 전송 카톡처럼 마지막 메세지를 보이기위함
    def index(request): 
        user = get_user_model().objects.get(pk=request.user.pk)
        send = user.send_user.all()
        receiver = user.receiver_user.all()
        context = {"messagerooms": send.union(receiver, all=False).order_by("-updated_at")}
        return render(request, "chats/index.html", context)
    
    
    @login_required
    #상세 페이지. 좌측엔 현재 참여해있는 방을 보여주고 우측은 메세지를 띄워주기 위하여 채팅방의 정보와 현재 접속한 방의 정보를 전송
    def detail(request, room_pk):
        room_info = get_object_or_404(MessageRoom, pk=room_pk)
        if request.user == room_info.to_user or request.user == room_info.from_user:
            user = get_user_model().objects.get(pk=request.user.pk)
            send = user.send_user.all()
            receiver = user.receiver_user.all()
            if request.user.id != room_info.last_user_id and room_info.count > 0:
                room_info.count = 0
                room_info.save()
            messages = DirectMessage.objects.filter(room_number_id=room_pk)
            if DirectMessage.objects.filter(room_number_id=room_pk, recipient_id=request.user, read=False).exists():
                temp = DirectMessage.objects.filter(room_number_id=room_pk, recipient_id=request.user, read=False)
                for i in temp:
                    i.read = True
                    i.save()
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
    # 내가 받는 사람이고 상대가 보내는 사람의 방이 있는지, 혹은 그 반대로 된 경우가 있는지 확인 후에 없으면 방을 생성
    def send(request, pk):
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            if MessageRoom.objects.filter(to_user_id=request.user.id, from_user_id=pk).exists():
                room = MessageRoom.objects.get(to_user_id=request.user.id, from_user_id=pk)
                temp = form.save(commit=False)
                temp.room_number_id = room.id
                temp.recipient_id = pk
                temp.save()
                room.last_user_id = request.user.id
                room.last_message = temp.content
                if request.user.id != temp.recipient_id:
                    room.count += 1
                room.save()
                roominfo = []
                user = get_user_model().objects.get(pk=request.user.pk)
                send = user.send_user.all()
                receiver = user.receiver_user.all()
                sere = send.union(receiver, all=False).order_by("-updated_at")
                for i in sere:
                    if request.user == i.to_user:
                        temp = i.from_user.username
                    else:
                        temp = i.to_user.username
                    if '/static/imo' in i.last_message:
                        text = '이모티콘을 전송하였습니다.'
                    else:
                        text = i.last_message
                    roominfo.append((i.updated_at, temp, text, i.pk))
                arr = []
                messages = DirectMessage.objects.filter(room_number_id=room.pk)
                for i in messages:
                    arr.append((i.recipient.pk, i.content, i.create_at, i.read))
                context = {
                    'content': arr,
                    'room': roominfo,
                }
    
    
                return JsonResponse(context)
            else:
                if MessageRoom.objects.filter(to_user_id=pk, from_user_id=request.user.id).exists():
                    room = MessageRoom.objects.get(to_user_id=pk, from_user_id=request.user.id)
                    temp = form.save(commit=False)
                    temp.room_number_id = room.id
                    temp.recipient_id = pk
                    temp.save()
                    room.last_user_id = request.user.id
                    room.last_message = temp.content
                    if request.user.id != temp.recipient_id:
                        room.count += 1
                    room.save()
                    roominfo = []
                    user = get_user_model().objects.get(pk=request.user.pk)
                    send = user.send_user.all()
                    receiver = user.receiver_user.all()
                    sere = send.union(receiver, all=False).order_by("-updated_at")
                    for i in sere:
                        if request.user == i.to_user:
                            temp = i.from_user.username
                        else:
                            temp = i.to_user.username
                        if '/static/imo' in i.last_message:
                            text = '이모티콘을 전송하였습니다.'
                        else:
                            text = i.last_message
                        roominfo.append((i.updated_at, temp, text, i.pk))
                    arr = []
                    messages = DirectMessage.objects.filter(room_number_id=room.pk)
                    for i in messages:
                        arr.append((i.recipient.pk, i.content, i.create_at, i.read))
                    context = {
                        'content': arr,
                        'room': roominfo,
                    }
                    return JsonResponse(context)
                else:
                    temp = form.save(commit=False)
                    room = MessageRoom.objects.create(
                        to_user_id=request.user.id,
                        from_user_id=pk,
                        count = 0,
                        last_user_id=request.user.id,
                        last_message=temp.content,
                    )
                    temp.room_number_id = room.id
                    temp.recipient_id = pk
                    if request.user.id != temp.recipient_id:
                        room.count = 1
                    room.save()
                    temp.save()
                    roominfo = []
                    user = get_user_model().objects.get(pk=request.user.pk)
                    send = user.send_user.all()
                    receiver = user.receiver_user.all()
                    sere = send.union(receiver, all=False).order_by("-updated_at")
                    for i in sere:
                        if request.user == i.to_user:
                            temp = i.from_user.username
                        else:
                            temp = i.to_user.username
                        if '/static/imo' in i.last_message:
                            text = '이모티콘을 전송하였습니다.'
                        else:
                            text = i.last_message
                        roominfo.append((i.updated_at, temp, text, i.pk))
                    arr = []
                    messages = DirectMessage.objects.filter(room_number_id=room.pk)
                    for i in messages:
                        arr.append((i.recipient.pk, i.content, i.create_at, i.read))
                    context = {
                        'content': arr,
                        'room': roominfo,
                    }
                    return JsonResponse(context)
        return render(request, "chats/detail.html", {"form": form})
    
    @login_required
    #방 삭제버튼
    def delete(request, pk):
        room = get_object_or_404(MessageRoom, pk=pk)
        if room.to_user_id == request.user.pk or room.from_user_id == request.user.pk:
            room.delete()
        return redirect('chats:index')
    
    #DM 버튼을 누르고 메세지 보내는 로직은 send와 거의 동일하여 생략
    ```

  - HTML 설정

    ```html
    <ul class="dropdown-menu" style="width: 600px;">
        <div class="row row-cols-4" id="div1">
            <div><img class="dropdown-item" src="{% static 'imo/carrot/1.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/2.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/3.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/4.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/5.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/6.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/7.png' %}" style="width: 125px; height: 125px;"></div>
            <div><img class="dropdown-item" src="{% static 'imo/carrot/8.png' %}" style="width: 125px; height: 125px;"></div>
        </div>
    </ul>
    ```

    

  - JavaScript 설정 - 이모티콘 전송 (일반 메세지 전송은 쉽기에 생략)

    ```javascript
    const message = document.querySelector('#message')
      message.scrollTop = message.scrollHeight; // 메세지 div는 스크롤 하단고정 되도록
      var cols = document.querySelectorAll('#div1 .dropdown-item'); // 드롭다운에 등록된 모든 아이템들 이벤트 등록
      [].forEach.call(cols, function(col){
        col.addEventListener("click" , click , false );
      });
    
      function click(event){
        const omg = event.path[0].currentSrc // 클릭 시 뭘 클릭했는지 나오는 곳
        messageForm.content.value = omg
        console.log(messageForm.content)
        axios({ // axios 로 전송 로직
          method: 'post',
          url: `/chats/${toPk}/send/`,
          headers: {'X-CSRFToken': csrftoken},
          data: new FormData(messageForm),
        })
        .then(response => {
          const message = document.querySelector('#message') // 받아왔을 때 기존의 메세지 div의 모든 내용 삭제
          removeAllchild(message)
          function removeAllchild(div) {
            while (div.hasChildNodes()) {
              div.removeChild(div.firstChild);
            }
          };
          const resdata = response.data.content;
          for (let i = 0; i < resdata.length; i++) { // 삭제 후 받아온 모든 메세지를 붙여 줌, 보낸 메세지면 우측 받는 메세지면 좌측
            const div = document.createElement('div')
            div.className = 'd-flex';
            if (resdata[i][0] === Number(toPk)) {
              div.className += ' justify-content-end position-relative'
              const p1 = document.createElement('p');
              const p2 = document.createElement('p');
              if (`${resdata[i][1]}`.includes('/static/imo')) {
                const p3 = document.createElement('img')
                p3.src = `${resdata[i][1]}`;
                p3.style.height = '125px';
                p3.style.width = '125px';
                p1.innerText = `${resdata[i][2]}`;
                p2.innerText = mename
                const temp = document.createElement('div')
                temp.appendChild(p2);
                temp.appendChild(p3);
                temp.appendChild(p1);
                div.appendChild(temp)
              }
              else {
                const p3 = document.createElement('p')
                p3.innerText = `${resdata[i][1]}`
                p1.innerText = `${resdata[i][2]}`;
                p2.innerText = mename
                const temp = document.createElement('div')
                temp.appendChild(p2);
                temp.appendChild(p3);
                temp.appendChild(p1);
                div.appendChild(temp)
              }
              if (`${resdata[i][3]}` === 'false') {
                const p4 = document.createElement('p')
                p4.className = 'rounded-circle'
                p4.className += ' bg-white fw-bold text-center text-warning position-absolute bottom-0 start-50'
                p4.style.width = "25px;"
                p4.innerText = '1'
                div.appendChild(p4)
              }
            }
            else {
              div.className += ' justify-content-start'
              const p1 = document.createElement('p')
              const p3 = document.createElement('p');
              if (`${resdata[i][1]}`.includes('/static/imo')) {
                const p2 = document.createElement('img')
                p2.src = `${resdata[i][1]}`;
                p2.style.height = '125px';
                p2.style.width = '125px';
                p3.innerText = `${resdata[i][2]}`;
                p1.innerText = notmename
                const temp = document.createElement('div')
                temp.appendChild(p1);
                temp.appendChild(p2);
                temp.appendChild(p3);
                div.appendChild(temp)
              }
              else {
                const p2 = document.createElement('p')
                p2.innerText = `${resdata[i][1]}`
                p3.innerText = `${resdata[i][2]}`;
                p1.innerText = notmename
                const temp = document.createElement('div')
                temp.appendChild(p1);
                temp.appendChild(p2);
                temp.appendChild(p3);
                div.appendChild(temp)
              }
            }
            message.appendChild(div)
          };
          messageForm.reset()
          message.scrollTop = message.scrollHeight; // 모든 메세지 출력 후 스크롤 하단 고정
          const roomdata = response.data.room
          const roomdiv = document.querySelector('#roomdiv') // 참여한 채팅방 정보 새로 고침 해주는 로직
          removeAllchild(roomdiv)
          function removeAllchild(div) {
            while (div.hasChildNodes()) {
              div.removeChild(div.firstChild);
            }
          };
          for (let i = 0; i < roomdata.length; i++) {
            const room = document.createElement('a');
            const br = document.createElement('br');
            room.className = 'text-decoration-none'
            room.href = `/chats/${roomdata[i][3]}`
            room.innerText = `${roomdata[i][1]}\n${roomdata[i][2]}\n${roomdata[i][0]}`
    
            roomdiv.appendChild(room)
            roomdiv.appendChild(br)
            roomdiv.appendChild(br)
          }
        })
      }
    ```




### 📌 생긴 오류 및 해결

- django-imoji-picker 앱을 사용하여 채팅에서 이모지 전송을 구현하고 싶었으나, 앱을 사용하려면 React와 연동해야 사용가능 할 것 같아서 서버 static 폴더에 이미지를 저장 한 뒤 이미지 박스가 클릭이 될 경우 해당 이미지의 static 파일명을 상대에게 javascript를 통하여 비동기로 전송하도록 구현. static/js/chat.js 
Message DB 에는 파일명만 저장이 되고, 화면에 노출시엔 load static을 활용하여 화면에 노출



### 📌 서비스 주요 기능

---

- 회원관리
  - 회원가입
  - 로그인
  - 로그아웃
  - 회원 프로필
  - 팔로우 / 취소
  - 블랙리스트
- 지역 커뮤니티
  - 이미지 업로드
  - 글 수정 / 삭제
  - 좋아요 / 취소
  - 댓글 작성 / 수정 / 삭제 / 신고
  - 대댓글 작성 / 수정 / 삭제 / 신고
- 상품
  - 이미지 업로드
  - 글 수정 / 삭제
  - 좋아요 / 취소
  - 판매 위치 또는 택배 거래 유무
  - 판매자가 파는 다른 상품 소개
  - 매너온도
- 채팅
  - 1:1 대화 구현
  - 이모티콘 전송 
- 검색
  - 인기 검색어 순위
- 문의하기
  - 문의 제목
  - 문의 글
  - 사진 업로드 (선택)
  - 자주 묻는 질문 (후순위)



### 📌 화면 설계

---

![templates_structure](README.assets/templates_structure.png)



### 📌DB 모델링

---

![ERD](README.assets/ERD.png)
