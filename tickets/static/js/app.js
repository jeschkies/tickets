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

var ticket_count_vm = new Vue({
  el: '#ticket_count',
  data: {
    number_tickets: ''
  }
})

var charge_vm = new Vue({
  el: '#charge_button',
  data: {},
  computed: {
    total_amount: function() {
        var price = 2500 * ticket_count_vm.number_tickets
        return price
    },
    total_amount_readable: function() {
        var price = this.total_amount
        price /= 100
        return price.toLocaleString("de-DE", {style:"currency", currency:"EUR"})
    }
  },
  methods: {
    charge: function(event) {
        stripe_handler.open({amount: this.total_amount})
    }
  }
})
