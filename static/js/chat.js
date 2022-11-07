const messageForm = document.querySelector('#message-form')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  const toPk = document.querySelector('#to-pk').innerText
  const mename = document.querySelector('#mename').innerText
  const notmename = document.querySelector('#notmename').innerText
  messageForm.addEventListener('submit', function(event) {
    event.preventDefault();
    axios({
      method: 'post',
      url: `/chats/${toPk}/send/`,
      headers: {'X-CSRFToken': csrftoken},
      data: new FormData(messageForm),
    })
    .then(response => {
      const message = document.querySelector('#message')
      removeAllchild(message)
      function removeAllchild(div) {
        while (div.hasChildNodes()) {
          div.removeChild(div.firstChild);
        }
      };
      const resdata = response.data.content;
      for (let i = 0; i < resdata.length; i++) {
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
      message.scrollTop = message.scrollHeight;
      const roomdata = response.data.room
      const roomdiv = document.querySelector('#roomdiv')
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
        console.log(roomdata)
        roomdiv.appendChild(room)
        roomdiv.appendChild(br)
        roomdiv.appendChild(br)
      }
    })
  })
  const message = document.querySelector('#message')
  message.scrollTop = message.scrollHeight;
  var cols = document.querySelectorAll('#div1 .dropdown-item');
  [].forEach.call(cols, function(col){
    col.addEventListener("click" , click , false );
  });

  function click(event){
    const omg = event.path[0].currentSrc
    messageForm.content.value = omg
    console.log(messageForm.content)
    axios({
      method: 'post',
      url: `/chats/${toPk}/send/`,
      headers: {'X-CSRFToken': csrftoken},
      data: new FormData(messageForm),
    })
    .then(response => {
      const message = document.querySelector('#message')
      removeAllchild(message)
      function removeAllchild(div) {
        while (div.hasChildNodes()) {
          div.removeChild(div.firstChild);
        }
      };
      const resdata = response.data.content;
      for (let i = 0; i < resdata.length; i++) {
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
      message.scrollTop = message.scrollHeight;
      const roomdata = response.data.room
      const roomdiv = document.querySelector('#roomdiv')
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