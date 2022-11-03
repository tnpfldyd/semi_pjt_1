const a = document.querySelector('#a')

a.addEventListener('click', function(event) {
    event.preventDefault();
    
    axios({
        method: 'get',
        url: `/${event.target.dataset.commentId}/reply/`,
    })
    .then(response => {
      const commentDiv = document.querySelector('#comment-div')
      removeAllchild(commentDiv)
      function removeAllchild(div) {
        while (div.hasChildNodes()) {
          div.removeChild(div.firstChild);
        }
      }

      const resdata = response.data.content    

      for (let i = 0; i < resdata.length; i++) {
        const p = document.createElement('p')
        p.innerText = `${resdata[i][0]} | ${resdata[i][1]}`
        const hr = document.createElement('hr')
        commentDiv.appendChild(p)
        commentDiv.appendChild(hr)
      }
    })
})

const a_close = document.querySelector('#a_close')

a_close.addEventListener('click', function(event) {
    event.preventDefault();
    
    axios({
        method: 'get',
        url: `/${event.target.dataset.commentId}/reply/`,
    })
    .then(response => {
      const commentDiv = document.querySelector('#comment-div')
      removeAllchild(commentDiv)
      function removeAllchild(div) {
        while (div.hasChildNodes()) {
          div.removeChild(div.firstChild);
        }
      }
    })
})