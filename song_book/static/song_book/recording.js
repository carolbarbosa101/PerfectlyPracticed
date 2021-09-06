URL = window.URL || window.webkitURL;
var gumStream;
var rec;
var input;

let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext = new AudioContext;
var constraints = { audio: {
    volume: 1.0,
}, video:false }

var user_pk;
var song_pk;

function startRecording(elem){
    $(elem).attr('disabled', true)
    $(elem).siblings('.stop_button').attr('disabled', false)
    $(elem).siblings('.pause_button').attr('disabled', false)

    // get user mic input    
    navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
        audioContext.resume()
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        
        // 1 channel = mono sound
        rec = new Recorder(input, {
            numChannels: 1
        }) 
        
        rec.record()
        console.log('recording')
        
    }).catch(function(err) {
        audioContext.suspend()
        //enable the record button and disable others if getUserMedia() fails 
        $(elem).attr('disabled', false)
        $(elem).siblings('.stop_button').attr('disabled', true)
        $(elem).siblings('.pause_button').attr('disabled', true)
    });
}

function pauseRecording(elem){
    if (rec.recording) {
        rec.stop();
        $(elem).html('Resume')
        console.log('paused')
    } else {
        rec.record()
        $(elem).html('Pause')
    }
}

function stopRecording(elem){
    $(elem).attr('disabled', true)
    $(elem).siblings('.record_button').attr('disabled', true)
    $(elem).siblings('.pause_button').attr('disabled', true)
    
    // incase stopped while paused
    $(elem).siblings('.pause_button').html('Pause')
    
    rec.stop()
    gumStream.getAudioTracks()[0].stop()
    audioContext.suspend()
    console.log('stopped')
    
    // convert recorded data to blob and process
    rec.exportWAV(function(blob){
        
        // add to preview list temporarily so user can playback straight away 
        // user can choose to keep the recording and save to DB or discard
        saveOrDiscard(elem, blob);
        
    })
}

function saveOrDiscard(elem, blob){
    user_pk = $(elem).parent().attr('user_pk')
    song_pk = $(elem).parent().attr('song_pk')
    var blob_url = URL.createObjectURL(blob);
    
    var au = document.createElement('audio');
    au.controls = true;
    au.src = blob_url;
    au.className = 'preview-audio'
    
    var saveBtn = document.createElement('button');
    saveBtn.innerHTML = 'Save';
    saveBtn.className = 'btn btn-success save';

    var discardBtn = document.createElement('button');
    discardBtn.innerHTML = 'Discard';
    discardBtn.className = 'btn btn-danger discard';

    var loading = document.createElement('span');
    loading.className = 'loading';

    
    var li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-center align-items-center temp'
    
    li.innerHTML = 'Preview:'
    li.appendChild(au);
    li.appendChild(saveBtn);
    li.appendChild(discardBtn);
    li.appendChild(loading);
    $(elem).parents('.row.justify-content-center.align-items-center.controls').nextAll('.col-md-12.recordings').find('.list-group.temp_list').prepend(li);

    $(saveBtn).click(function() {
        // send blob to Django view.py
        //sendBlobToView(blob, user_pk, song_pk);
        getSignedRequest(blob, user_pk, song_pk)
    });
    
    $(discardBtn).click(function(){
        $(li).remove();
        $(elem).siblings('.record_button').attr('disabled', false)
    });
}

// first a get request is sent to sign off with the AWS details in Django
function getSignedRequest(file){
    let formData = new FormData();
    // have a pre-selected actual file name and user-selected display name for security
    var dt = new Date().toLocaleString().replace(', ','_').replaceAll('/','-').replaceAll(':', '-');
    var file_name = `${dt}.wav`
    display_name=prompt('Pick a name for your recording:', dt);

    // display_name == null if user cancels in prompt
    if(display_name !== null){
        if(display_name ==='') display_name = dt;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", `/song_book/song_recording/sign_s3/${file_name}/`);

        xhr.onreadystatechange = function(){
          if(xhr.readyState === 4){
            if(xhr.status === 200){
            // if the sign off is successful, we take the response data with the AWS details and the blob file, and upload
              var response = JSON.parse(xhr.responseText);
              uploadFile(file, response.data, response.url, display_name);
              $('.loading').html('<img src= /static/song_book/loading_spinner.svg/>')
            }
            else{
              alert("Could not get signed URL.");
            }
          }
        };
        xhr.send();
    }

  }

  function uploadFile(file, s3Data, url, display_name){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data.url);
  
    var postData = new FormData();
    for(key in s3Data.fields){
      postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);
  
    xhr.onreadystatechange = function() {
      if(xhr.readyState === 4){
        if(xhr.status === 200 || xhr.status === 204){
            // if the upload to AWS is sucessful, we save the reference to the file in the DB with Django
            saveToDB(url, display_name)
        }
        else{
          alert("Could not upload file.");
        }
     }
    };
    xhr.send(postData);
  }

  function saveToDB(url, display_name){
    var postData = new FormData();
    postData.append('url', url)
    postData.append('display_name', display_name)

    fetch(`/song_book/${user_pk}/song_recording/${song_pk}/`, {
        headers: {"X-CSRFToken": csrftoken},
        method: 'post',
        body: postData,
    });
    window.location.reload()
  }

