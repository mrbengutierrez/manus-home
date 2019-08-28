var video = document.querySelector("#videoElement");

//var overlay = documetn.getElementbyID("videoElement");
//overlay.style.visibility == "visible";
//window.scrollTo(0,0);

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}
