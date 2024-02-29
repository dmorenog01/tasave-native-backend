const errorHandler = (err, req, res, next) => {
    return res.json({error: err.message}).status(500)
}

module.exports = { errorHandler }