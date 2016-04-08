
$(document).ready(function(){
	console.log("Hi there!")

	$(".button-collapse").sideNav();

	$(document).ready(function(){
    $('.parallax').parallax();
    });

///// Register /////
    $('#nav').on('click', ".register", function(event){
    	event.preventDefault();
        var template = $('#register-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#register_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "register",
        data: query_string,
    }).done(function(data, status){

		if (data.success){
			////// if they registered then display the Login ////////
                var template = $('#login-template').html();
		        var renderM = Mustache.render(template);
		        $('#answer_div').html(renderM);
		        $('#answer_div').append("<br><br>");
		        $('#answer_div').append(data.Message);
            }
        });
    });


///// Login /////
    $('#nav').on('click', ".login", function(event){
    	event.preventDefault();
        var template = $('#login-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#login_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "login",
        data: query_string,
    }).done(function(data, status){

        $('#answer_div').html(data.Message);
        $('#answer_div').append("<br><br>");
        $('#nav').append(data.username);

        });
    });

///// Logout /////
    $('#nav').on('click', ".logout", function(event){
    event.preventDefault();

    // var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "logout",
        // data: query_string,
    }).done(function(data, status){

    $('#answer_div').html(" <h2> Goodbye, See you soon!</h2>");
    $('#answer_div').append(data.Message);
	location.reload();

    });
});


///// Create Tweet /////
    $('#nav').on('click', ".tweet", function(event){
        event.preventDefault();
        var template = $('#create-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#create_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "create",
        data: query_string,
    }).done(function(data, status){

        var template = $('#profile-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });


////// Get All Tweets (timeline) /////
    $('#nav').on('click', ".timeline", function(event){
    event.preventDefault();

    // var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "timeline",
        // data: query_string,
    }).done(function(data, status){

        var template = $('#all-tweets').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });


////// Get Your Tweets (profile) /////
    $('#nav').on('click', ".profile", function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: $(this).attr("href"),
        data: query_string,
    }).done(function(data, status){

        var template = $('#profile-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });


///// Repost/////
    $('#answer_div').on('click', '#repost_button',function(event){
    event.preventDefault();

    if(confirm("Are you sure you would like to repost this tweet?")){
        var query_string = $(this).serialize() // returns all the data in your form
        var url = $(this).attr("href")

        $.ajax({
            method: "POST",
            url: url,
            data: query_string,
        }).done(function(data, status){

        var template = $('#profile-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    };
});


///// Vote Up/////
    $('#answer_div').on('click', '#up_button',function(event){
    event.preventDefault();

    if(confirm("Are you sure you want to like this?")){
        var query_string = $(this).serialize() // returns all the data in your form
        var url = $(this).attr("href")

        $.ajax({
            method: "POST",
            url: url,
            data: query_string,
        }).done(function(data, status){

            var template = $('#all-tweets').html();
            var renderM = Mustache.render(template,data);
            $('#answer_div').html(renderM);  
        });
    };
});


///// Vote Down/////
    $('#answer_div').on('click', '#down_button',function(event){
    event.preventDefault();

    if(confirm("Are you sure you want to unlike this?")){
        var query_string = $(this).serialize() // returns all the data in your form
        var url = $(this).attr("href")

        $.ajax({
            method: "POST",
            url: url,
            data: query_string,
        }).done(function(data, status){

            var template = $('#all-tweets').html();
            var renderM = Mustache.render(template,data);
            $('#answer_div').html(renderM);  
        });
    };
});


///// Delete Tweet/////
    $('#answer_div').on('click', '#delete_button',function(event){
    event.preventDefault();

    if(confirm("Are you sure you would like to delete this tweet?")){
        var query_string = $(this).serialize() // returns all the data in your form
        var url = $(this).attr("href")

        $.ajax({
            method: "POST",
            url: url,
            data: query_string,
        }).done(function(data, status){

        var template = $('#profile-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    };
});

///// Edit Event /////
    $('#answer_div').on('click', "#edit_button", function(event){ //on click
        event.preventDefault();

    $.ajax({
        method: "GET",
        url: $(this).attr("href"),
    }).done(function(data, status){

        // this just send back the form with the right info already filled out 
        var template = $('#edit-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
    });

    $('#answer_div').on('submit', '#edit_form',function(event){ // on submit
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: $(this).attr("action"),
        data: query_string,
    }).done(function(data, status){

        var template = $('#profile-template').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });
});

///// Search /////
    $('#nav').on('click', ".search", function(event){
        event.preventDefault();
        var template = $('#search-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#user_search_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form
    console.log(query_string)

    $.ajax({
        method: "POST",
        url: $(this).attr("action"),
        data: query_string,
    }).done(function(data, status){

            var template = $('#results-template').html();
            var renderM = Mustache.render(template,data);
            $('#answer_div').html(renderM);  
        });
    });


    $('#answer_div').on('submit', '#tag_search_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: $(this).attr("action"),
        data: query_string,
    }).done(function(data, status){

            var template = $('#results-template').html();
            var renderM = Mustache.render(template,data);
            $('#answer_div').html(renderM);  
        });
    });

});




