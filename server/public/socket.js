let HOST = location.origin.replace(/^http/, 'ws')
let ws = new WebSocket(HOST);
let img;
let signName;

ws.onmessage = (event) => {
  const data = event.data;
  img = document.getElementById('image');
  signName = document.getElementById('signName');
  img.src = data.img;
  signName.innerHTML = data.name;
}