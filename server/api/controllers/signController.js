const catchAsync = require('../utils/catchAsync')

exports.createSign = catchAsync(async (req, res, next) => {

    const newDoc = await Sign.create(req.body);

    res.status(201).json({
        status: 'success',
        data: {
            data: newDoc
        }
    });
});