function startSound(){
    var bpm = $('#bpm_input').val();
    // bpm = beats per minute
    // 1 minute = 60s = 60,000 ms
    // by dividing 60,000 by the bpm, we know how often (in ms) we want a beat to happen,
    // to reach that many beats in a minute
    // i.e a beat every x ms , where x = 60,000 / bpm
    // therefore x = interval (between each beat)

    var interval = 1000*60/bpm;

    metroInterval = setInterval(() => {
        $('#beat_sound')[0].play();
        $('#circle_2').fadeTo(200, 0.5, function() { $(this).fadeTo(200, 1.0); });
        console.log('beat')
      }, interval);
    
    return metroInterval;
}
