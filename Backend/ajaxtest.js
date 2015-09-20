var $ = require('jQuery');
$.ajax({
  url: "http://127.0.0.1:3030/data/",
  method: "GET",
  crossDomain: true,
  headers: {"Access-Control-Allow-Origin": "x-requested-with"},
  data: {'id': '-Jzd0-9MrcDnXBiJOS0'},
  success: function(result) {
    console.log(result);
  },
});
