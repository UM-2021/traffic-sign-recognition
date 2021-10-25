const { Schema, model } = require('mongoose');

const signLocationSchema = new Schema({
  sign: {
    type: Schema.Types.ObjectId,
    ref: 'Sign'
  },
  location: {
    type: {
      type: String,
      default: 'Point',
      enum: ['Point'],
    },
    coordinates: {
      type: [Number],
      required: [true, 'A sign record must have a location.'],
      validate: {
        validator: (val) => Array.isArray(val) && val.length === 2,
        message: 'A sign record must have a valid location.',
      },
    },
  },
  count: {
    type: Number,
    default: 1,
  },
});

module.exports = model('SignLocation', signLocationSchema);
