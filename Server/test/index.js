$(function (){
	console.log("ready");

	$.ajax({
		url: "./test.py",
		type: "POST",
		data: {},
		dataType: "JSON",
		success: function(data){
			console.log('success');
			console.log(data)
		}
	})	
})
