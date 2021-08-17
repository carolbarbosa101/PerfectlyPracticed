let audioContext = new AudioContext;
let scheduleAheadTime = 0.1;
let lookahead = 0.25;
let nextNoteTime = 0;
var bpm = $('#bpm_input').val();


function playOsc(time){
  // input node oscillator
  let osc = audioContext.createOscillator();
  osc.frequency.value = 800;

  // add a gain node
  let theGain = audioContext.createGain();
  theGain.gain.exponentialRampToValueAtTime(1, time + 0.001);
  theGain.gain.exponentialRampToValueAtTime(0.001, time + 0.02);

  // start playing note at calculated nextNoteTime
  osc.start(time);
  osc.stop(time + 0.01);
  
  playAnimation(time);
  
  // need to connect audio graph by connecting input nodes with output
  osc.connect(theGain).connect(audioContext.destination);

}

function playAnimation(time){

  // mitigate animation lag by adjusting fade time at higher bpm
  var fadeTime;
  if(bpm < 120){
    fadeTime = 200
  }else{
    fadeTime = 100
  }
  
  timeLeft = (time - audioContext.currentTime) * 1000
  setTimeout(() => {
    $('#circle_2').fadeTo(fadeTime, 0.5, function() { $(this).fadeTo(fadeTime, 1.0); });
    console.log('beat')
    }, timeLeft);
}

function nextNote(){
  // $('#beat_sound')[0].play();
  bpm = $('#bpm_input').val();
  var interval = 60/bpm;
  nextNoteTime += interval;
  
}

function scheduleNote(time){
  // audioContext.resume();
  playOsc(time);
}


function scheduler(){
  while (nextNoteTime < audioContext.currentTime + scheduleAheadTime ) {
    scheduleNote(nextNoteTime);
    nextNote();
  }
}

function startSound(){

  nextNoteTime = audioContext.currentTime;

    metroInterval = setInterval(() => {
      scheduler();
      }, lookahead);
    
    return metroInterval;
}
