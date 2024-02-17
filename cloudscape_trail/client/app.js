
var pdf_url=""
// "https://probe-test-alpha.s3.ap-south-1.amazonaws.com/Intrigual_props.pdf"
var query= "Why do we sneeze?"
var system_prompt="Answer the query"
filename=""
BUCKET_NAME="probe-test-alpha"

text_form=document.getElementById('text_form')
answer_field=document.getElementById('answer')
get_history=document.getElementById('get_history')
history_div=document.getElementById('history')



document.getElementById('pdf_form').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if(!file)
    {
        alert("Please upload a file");
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);

    filename=file.name

    uploadbtn=document.getElementById('upload_button')
    uploadbtn.disabled=true
    uploadbtn.textContent="Uploading"

    fetch('https://j4j1ppnbec.execute-api.ap-south-1.amazonaws.com/default/geturl',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            "filename": file.name
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.presigned_url);
        uploadFileToS3(formData, data.presigned_url);
        })
});

async function uploadFileToS3(file, presignedUrl) {
    try {
      const response = await fetch(presignedUrl, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type,
        },
      });
  
      if (response.ok) {
        console.log('File uploaded successfully!');
        pdf_url=`https://${BUCKET_NAME}.s3.ap-south-1.amazonaws.com/${filename}`
      } else {
        throw new Error(`Upload failed with status ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error(error);
    }
    uploadbtn.disabled=false
    uploadbtn.textContent="Upload"
  }

get_history.addEventListener('click', function(event) {
    event.preventDefault();

    console.log("Fetching history...");

    fetch(`https://j4j1ppnbec.execute-api.ap-south-1.amazonaws.com/default/history`,{
        method: 'GET',
    }).then(response => response.json())
    .then(data => {
        console.log(data.message);
        update_history(data.history);
    })
});

text_form.addEventListener('submit', function(event) {
  event.preventDefault();

  const queryInput = document.getElementById('text_query');
  const query = queryInput.value;

  if (!query) {
    alert("Please enter some text");
    return;
  }

  body = JSON.stringify({
    "query": query,
    "pdf_url": pdf_url,
    "system_prompt": system_prompt,
  });

  console.log("querying...");

  // Disable the query button and set its text to "Querying"
  const queryButton = document.getElementById('query_button');
  queryButton.disabled = true;
  queryButton.textContent = "Querying";

  fetch(`https://j4j1ppnbec.execute-api.ap-south-1.amazonaws.com/default/query`,{
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
        },
      body: body,
  })
  .then(response => response.json())
  .then(data => {
      console.log(data);
      answer_field.textContent = data.answer;

      // Re-enable the query button and set its text back to "Query"
      queryButton.disabled = false;
      queryButton.textContent = "Query";
  });


});

function update_history(history){
    history=JSON.parse(history)
    history_div.innerHTML=""
    for (var i=0; i<history.length; i++){
        history_div.innerHTML+=`<p>Query: ${history[i].query}</p><p>Answer: ${history[i].answer}</p><p>${history[i].pdf_url}</p><br>`
    }
}

