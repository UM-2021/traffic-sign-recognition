const express = require('express');
const router = express.Router();

const signController = require('../controllers/signController');
const authController = require('../controllers/authController');

router.post('/', authController.protect, signController.createSign);
router.post('/locations', authController.protect, signController.createSignLocation);

router.get('/', authController.protect, signController.getSigns);
router.get('/locations', authController.protect, signController.getSignsLocation);
router.get('/records', authController.protect, signController.getSignsRecords);
router.get('/records/date', authController.protect, signController.getSignsCountByDate);
router.get('/type', authController.protect, signController.getSignsCountByType);
router.get('/:id', authController.protect, signController.getSign);

module.exports = router;
