const { Schema, model } = require('mongoose');

const signSchema = new Schema({
  sign: {
    type: Number,
    unique: [true, 'There is already a sign with that identifier.'],
    required: [true, 'A sign must have an identifier.'],
  },
  name: {
    type: String,
    required: [true, 'A sign must have a name.']
  },
  photo: {
    type: String,
    required: [true, 'A sign must have a photo path.']
  },
  audio: {
    type: String,
    required: [true, 'A sign must have a audio path.']
  }
});

module.exports = model('Sign', signSchema);
