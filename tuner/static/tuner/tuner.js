const model_url =
'https://cdn.jsdelivr.net/gh/ml5js/ml5-data-and-models/models/pitch-detection/crepe/';
let pitch;
let mic;
let freq;
// lightslider carousel settings
var slider = $('#light_slider').lightSlider({
  item: 5,
  loop: true,
  slideMargin: 0,
  controls: false,
  pager: false,
  enableTouch: false,
  enableDrag: false,
  onSliderLoad: function() {
    $('#light_slider').removeClass('cS-hidden');
  } 
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
      freq = frequency;
      pitch.getPitch(gotPitch);
      showNote();
    }
}

// change DOM to display the likely guitar note
// update every 10 ms
function showNote(){
    interval = setInterval(() => {
      higherOrLower();
    }, 10);
}

// when string is plucked in a range of +/- 0.6 near a note, 
// we identify the note and go to its respective carousel slide
function higherOrLower(){
    for(var noteFreq in notes){
      var absDiff = Math.abs(freq - noteFreq);
      // perfectly tuned
      if(absDiff <= 0.6){
          var note = notes[noteFreq];
          var noteSlide = noteSlides[note];
          slider.goToSlide(noteSlide - 1);
          $('#freq').html(noteFreq + ' Hz').css('color', '#3badad');
        }
    }
}

function startTuner(){
  // need user input to resume audioContext otherwise chrome doesn't like it
  listening();
  $('#start_button').replaceWith(
      "<button class='btn btn-danger' id='stop_button'>Stop</button>"
  );
  $('#stop_button').click(stopTuner)
}
function stopTuner(){
    window.location.reload()
}