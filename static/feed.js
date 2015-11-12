var value = 'first';
console.log("yo");
$(window).scroll(function() {
    console.log(value);
    console.log(($(window).scrollTop()));
    console.log($(document).height() - $(window).height());
    if (($(window).scrollTop() == $(document).height() - $(window).height()) && (value != "END"))  {
        // ajax call get data from server and append to the div
        console.log("hello")
        $.ajax({
            url: '/feedData',
	    type: 'POST',
	    data: {"oldest": value},
	    dataType: 'json',
            success: function(response) {
                console.log(response);
		
		$("body").append(response.posts);
		// console.log(response.posts.);
		// for (i=0; i < response.posts.length; i++)
		// {
		//     for (j=0; j < response.posts[i].length; j++)
		//     {
		// 	$(".main-container").after(response.posts[i][j]);
		// 	$(".main-container").after("<br/>");
		//     }
		// }
		
		value = response.oldest_pub_date;
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});
