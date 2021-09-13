var express = require('express');
const signs = require('../signs')

var router = express.Router();

/* GET signs listing. */
router.get('/', (req, res, next) => {
  res.send('respond with a resource');
});

router.get('/:sign', (req, res, next) => {
  const sign = getSign(req.params.sign);
  
  // 1. Verificar que sea una senal valida.

  // 2. Buscar senal en la base por coordenadas. (opcional por ahora)

    // 2a. Si existe, devuelvo.
  
    // 2b. Si no existe, la guardo.

  // 3. 

  if (sign.sign != null) res.send(`Received ${sign.sign}`);
})

const getSign = sign => {
  //TODO
}

module.exports = router;
