(function () {
	let img = document.getElementById('image');
	let img2 = document.getElementById('image2');
	let signName = document.getElementById('signName');
	let signName2 = document.getElementById('signName2');
	let audio = document.getElementById('audio');
  	let ws = new WebSocket(`ws://${location.host}`);
	
	ws.onmessage = function (event) {
		const data = JSON.parse(event.data);		
		console.log('Afuera')
		if (img.src == window.location.href){  // Is equal to no image
			console.log('Primer IF')
			console.log(img.src)
			img.src = data.image;
			signName.innerHTML = data.name;
			audio.src = data.audio;
			console.log(img.src)
			img.style="opacity: 1;"
			setTimeout(async () => {
				if (img.src == window.location.href.slice(0, -1) + data.image){
					await fadeOut(img);
					removeElement(img, signName, audio);
				}
			}, 7000);
		} else if (img.src == window.location.href.slice(0, -1) + data.image) {  // The same image arrives
			
		} else if (img.src != window.location.href.slice(0, -1) + data.image) {  // Another image arrives
			img2.src = 	img.src;
			img.src = data.image;
			signName2.innerHTML = signName.innerHTML;
			signName.innerHTML = data.name;
			audio.src = data.audio;
			img.style="opacity: 1;"
			img2.style="opacity: 1;"
			setTimeout(async () => {
				await fadeOut(img2);
				await fadeOut(img);
				removeJustImageAndSignName(img2, signName2);
				removeJustImageAndSignName(img, signName);
				// img2.src = ''
				// img.src = ''
				// signName.innerHTML = '';
				// signName2.innerHTML = '';
				// removeElement(img, signName, audio)
				// removeElement(img2, signName2, audio)
			}, 7000);
		}
	
		function removeElement(img, signName, audio) {
			img.src = '';
			signName.innerHTML = '';
			audio.src = '';
			img.style="opacity: 0;"
		}
		
		function removeJustImageAndSignName(img, signName) {
			img.src = '';
			signName.innerHTML = '';
			img.style="opacity: 0;"
		}

		function fadeOut(ele) {
			return new Promise(function (resolve, reject) {
			let opacity = 1;
			function fade(){
			   if ((opacity -= .01) > 0){
				 ele.style.opacity = opacity;
				 requestAnimationFrame(fade);
			   } else {
				 resolve();
			   }
			}
		   fade();
		   });
		 };

	};
})();
