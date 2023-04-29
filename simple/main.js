'use strict';

const constraints = window.constraints = {
  audio: false,
  video: true
};

const stream = {content: null};
const toggle_button = {button: null};

function handleSuccess(stream) {
  const video = document.querySelector('video');
  const videoTracks = stream.getVideoTracks();
  console.log('Got stream with constraints:', constraints);
  console.log(`Using video device: ${videoTracks[0].label}`);
  window.stream = stream; // make variable available to browser console
  video.srcObject = stream;
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

document.querySelector('#showVideo').addEventListener('click', e => init(e));