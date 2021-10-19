const {Schema, model} = require('mongoose')

const signSchema = new Schema(
    {
        sign: {
            type: Number,
            required: true
        },
        name: {
            type: String,
            required: [true, 'A sign record must have a name.']
        },
        location: {
            type: {
                type: String,
                default: 'Point',
                enum: ['Point']
            },
            coordinates: [Number]
        }
    }
)

module.exports = model('Sign', signSchema);