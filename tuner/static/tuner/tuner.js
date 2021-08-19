const model_url =
'https://cdn.jsdelivr.net/gh/ml5js/ml5-data-and-models/models/pitch-detection/crepe/';
let pitch;
let mic;
let freq;
let notes = {82.41:'E2', 110:'A2', 146.8:'D3', 196:'G3', 246.9:'B3', 329.6:'E4'}

// need user input to resume audioContext otherwise chrome doesn't like it
$(function() {
    $('#start_tuner').click(listening)
  });  


// create mic audio input with p5.js
function setup() {
  createCanvas(windowWidth, windowHeight);
  mic = new p5.AudioIn();
  audioContext = getAudioContext();
  mic.start();
}

// load in the crepe model
function listening() {
    console.log('listening');
    getAudioContext().resume()
    pitch = ml5.pitchDetection(model_url, audioContext, mic.stream, modelLoaded);
}

function modelLoaded() {
    console.log('model loaded');
    pitch.getPitch(gotPitch);
}

// after model loading, get the sound and frequency continously
function gotPitch(err, frequency) {
    if (err) {
      console.error(err);
    } else {
      console.log(frequency);
      freq = frequency;
      pitch.getPitch(gotPitch);
      showNote();
    }
}

// change DOM to display the likely guitar note
// update every 0.25s
function showNote(){
    interval = setInterval(() => {
      higherOrLower();
    }, 250);
}

// when string is plucked in a range of +/- 10 near a note, 
// tell the user the note you are close to and whether you are higher or lower than it
function higherOrLower(){
    for(var noteFreq in notes){
      var absDiff = Math.abs(freq - noteFreq)
      var signedDiff = freq - noteFreq
      if(absDiff <= 10){
        if(absDiff <= 1){
          $('#note_playing').html(notes[noteFreq]).css('color', 'green');
          $('#higher_lower').html('Perfect!').css('color', 'green');
        }else{
          if(Math.sign(signedDiff) === -1){
            $('#note_playing').html(notes[noteFreq]).css('color', 'blue');
            $('#higher_lower').html('Too Low').css('color', 'blue');
          }else if(Math.sign(signedDiff) === 1){
            $('#note_playing').html(notes[noteFreq]).css('color', 'red');
            $('#higher_lower').html('Too High').css('color', 'red');
          }
      }
    }
  }
}