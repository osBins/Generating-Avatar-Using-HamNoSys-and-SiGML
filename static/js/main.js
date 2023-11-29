document.getElementById('play-button').addEventListener('click', function() {
    document.getElementById('uploaded-video').play();
    document.getElementById('cwasa-frame').contentWindow.document.getElementById('harshitbtn').click();
});

document.getElementById('stop-button').addEventListener('click', function() {
    var video = document.getElementById('uploaded-video');
    video.pause(); 
    video.currentTime = 0; 

    // clicking a button inside an iframe as in the play-button handler
    document.getElementById('cwasa-frame').contentWindow.document.getElementById('yourStopButtonId').click();
});
