$( document ).ready(function() {

    // On reload open the download tab
    setTimeout(() => {

        var hash = window.location.hash;
        if (hash != ''){
            hash = hash. substring(1);
            var nav = '#nav-';
            var tab = '-tab';
            hash = nav.concat(hash);
            hash = hash.concat(tab);
            var hash1 = hash.substring(0,hash.length - 4);

            $(".tab-pane").removeClass('show');
            $(".tab-pane").removeClass('active');

            $(".nav-link").removeClass('active');
            $(".nav-link").attr('aria-selected', false);

            $(hash).addClass('active');
            $(hash).attr('aria-selected', true);
            $(hash).removeAttr('tabindex');

            $(hash1).addClass('active');
            $(hash1).addClass('show');

            $(hash).trigger( "click" );
        }

    }, "500");

    // On click open the download tab
    $(".click-trigger").click(function(){

        setTimeout(() => {

            var hash = window.location.hash;
            hash = hash. substring(1);
            var nav = '#nav-';
            var tab = '-tab';
            hash = nav.concat(hash);
            hash = hash.concat(tab);
            var hash1 = hash.substring(0,hash.length - 4);

            $(".tab-pane").removeClass('show');
            $(".tab-pane").removeClass('active');

            $(".nav-link").removeClass('active');
            $(".nav-link").attr('aria-selected', false);

            $(hash).addClass('active');
            $(hash).attr('aria-selected', true);
            $(hash).removeAttr('tabindex');

            $(hash1).addClass('active');
            $(hash1).addClass('show');

            $(hash).trigger( "click" );

        }, "200");

    });

    // On click show loader
    $("form").submit(function(){
        $('.loader').show();
    });

    // Validate input URL for private downloader

    setInterval(function (){

        var url = $('#url').val();

        if (url != ''){
            let domain = (new URL(url));
            domain = domain.hostname;
            if (domain == 'www.facebook.com'){
                const regex_r = new RegExp("/reel/",);
                const regex_v = new RegExp("/watch",);
                const regex_v_p = new RegExp("/videos/",);
                const regex_v_s = new RegExp("/stories/",);
                if ((regex_r.test(url)) || regex_v.test(url) || regex_v_p.test(url) | regex_v_s.test(url)){
                    // url = url.replace(/\?.*$/g,"");
                    url = 'view-source:'+url;
                    $('#scrap_url').val(url);
                }else{
                    $('#url').val('');
                    $('#scrap_url').val('');
                    alert("The URL you pasted is not an Facebook video/reel URL!");
                }
            }else{
                $('#url').val('');
                $('#scrap_url').val('');
                alert("The URL you pasted is not a Facbook video/reel URL!");
            }
        }else{
            $('#scrap_url').val('');
        }

    },1000)


});


