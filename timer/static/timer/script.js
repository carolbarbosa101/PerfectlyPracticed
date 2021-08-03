let total_time = JSON.parse(document.getElementById('total_time_id').textContent);
console.log(total_time);
let timePassed = 0;
let timeLeft = total_time * 60;
let timerInterval = null;


function formatTimeLeft(time) {   
  let minutes = Math.floor(time/60);
  
  let seconds = time % 60;
  
  if (seconds < 10) {
    seconds = `0${seconds}`;
  }
  
  return `${minutes}:${seconds}`;
}  

document.addEventListener('DOMContentLoaded', function() {
  $('#timer_label').html(formatTimeLeft(timeLeft));
  $('#timer_button').click(startTimer)
}, false);


function startTimer(){
  $('#timer_button').replaceWith(
    "<button class='btn btn-danger' id='timer_button'>Stop</button>"
    );
  $('#timer_button').off('click')
  $('#timer_button').click(stopTimer)

  timerInterval = setInterval(() => {
    timePassed += 1;
    timeLeft = (total_time * 60) - timePassed;
    if(timePassed == total_time * 60){
      clearInterval(timerInterval);
      alert("Time's Up!")
      location.reload();
    }
    $('#timer_label').html(formatTimeLeft(timeLeft));
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



  
  