(function () {
	let img = document.getElementById('image');
	let signName = document.getElementById('signName');
	let audio = document.getElementById('audio');
  let ws = new WebSocket(`ws://${location.host}`);
  
	ws.onmessage = function (event) {
		const data = JSON.parse(event.data);
		img.src = data.image;
		signName.innerHTML = data.name;
		audio.src = data.audio
	};
})();
