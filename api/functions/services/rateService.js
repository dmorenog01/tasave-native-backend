const { getFirestore } = require('firebase-admin/firestore');

const db = getFirestore();

const getCurrencyPairs = async () => {
    const infoDoc = await db.collection('info').doc('api').get()
    const infoData = infoDoc.data()
    return infoData.pairs
}

const getLatestRate = async (rateName) => {
    const rateCollection = db.collection(rateName)
    const snapshot = await rateCollection.orderBy("rate_date", "desc").limit(1).get()
    if (snapshot.empty) {
        return null
    }
    const latestUpdate = snapshot.docs[0].data()
    return latestUpdate
}

const getLatestRates = async () => {
    const pairs = await getCurrencyPairs()
    const promises = pairs.map(rateName => getLatestRate(rateName))
    const results = await Promise.all(promises)
    return results
}

module.exports = { getLatestRates }