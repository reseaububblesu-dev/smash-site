// Netlify Function — Vérifier le statut d'un paiement
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  try {
    const { paymentIntentId } = JSON.parse(event.body);
    const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        status: paymentIntent.status,
        amount: paymentIntent.amount,
        succeeded: paymentIntent.status === 'succeeded'
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
