$(document).ready(function () {
    // session = new QiSession("127.0.0.1:80");

    //  use qimessaging-json directly 
    // the port 8002 is the port qimessaging-json is listening to
    // the string "1.0" avoids to have to rewrite url with reverse proxy
    session = new QiSession("127.0.0.1:8002", "1.0");

    $('#page_empty').show();
    $('#page_1').hide();
    $('#page_2').hide();
    $('#page_3').hide();
    $('#restart').hide();


    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("Choix/Page0").done(function(subscriber) {

            subscriber.signal.connect(function(val) {
                $('#page_empty').show();
                $('#page_1').hide();
                $('#page_2').hide();
                $('#page_3').hide();
                $('#restart').hide();
		console.log("val:"+val);
		$('#text_start').html("<h1>"+val+"</h1>");
            });
        });


        ALMemory.subscriber("Choix/Page1").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_1').show();
                $('#page_empty').hide();
                $('#page_2').hide();
                $('#page_3').hide();
                $('#restart').hide();

            });
        });

        ALMemory.subscriber("Choix/Page2").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_2').show();
                $('#page_empty').hide();
                $('#page_1').hide();
                $('#page_3').hide();
                $('#restart').show();

            });
        });

        ALMemory.subscriber("Choix/Page3").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_3').show();
                $('#page_empty').hide();
                $('#page_1').hide();
                $('#page_2').hide();
                $('#restart').show();

            });
        });

        ALMemory.subscriber("objet").done(function(subscriber) {

            subscriber.signal.connect(function(val1) {
                $('#page_3').show();
                $('#page_1').hide();
                $('#page_2').hide();
                $('#page_empty').hide();
                $('#restart').show();

		console.log("val:"+val1);
        $('#order').html('<h1>'+'your '+val1+' is coming </h1>');
        $('#img_order').html('<div style="text-aligne: center"> <img src="img/'+val1+'.png"></div>');
            });
        });

    });

    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

	$('#footer_start').on('click', function() {
        console.log("click Start");
        raise('Choix/Start', 1)
    });

    $('#choice_1_1').on('click', function() {
        console.log("click 1");
        raise('Choix/Button1', 1)
    });

    $('#choice_1_2').on('click', function() {
        console.log("click 2");
        raise('Choix/Button2', 1)
    });

    $('#choice_1_3').on('click', function() {
        console.log("click 3");
        raise('Choix/Button3', 1)
    });
    $('#choice_2_1').on('click', function() {
        console.log("click 1");
        raise('Choix/table1', 1)
    });

    $('#choice_2_2').on('click', function() {
        console.log("click 2");
        raise('Choix/table2', 1);
        raise('fincommande', 1)
    });
    $('#restart').on('click', function() {
        console.log("click restart");
        raise('Choix/Restart', 1);
        raise('fincommande', 1)
    });

});
