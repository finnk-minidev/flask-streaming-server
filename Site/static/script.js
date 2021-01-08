let preview = document.getElementById("preview");
let recording = document.getElementById("recording");
let startButton = document.getElementById("startStream");
let stopButton = document.getElementById("stopbutton");
let downloadButton = document.getElementById("downloadButton");
let uid = document.getElementById("jinjaInput").getAttribute("streamUID");
let record = false;


let recordingTimeMS = 5000;

function wait(delayInMS){
	return new Promise(resolve => setTimeout(resolve, delayInMS));
}

function startRecording(stream, lengthInMS){
	let recorder = new MediaRecorder(stream);
	let data = [];
	
	recorder.ondataavailable = event => data.push(event.data);
	recorder.start();
	
	let stopped = new Promise((resolve, reject) => {
		recorder.onstop = resolve;
		recorder.onerror = event => reject(event.name);
	});
	
	let recorded = wait(lengthInMS).then(
		() => recorder.state == "recording" && recorder.stop()
		);
	return Promise.all([stopped, recorded]).then(() => data);
}

function stop(stream){
	stream.getTracks().forEach(track => track.stop());
}

function streamToServer(){
	navigator.mediaDevices.getUserMedia({
		video: {
			facingMode: {
     			exact: 'environment'
    		}
    	},
		audio: true
	}).then(stream => 
		preview.srcObject = stream;
		preview.captureStream = preview.captureStream || preview.mozCaptureStream;
	);
	while(record){
		new Promise(resolve => preview.onplaying = resolve)
		.then(() => startRecording(preview.captureStream(), recordingTimeMS))
		.then(recordedChunks => {
			sendToServer(recordedChunks);
		}, false);
	}
		
		recording = startRecording(preview.captureStream(), recordingTimeMS);
		setTimeout(sendToServer, 0, recording);		
}

function sendToServer(data){
	blob = new Blob(data, {type: "video/webm" });
	request = new XMLHttpRequest();
	fd = new FormData();
	fd.append("video",data);
	request.open("POST", "https://192.168.42.235:5000/show/receive/"+uid, true)
	request.onload = function(event){};
	request.send(blob);
}

startButton.addEventListener("click", function() {
	record = true;
	streamToServer();

//	navigator.mediaDevices.getUserMedia({
//		video: {
//			facingMode: {
//     			exact: 'environment'
//    		}
//    	},
//		audio: true
//	}).then(stream => {
//		preview.srcObject = stream;
//		downloadButton.href = stream;
//		preview.captureStream = preview.captureStream || preview.mozCaptureStream;
//		return new Promise(resolve => preview.onplaying = resolve);
//	}).then(() => startRecording(preview.captureStream(), recordingTimeMS))
//	.then(recordedChunks => {
//		sendToServer(recordedChunks);
//		let recordedBlob = new Blob(recordedChunks, {type: "video/webm" });
//		recording.src = URL.createObjectURL(recordedBlob);
//		downloadButton.href = recording.src;
//		downloadButton.download = "RecordedVideo.webm";
//		}, false);
});

stopButton.addEventListener("click", function() {
 	record = false;
	stop(preview.srcObject);
}, false);