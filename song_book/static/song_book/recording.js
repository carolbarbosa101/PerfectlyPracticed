URL = window.URL || window.webkitURL;
var gumStream;
var rec;
var input;

let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext = new AudioContext;
var constraints = { audio: {
    volume: 1.0,
}, video:false }

function startRecording(elem){
    $(elem).attr('disabled', true)
    $(elem).siblings('.stop_button').attr('disabled', false)
    $(elem).siblings('.pause_button').attr('disabled', false)

    
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
    var user_pk = $(elem).parent().attr('user_pk')
    var song_pk = $(elem).parent().attr('song_pk')
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
    
    var li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-center align-items-center temp'
    
    li.innerHTML = 'Preview:'
    li.appendChild(au);
    li.appendChild(saveBtn);
    li.appendChild(discardBtn);
    $(elem).parents('.row.justify-content-center.align-items-center.controls').nextAll('.col-md-12.recordings').find('.list-group.temp_list').prepend(li);

    $(saveBtn).click(function() {
        // send blob to Django view.py
        sendBlobToView(blob, user_pk, song_pk);
        window.location.reload()
    });
    
    $(discardBtn).click(function(){
        $(li).remove();
        $(elem).siblings('.record_button').attr('disabled', false)
    });
}

function sendBlobToView(blob, user_pk, song_pk){
    let formData = new FormData();

    // have a pre-selected actual file name and user-selected display name for security
    var dt = new Date().toLocaleString().replace(', ','_').replaceAll('/','-').replaceAll(':', '-');
    var filename = `${dt}.wav`
    var display_name=prompt('Pick a name for your recording:', dt);
    if(!display_name) display_name = dt;

    formData.append('file', blob, filename)
    formData.append('display_name', display_name)
	fetch(`/song_book/${user_pk}/song_recording/${song_pk}/`, {
		headers: {"X-CSRFToken": csrftoken},
		method: 'post',
		body: formData,
	});

    console.log('sucessssss')
}

