const buildResponseFromRates = (rateArray) => {
    const response = {}
    rateArray.forEach((rate) => {
        const { from_currency, to_currency } = rate
        if (!response[from_currency]) {
            response[from_currency] = {}
        } 
        response[from_currency][to_currency] = rate
    })
    return response
}

module.exports = { buildResponseFromRates }