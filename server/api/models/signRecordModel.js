const { Schema, model } = require('mongoose');

const signRecordSchema = new Schema({
  signLocation: {
    type: Schema.Types.ObjectId,
    ref: 'SignLocation',
  },
  identifiedAt: {
    type: Date,
    default: Date.now(),
  },
});

module.exports = model('SignRecord', signRecordSchema);
