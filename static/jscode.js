var mousePressed = false;
var lastX, lastY;
var ctx;

function InitThis() {
    ctx = document.getElementById('myCanvas').getContext("2d");

    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    $('#myCanvas').mouseup(function (e) {
        mousePressed = false;
    });
	
    $('#myCanvas').mouseleave(function (e) {
        mousePressed = false;
    });

}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = $('#selColor').val();
        ctx.lineWidth = $('#selWidth').val();
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}
	
function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    console.log('cleared')
    $('#pred').val('')
}

function SaveImg() {
    // Use the identity matrix while clearing the canvas
    var scratchCanvas = document.getElementById('myCanvas');
    var context = scratchCanvas.getContext('2d');
    var dataURL = scratchCanvas.toDataURL();
    //console.log(dataURL)
    
    $.ajax({
          type: "POST",
          url: "http://127.0.0.1:5000/imgrec",
          data:{
            imageBase64: dataURL
          }
        }).done(function(resp) {
          console.log(resp);
          $('#pred').val(resp['pred']);
        });
}