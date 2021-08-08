// window.Musicsite = {}; 
// window.Musicsite.initialize = function () {
//     console.log('initialize called');
//     // input some tasks
//     $('Starman chords').attr({ type: 'text', name: 'task_input' }).appendTo('#task_form').focus();
//     $('15').attr({ type: 'number', name: 'time_input' }).appendTo('#task_form').focus();
//     $('#add_button').click()
//     export {totalTime};
//   };

let totalTime = JSON.parse(document.getElementById('total_time').textContent);

let timeString = JSON.parse(document.getElementById('time_list').textContent);
let timeList = timeString.substring(1, (timeString.length - 1)).split(', ');
console.log(timeList);

let colourString = JSON.parse(document.getElementById('colour_list').textContent);
colourString = colourString.replace(/["]/g, "");
let colourList = colourString.substring(1, (colourString.length - 1)).split(', ');
console.log(colourList);

let timePassed = 0;
let timeLeft = totalTime * 60;
let timerInterval = null;
const RADIUS = 300;
const CIRCUMFERENCE = 2*Math.PI*RADIUS;


function calculateOffsets(){
  var offsets = [];
  var circleFractions = [];
  var offset;
  var prevOffset = 0;

  for(let i = 0; i < timeList.length; i++){
    // get fractions of circle of each task time
    circleFractions.push((timeList[i]/totalTime) * CIRCUMFERENCE);
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

  console.log(offsets);
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

var circlesHTML = circlesList.join("\n");

console.log(circlesHTML);
  
  $('.timer_group').html(
    circlesHTML
  )
}

function formatTimeLeft(time) {   
  let minutes = Math.floor(time/60);
  
  let seconds = time % 60;
  
  if (seconds < 10) {
    seconds = `0${seconds}`;
  }
  
  return `${minutes}:${seconds}`;
}  

function startTimer(){
  $('#timer_button').replaceWith(
    "<button class='btn btn-danger' id='timer_button'>Stop</button>"
    );
    $('#timer_button').off('click')
    $('#timer_button').click(stopTimer)
    
    timerInterval = setInterval(() => {
      timePassed += 1;
      timeLeft = (totalTime * 60) - timePassed;
      if(timePassed == totalTime * 60){
        clearInterval(timerInterval);
        alert("Time's Up!")
        location.reload();
      }
    $('#timer_label').html(formatTimeLeft(timeLeft));

    generateCircles();

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
  
  
  document.addEventListener('DOMContentLoaded', function() {
    $('#timer_label').html(formatTimeLeft(timeLeft));
    $('#timer_button').click(startTimer);
    generateCircles();
  }, false);
  
  
  