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
          div.className += ' justify-content-end'
          const p1 = document.createElement('p');
          const p2 = document.createElement('p');
          if (`${resdata[i][1]}`.includes('/static/imo')) {
            const p3 = document.createElement('img')
            p3.src = `${resdata[i][1]}`;
            p3.style.height = '125px';
            p3.style.width = '125px';
            p1.innerText = `${resdata[i][2]}`;
            p2.innerText = mename
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
          }
          else {
            const p3 = document.createElement('p')
            p3.innerText = `${resdata[i][1]}`
            p1.innerText = `${resdata[i][2]}`;
            p2.innerText = mename
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
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
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
          }
          else {
            const p2 = document.createElement('p')
            p2.innerText = `${resdata[i][1]}`
            p3.innerText = `${resdata[i][2]}`;
            p1.innerText = notmename
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
          }
        }
        message.appendChild(div)
      };
      messageForm.reset()
      message.scrollTop = message.scrollHeight;
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
          div.className += ' justify-content-end'
          const p1 = document.createElement('p');
          const p2 = document.createElement('p');
          if (`${resdata[i][1]}`.includes('/static/imo')) {
            const p3 = document.createElement('img')
            p3.src = `${resdata[i][1]}`;
            p3.style.height = '125px';
            p3.style.width = '125px';
            p1.innerText = `${resdata[i][2]}`;
            p2.innerText = mename
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
          }
          else {
            const p3 = document.createElement('p')
            p3.innerText = `${resdata[i][1]}`
            p1.innerText = `${resdata[i][2]}`;
            p2.innerText = mename
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
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
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
          }
          else {
            const p2 = document.createElement('p')
            p2.innerText = `${resdata[i][1]}`
            p3.innerText = `${resdata[i][2]}`;
            p1.innerText = notmename
            div.appendChild(p1);
            div.appendChild(p2);
            div.appendChild(p3);
          }
        }
        message.appendChild(div)
      };
      messageForm.reset()
      message.scrollTop = message.scrollHeight;
    })
  }