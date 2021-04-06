let top100 = ""
$.ajax({ type: 'GET', url: "out.txt", data: {}, //passing some input here
dataType: "text", success: function(response){ output = response; alert(output);} }).done(function(data){  alert(data); top100=data;});
console.log(top100);