const express = require('express');
const { createServer } = require('http');
const WebSocket = require('ws');
const signs = require('./signs');
const app = express();
const server = createServer(app);

app.use(express.static('public'));

const wss = new WebSocket.Server({ server });

wss.broadcast = msg => {
	wss.clients.forEach(c => c.send(JSON.stringify(msg)));
}

wss.on('connection', ws => {
	console.log('ws connected..');
	ws.on('message', data => {
		const sign = signs.filter(s => s.sign === Number(data))[0];
		wss.broadcast(sign)
	});
});


// Only for testing.
// A sign can be send via HTTP to test the live change in the browser.
app.post('/:sign', (req, res, next) => {
	const signNbr = req.params.sign;

	const sign = signs.filter(s => s.sign === Number(signNbr))[0];

	wss.broadcast(sign);

	res.end();
});

server.listen(3000, function () {
	console.log('Server listening on port 3000...');
});
