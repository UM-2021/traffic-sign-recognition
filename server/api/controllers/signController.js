const catchAsync = require('../utils/catchAsync');
const APIFeatures = require('../utils/apiFeatures');
const AppError = require('../utils/appError');
const Sign = require('../models/signModel');
const SignLocation = require('../models/signLocationModel');
const SignRecord = require('../models/signRecordModel');

exports.createSign = catchAsync(async (req, res, next) => {
  const newSign = await Sign.create(req.body);

  res.status(201).json({
    status: 'success',
    data: {
      data: newSign,
    },
  });
});

exports.createSignLocation = catchAsync(async (req, res, next) => {
  const sign = req.body;

  // Verificar request body
  if (!('sign' in sign) || !('coordinates' in sign))
    return next(new AppError('Not a valid request body.', 400));

  // Verificar si la señal es valida.
  const rawSign = await Sign.findOne({ sign: Number(sign.sign) });
  if (!rawSign) return next(new AppError('Not a valid sign.', 404));

  // Crear o sumar al contador de una ubicacion.
  const EARTH_RADIUS_KM = 6378.1;
  const distance = 0.2; // 20 m

  const lng = sign.coordinates[0];
  const lat = sign.coordinates[1];

  const radius = distance / EARTH_RADIUS_KM;
  let nearSigns = await SignLocation.find({
    location: { $geoWithin: { $centerSphere: [[lng, lat], radius] } },
  }).populate({
    path: 'sign',
    match: { sign: Number(sign.sign) },
  });

  nearSigns = nearSigns.filter((loc) => loc.sign != null);

  let signLocation = null;
  if (nearSigns.length > 0) {
    const nSign = nearSigns[0];
    signLocation = await SignLocation.findOneAndUpdate(
      { _id: nSign._id },
      { count: nSign.count + 1 },
      { new: true }
    ).populate('sign', '-_id');
  } else {
    const newSignLocation = {
      sign: rawSign._id,
      location: {
        coordinates: sign.coordinates,
      },
    };

    signLocation = await SignLocation.create(newSignLocation);
    signLocation = await signLocation.populate('sign', '-_id');
  }

  // Crear SignRecord
  if (signLocation) await SignRecord.create({ signLocation: signLocation._id });

  res.status(201).json({
    status: 'success',
    data: {
      data: signLocation,
    },
  });
});

exports.getSigns = catchAsync(async (req, res, next) => {
  const features = new APIFeatures(Sign.find(), req.query).filter().sort().limit().paginate();
  // const signs = await features.query.explain();
  const signs = await features.query;

  res.status(200).json({
    status: 'success',
    results: signs.length,
    data: {
      data: signs,
    },
  });
});

exports.getSignsLocation = catchAsync(async (req, res, next) => {
  let features = new APIFeatures(SignLocation.find(), req.query).filter().sort().limit().paginate();
  // const signs = await features.query.explain();
  features.query = features.query.populate('sign', '-_id');
  const signs = await features.query;

  res.status(200).json({
    status: 'success',
    results: signs.length,
    data: {
      data: signs,
    },
  });
});

exports.getSignsRecords = catchAsync(async (req, res, next) => {
  let features = new APIFeatures(SignRecord.find(), req.query).filter().sort().limit().paginate();
  // const signs = await features.query.explain();
  features.query = features.query.populate({
    path: 'signLocation',
    select: '-_id',
    populate: { path: 'sign', select: '-_id' },
  });
  const signs = await features.query;

  res.status(200).json({
    status: 'success',
    results: signs.length,
    data: {
      data: signs,
    },
  });
});

exports.getSign = catchAsync(async (req, res, next) => {
  const sign = await Sign.findById(req.params.id);

  if (!sign) return next(new AppError('No sign found with that ID', 404));

  res.status(200).json({
    status: 'success',
    data: {
      data: sign,
    },
  });
});

exports.getSignsCountByType = catchAsync(async (req, res, next) => {
  const signs = await SignRecord.aggregate([
    {
      $lookup: {
        from: 'signlocations',
        localField: 'signLocation',
        foreignField: '_id',
        as: 'sign',
      },
    },
    {
      $unwind: {
        path: '$sign',
        preserveNullAndEmptyArrays: true,
      },
    },
    {
      $lookup: {
        from: 'signs',
        localField: 'sign.sign',
        foreignField: '_id',
        as: 'sign.type',
      },
    },
    {
      $group: {
        _id: '$sign.type.sign',
        count: { $sum: 1 },
        name: { $first: '$sign.type.name' },
        photo: { $first: '$sign.type.photo' },
      },
    },
    {
      $project: {
        sign: { $arrayElemAt: ['$_id', 0] },
        name: { $arrayElemAt: ['$name', 0] },
        photo: { $arrayElemAt: ['$photo', 0] },
        count: 1,
        _id: 0,
      },
    },
  ]);

  res.status(200).json({
    status: 'success',
    data: {
      data: signs,
    },
  });
});

exports.getSignsCountByDate = catchAsync(async (req, res, next) => {
  const signs = await SignRecord.aggregate([
    {
      $match: {
        identifiedAt: {
          $gte: new Date(new Date().getTime() - 10 * 24 * 60 * 60 * 1000),
        },
      },
    },
    {
      $group: {
        _id: { $dateToString: { format: '%Y-%m-%d', date: '$identifiedAt' } },
        count: { $sum: 1 },
      },
    },
    {
      $project: {
        _id: 0,
        date: '$_id',
        count: 1,
      },
    },
  ]);

  res.status(200).json({
    status: 'success',
    data: {
      data: signs,
    },
  });
});
