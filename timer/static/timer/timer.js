// window.Musicsite = {}; 
// window.Musicsite.initialize = function () {
//     console.log('initialize called');
//     // input some tasks
//     $('Starman chords').attr({ type: 'text', name: 'task_input' }).appendTo('#task_form').focus();
//     $('15').attr({ type: 'number', name: 'time_input' }).appendTo('#task_form').focus();
//     $('#add_button').click()
//     export {totalTime};
//   };

let timeString = JSON.parse(document.getElementById('time_list').textContent);
let timeList = timeString.substring(1, (timeString.length - 1)).split(', ');

let colourString = JSON.parse(document.getElementById('colour_list').textContent);
colourString = colourString.replace(/["]/g, "");
let colourList = colourString.substring(1, (colourString.length - 1)).split(', ');

let timePassed = 0;
let totalTime = calculateTotalTime();
let timeLeft = totalTime;
let timerInterval = null;
const RADIUS = 300;
const CIRCUMFERENCE = 2*Math.PI*RADIUS;

function calculateTotalTime(){
  // for initial time label with no tasks, set 0
  if(timeString === '[]'){
    console.log('test')
    return 0;
  }
  var total = 0;
  for(let i = 0; i < timeList.length; i++){
    total += parseInt(timeList[i]);
  }
  return total * 60;
}

function calculateOffsets(){
  var offsets = [];
  var circleFractions = [];
  var offset;
  var prevOffset = 0;

  for(let i = 0; i < timeList.length; i++){
    // get fractions of circle of each task time
    circleFractions.push((timeList[i]/(totalTime/60)) * CIRCUMFERENCE);
  }

  for(let i = 0; i < timeList.length; i++){
    // build dasharray offset list by taking away circle fraction of previous fraction 
    if(i == 0){
      offsets.push(0);
    }else{
      offset = prevOffset - circleFractions[i-1];
      offsets.push(offset);
      prevOffset = offset;
    }
  }
  return offsets;
}

function generateCircles(){
  var offsets = calculateOffsets();
  var circlesList = [];
  circlesList.push(
    `<circle id="circle_base" class="timer_circle" cx="440" cy="320" r="300" 
    transform="rotate(-90, 440, 320)" stroke="grey" stroke-dasharray="1885"/>`
      )
  for(let i = 0; i < offsets.length; i++){
    circlesList.push(
    `<circle id="circle_${i}" class="timer_circle" cx="440" cy="320" r="300" 
     transform="rotate(-90, 440, 320)" stroke="${colourList[i]}CC" stroke-dasharray="1885" stroke-dashoffset="${offsets[i]}"/>`
      )
  }
  circlesList.push(
    `<circle id="circle_top" class="timer_circle" cx="440" cy="320" r="300"/>
    <path
        id="circle_top_path"
        class="timer_circle"
        stroke="grey" 
        stroke-dasharray="1885" 
        stroke-dashoffset="-1885" 
        d="
        M -180, 60
        m -300, 0
        a 300,300 0 1,0 600,0
        a 300,300 0 1,0 -600,0
        "
    ></path>`
      )

var circlesHTML = circlesList.join("\n");

  $('.timer_group').html(
    circlesHTML
  )
}

function animateCircle(){
  var fraction = timeLeft / totalTime;
  fraction = fraction - (1/totalTime) * (1 - fraction);
  offset = fraction * CIRCUMFERENCE;

  $('#circle_top_path').attr('stroke-dashoffset', `-${offset}`)
}

function formatTimeLeft(time) {   
  let minutes = Math.floor(time/60);
  
  let seconds = time % 60;
  
  if (seconds < 10) {
    seconds = `0${seconds}`;
  }
  if (minutes < 10) {
    minutes = `0${minutes}`;
  }
  
  return `${minutes}:${seconds}`;
}  

function startTimer(){
  // if no tasks entered then alert and don't start timer
  if(timeString === '[]'){
    alert("Please enter a task.")
    return
  }
  
  $('#start_sound').prop('muted', false);
  $('#start_sound')[0].play();

  // change to stop button upon click
  $('#timer_button').replaceWith(
    "<button class='btn btn-danger' id='timer_button'>Stop</button>"
    );
    $('#timer_button').off('click')
    $('#timer_button').click(stopTimer)
    
    timerInterval = setInterval(() => {
      timePassed += 1;
      timeLeft = totalTime - timePassed;
      if(timePassed == totalTime ){
        clearInterval(timerInterval);
        timesUp();
      }
      $('#timer_label').html(formatTimeLeft(timeLeft));
      animateCircle();
    }, 1000);

}


function stopTimer(){
  $('#timer_button').replaceWith(
    "<button class='btn btn-success' id='timer_button'>Start</button>"
    );
    $('#timer_button').off('click')
    clearInterval(timerInterval);
    $('#timer_button').click(startTimer)
  }
  
  function timesUp(){
    $('#end_sound').prop('muted', false);
    $('#end_sound')[0].play();
    $(".modal").modal();
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    $('#start_sound').prop('muted', true)
    $('#end_sound').prop('muted', true)
    $('#timer_label').html(formatTimeLeft(timeLeft));
    $('#timer_button').click(startTimer);
    generateCircles();
  }, false);
  
  
  