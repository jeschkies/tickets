var stripe_handler = StripeCheckout.configure({
    key: "pk_test_0sXroqacYK4vsFNDUOJV40Eq", // TODO: Do not hardcode
    name: "Ticketfarm",
    image: "https://stripe.com/img/documentation/checkout/marketplace.png",
    locale: "auto",
    zipCode: true,
    currency: "eur",
    token: function(token) {
        alert('Toke is ' + token)
    }
})

var app = new Vue({
  el: '#ticket_count',
  data: {
    number_tickets: ''
  }
})

var b_vm = new Vue({
  el: '#charge_button',
  data: {},
  methods: {
    charge: function(event) {
        stripe_handler.open({amount: 2500 * app.number_tickets})
    }
  }
})
