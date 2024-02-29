const rateRouter = require('express').Router()
const rateService = require('../../services/rateService')
const utils = require('../../utils')

rateRouter.get('/ping', (req, res) => {
    return res.json({message: 'pong!'}).status(200)
})

rateRouter.get('/', async (req, res) => {
    const updates = await rateService.getLatestRates()
    const response = utils.buildResponseFromRates(updates)
    return res.json(response).status(200)
})

module.exports = rateRouter