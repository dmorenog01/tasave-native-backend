const express = require("express");
const middleware = require("./middleware")
require('express-async-errors')
const apiRouterv1 = require("./routers/v1/apiRouter")

const app = express();

app.use('/v1', apiRouterv1)
app.use(middleware.errorHandler)

module.exports = app