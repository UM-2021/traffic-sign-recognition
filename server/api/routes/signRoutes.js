const express = require('express');
const router = express.Router();

const signController = require('../controllers/signController');

router.post('/', signController.createSign);
router.post('/locations', signController.createSignLocation);

router.get('/', signController.getSigns)
router.get('/locations', signController.getSignsLocation)
router.get('/records', signController.getSignsRecords)
router.get('/records/date', signController.getSignsCountByDate)
router.get('/type', signController.getSignsCountByType)
router.get('/:id', signController.getSign)

module.exports = router;
