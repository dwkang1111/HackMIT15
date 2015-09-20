var $ = require('jQuery');
$.ajax({
  url: "http://127.0.0.1:3030/data",
  method: "GET",
  data: {'id': '-Jzd0-9MrcDnXBiJOS0a'},
  success: function(result) {
    console.log(result);
  },
});
