const express = require('express');
const socket = require('socket.io');
const signs = require('./signs')
const app = express();
const server = app.listen(3000, () => {
	console.log('Server Started..');
});

app.use(express.static('public'));

const io = socket(server);

io.on('connection', socket => {
	console.log('socket connected..', socket.id);

  socket.on('newSign', data => {
    const sign = signs.filter(s => s.sign === Number(data))[0];
		io.sockets.emit('sign', sign);
	});
});

app.post('/:sign', (req, res, next) => {
	const signNbr = req.params.sign;

	const sign = signs.filter(s => s.sign === Number(signNbr))[0];

  io.sockets.emit('sign', sign)

  res.end();
});