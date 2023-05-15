'use strict';

const constraints = window.constraints = {
  audio: false,
  video: true
};

const stream = {content: null};
const toggle_button = {button: null};

function handleSuccess(stream) {
  const video = document.querySelector('#video');
  const videoTracks = stream.getVideoTracks();
  console.log('Got stream with constraints:', constraints);
  console.log(`Using video device: ${videoTracks[0].label}`);
  window.stream = stream; // make variable available to browser console
  video.srcObject = stream;

  startCaptureInterval();
}

function handleError(error) {
  if (error.name === 'OverconstrainedError') {
    const v = constraints.video;
    errorMsg(`The resolution ${v.width.exact}x${v.height.exact} px is not supported by your device.`);
  } else if (error.name === 'NotAllowedError') {
    errorMsg('Permissions have not been granted to use your camera and ' +
      'microphone, you need to allow the page access to your devices in ' +
      'order for the demo to work.');
  }
  errorMsg(`getUserMedia error: ${error.name}`, error);
}

function errorMsg(msg, error) {
  const errorElement = document.querySelector('#errorMsg');
  errorElement.innerHTML += `<p>${msg}</p>`;
  if (typeof error !== 'undefined') {
    console.error(error);
  }
}

async function t_button(e) {
    if (toggle_button.button)
        toggle_button.button.target.disabled = false;

    e.target.disabled = true;
    toggle_button.button = e;
}

async function start(e) {
    try {
        stream.content = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream.content);
    } catch (e) {
        handleError(e);
    }
}

async function init(e) {
    if (stream.content) {
        stop(e)
        e.target.innerText = 'Open camera';
    } else {
        start(e)
        e.target.innerText = 'Stop';
    }
}

async function stop(e) {
    stream.content.getTracks().forEach(function(track) {
        track.stop();
    });

    stream.content = null;
}

function capture() {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const video_cv = document.querySelector("#video");
    context.canvas.width  = video_cv.videoWidth;
    context.canvas.height = video_cv.videoHeight;
    context.drawImage(video_cv, 0, 0);

    if (stream.content == null) {
        stopCaptureInterval();
        return;
    }

    if (document.getElementById('x1').checked)
        send();
}

function loadbase64image(data) {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    var image = new Image();

    image.onload = function() {
      context.drawImage(image, 0, 0);
    };

    image.src = "data:image/png;base64,"+data;
}

function loadtextfield(list_) {
    if (list_ && list_.length > 0) {
        var id = document.getElementById('id_');
        var name = document.getElementById('name_');

        id.value = list_[0][0]
        name.value = list_[0][1]
    }
}

function send() {
    stopCaptureInterval();
    const canvas = document.getElementById('canvas');
    let imagebase64data = canvas.toDataURL("image/png");
    imagebase64data = imagebase64data.replace('data:image/png;base64,', '');

    var url = '/rec'

    if (document.getElementById('x2').checked)
        url = '/reg';

    const fetchPromise = fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8'
      },
      body: JSON.stringify({
        image: imagebase64data,
        id: document.getElementById('id_').value,
        name: document.getElementById('name_').value
      })
    });

    fetchPromise.then(response => {
      return response.json();
    }).then(data => {
        startCaptureInterval();
        loadbase64image(data.data);
        loadtextfield(data.rec);
    });
}

var captureInterval;

function startCaptureInterval() {
  captureInterval = setInterval(capture, 1000);
}

function stopCaptureInterval() {
  clearInterval(captureInterval);
}

function toogleFeature(radioEl) {
    var selectedRadio = radioEl.getAttribute('id');
    var disableInputText = false;

    if (selectedRadio == "x1")
        disableInputText = true;

    var id = document.getElementById('id_');
    var name = document.getElementById('name_');
    var btn_capture = document.getElementById('btnCapture');

    if (disableInputText)
        btn_capture.style.display = "none";
    else
        btn_capture.style.display = "block";

    id.disabled = disableInputText;
    name.disabled = disableInputText;

    id.value = "";
    name.value = "";
}

document.querySelector('#showVideo').addEventListener('click', e => init(e));
document.querySelector('#btnCapture').addEventListener('click', e => send(e));