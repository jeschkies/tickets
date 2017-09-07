var stripe_handler = StripeCheckout.configure({
    key: stripe_publishable_key,
    name: "Ticketfarm",
    image: "https://stripe.com/img/documentation/checkout/marketplace.png",
    locale: "auto",
    zipCode: true,
    currency: "eur",
    token: function(token) {
        purchase_form_vm.submit(token.id, token.email)
    }
})

var purchase_form_vm = new Vue({
  el: '#purchase_form',
  data: purchase_data,
  computed: {
    total_amount: function() {
        var price = this.event_price * this.number_tickets
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
    },
    submit: function(token, email) {
        this.stripe_token = token
        this.email = email
        // Submit form after DOM has been updated.
        Vue.nextTick(function () {
            purchase_form_vm.$el.submit()
        })
    }
  }
})
