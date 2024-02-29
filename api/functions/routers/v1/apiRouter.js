const rateRouter = require('./rateRouter')

const apiRouter = require('express').Router()

apiRouter.use('/rates', rateRouter)

module.exports = apiRouter