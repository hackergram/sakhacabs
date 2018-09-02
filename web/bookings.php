    
<?php
// function to verify session status
function is_session_started()
{
    if ( php_sapi_name() !== 'cli' ) {
        if ( version_compare(phpversion(), '5.4.0', '>=') ) {
            return session_status() === PHP_SESSION_ACTIVE ? TRUE : FALSE;
        } else {
            return session_id() === '' ? FALSE : TRUE;
        }
    }
    return FALSE;
}
// verifying POST data and adding the values to session variables





if(isset($_POST["code"])){
  session_start();
  $_SESSION["code"] = $_POST["code"];
  $_SESSION["csrf_nonce"] = $_POST["csrf_nonce"];
  $ch = curl_init();
  // Set url elements
  $fb_app_id = '294008394485958';
  $ak_secret = '9c8b67552d1294e34c22e8254dba9d5d';
  $token = 'AA|'.$fb_app_id.'|'.$ak_secret;
  // Get access token
  $url = 'https://graph.accountkit.com/v1.0/access_token?grant_type=authorization_code&code='.$_POST["code"].'&access_token='.$token;
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_URL,$url);
  $result=curl_exec($ch);
  $info = json_decode($result);
  if ($info->error->code==100){
      session_start();
      unset($_SESSION);
      session_destroy();
      header('Location: signup.php'); 
  }
  else{
  // Get account information
    $url = 'https://graph.accountkit.com/v1.0/me/?access_token='.$info->access_token;
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_URL,$url);
    $result=curl_exec($ch);
    curl_close($ch);
    $final = json_decode($result);  
  }
}
if(isset($_GET["code"])){
  session_start();
  $_SESSION["code"] = $_GET["code"];
  $_SESSION["csrf_nonce"] = $_GET["state"];
  $ch = curl_init();
  // Set url elements
  $fb_app_id = '294008394485958';
  $ak_secret = '9c8b67552d1294e34c22e8254dba9d5d';
  $token = 'AA|'.$fb_app_id.'|'.$ak_secret;
  // Get access token
  $url = 'https://graph.accountkit.com/v1.0/access_token?grant_type=authorization_code&code='.$_GET["code"].'&access_token='.$token;
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_URL,$url);
  $result=curl_exec($ch);
  $info = json_decode($result);
  // Get account information
  if ($info->error->code==100){
        session_start();
        unset($_SESSION);
        session_destroy();
        header('Location: signup.php'); 
  }
  else{
    $url = 'https://graph.accountkit.com/v1.0/me/?access_token='.$info->access_token;
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_URL,$url);
    $result=curl_exec($ch);
    curl_close($ch);
    $final = json_decode($result);  

  }
    

}
$string = file_get_contents("hashtags.json");
$json_a = json_decode($string, true);
if( isset($json_a[$final->id])){
    $alreadysubmitted=true;
    $hashtag=$json_a[$final->id]['hashtag'];
    $entryname=$json_a[$final->id]['entryname'];
}
?>



<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="Competitive, Frugal Innovation">
        <meta name="author" content="The Great Indian Jugaad Challenge">


        <!-- HTTPS required. HTTP will give a 403 forbidden response -->
        <script src="https://sdk.accountkit.com/en_US/sdk.js"></script>
        <script>
            

          // initialize Account Kit with CSRF protection
            AccountKit_OnInteractive = function(){
                AccountKit.init(
                    {
                        appId:"294008394485958", 
                        state:"abcd", 
                        version:"v1.1",
                        fbAppEventsEnabled:true,
                        debug:true,
                        redirect:"https://tgijc.com/signup.php"
                    }
                );
            };
        </script>
        <link href="css/ak.css" rel="stylesheet">
        <link href="css/stepwizard.css" rel="stylesheet">
       
        
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-53668433-3"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'UA-53668433-3');
        </script>
        
        <title>The Great Indian Jugaad Challenge</title>

        <!-- Bootstrap core CSS -->
        <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="vendor/bootstrap/js/bootstrap.min.js"></script>

        <script src="js/vis.js"></script>
        <!-- Custom fonts for this template -->
        <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <!-- Custom styles for this template -->
        <link href="css/one-page-wonder.css" rel="stylesheet">
        <script src="js/mwbootstrapdisplayfromgdocs.js"></script>
        <link href="css/main.css" rel="stylesheet">
        <link href="css/vis.css" rel="stylesheet" type="text/css" />

    </head>
    <body>
        <div id="fb-root"></div>
        <script>
            window.fbAsyncInit = function() {
                FB.init({
                    appId      : '294008394485958',
                    cookie     : true,
                    xfbml      : true,
                    version    : 'v3.1'
                });

                FB.AppEvents.logPageView();   
            };

          (function(d, s, id){
                 var js, fjs = d.getElementsByTagName(s)[0];
                 if (d.getElementById(id)) {return;}
                 js = d.createElement(s); js.id = id;
                 js.src = "https://connect.facebook.net/en_US/sdk.js";
                 fjs.parentNode.insertBefore(js, fjs);
           }(document, 'script', 'facebook-jssdk'));
            
            
        </script>
        <!--
        <script>
            

          // initialize Account Kit with CSRF protection
            AccountKit_OnInteractive = function(){
                AccountKit.init(
                    {
                        appId:"294008394485958", 
                        state:"abcd", 
                        version:"v1.1",
                        fbAppEventsEnabled:true,
                        debug:true,
                        redirect:"signup.php"
                    }
                );
            };
        </script>
        --->
        <script>
            // login callback
            function loginCallback(response) {
                    if (response.status === "PARTIALLY_AUTHENTICATED") {
                        //console.log(response)
                    var code = response.code;
                    var csrf = response.state;
                    // Send code to server to exchange for access token
                    document.getElementById("code").value = response.code;
                    document.getElementById("csrf_nonce").value = response.state;
                    document.getElementById("my_form").submit();    
                }
                else if (response.status === "NOT_AUTHENTICATED") {
                  // handle authentication failure
                }
                else if (response.status === "BAD_PARAMS") {
                  // handle bad parameters
                }
            }

            // phone form submission handler
            function smsLogin() {
                //var countryCode = document.getElementById("country_code").value;
                //var phoneNumber = document.getElementById("phone_number").value;
                AccountKit.login(
                    'PHONE', 
                    {}, // will use default values if not specified countryCode: countryCode, phoneNumber: phoneNumber
                    loginCallback
                );
            }


            // email form submission handler
            function emailLogin() {
                //var emailAddress = document.getElementById("email").value;
                AccountKit.login(
                    'EMAIL',
                    {},//emailAddress: emailAddress
                    loginCallback
                );
            }

            function step2(){
                submission={}
                submission['firstname']=document.getElementById("firstname").value;
                submission['lastname']=document.getElementById("lastname").value;
                submission['location']=document.getElementById("location").value;
                submission['myurl']=document.getElementById("myurl").value
                console.log(submission);
                //document.getElementById("access_token").value=
                document.getElementById("submission").submit();
            }



            function uuidv4() {
                return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                    return v.toString(16);
                });
            }
            function share() {
                var entryname = '<?php echo $entryname;?>';
                var hashtag = '<?=$hashtag ?>';
                
            FB.ui({
                        method: 'feed',
                        hashtag: hashtag,
                        
                    }, function(response){
                            
                    }
                );
            }
            function logout() {
                document.location = 'logout.php';
            }
          
            
        </script>   
        <!-- Navigation 
        <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
          <div class="container">
            <a class="navbar-brand" href="#">Start Bootstrap</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
              <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                  <a class="nav-link" href="#">Sign Up</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">Log In</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>-->
        <header class="masthead text-center text-white">
            <div class="masthead-content">
                <div class="container" style="height: 50px">
                    <h5 class="masthead-subheading mb-0">Signup</h5>
                    <h4>The Great Indian Jugaad Challenge 2018</h4>
                    <h5>Theme: <font style="color: yellow"> Waste Management & Upcycling</font></h5>
                    <h5>Prize: <font style="color: yellow">₹50,000</font></h5>
                    <h5>Signup Closes: <font style="color: yellow    ">15 September 2018</font></h5>
                </div>
            </div>
            <!--
            <div class="bg-circle-1 bg-circle"></div>
            <div class="bg-circle-2 bg-circle"></div>
            <div class="bg-circle-3 bg-circle"></div>
            <div class="bg-circle-4 bg-circle"></div>
            -->
           
        </header>
        
        <section id="timeline">
            <div class="row align-items-center" >
                <div class="col-sm-12 text-center" >
                <div id="story" class="p-5">
						<h3>Contest Timeline</h3>
						<center><div id="visualization"></div>
						</center>
						<script>
				
							// load device list in GeoJSON from a Google spreadsheet
							
							function getEventList(entry){
								events=[]
								i=1
								$(entry).each(function(){
									template={}
									template['content']=this.title.$t
									template.id=i
									valuepairs=this.content.$t.split(",")
									$(valuepairs).each(function(){
										key=$.trim(this.split(": ")[0]);
										value=$.trim(this.split(": ")[1]);
										template[key]=value;
									});
									events.push(template)
									i=i+1;		
								});
								return events
							}
							
							
							var url="https://spreadsheets.google.com/feeds/list/10Hd02ofOklyYdfrdPF5Ie9xnGRp1f7oB7QJEB5P1Juw/od6/public/basic?alt=json"
							$.getJSON(url, function(data) {
								var entry = data.feed.entry;
								events=getEventList(entry)
								//console.log(events)
								var container = document.getElementById('visualization');
								var options = {};
								var timeline = new vis.Timeline(container, events, options);


							});
						</script>	
						
					
					</div>
                </div>
            </div>
        </section>
               <section id="signupsection">
            <div class="row align-items-center" id="signupworkflow">
             
             <div class="col-sm-12 text-center" >
                
                    <?php
                        // verifying if the session exist
                    if(is_session_started() === FALSE && !isset($_SESSION)){
                    ?>
                           
                            <div class="p-5">
                                 <div class="buttons">
                                <button onclick="smsLogin();">Signup with Mobile Number<br> मोबाइल नम्बर से साइन अप करें</button>
                            </div>
                                  <h3> Sign up for TGIJC2018 <br> TGIJC2018 में भाग लें</h3>
                                        <p>To sign up for the challenge, <br>log in with your mobile number and get your registration code <br> We will be sharing problem statements on 15 September 2018</p>
                                        <p>चैलेंज में भाग लेने के लिये <br>अपने मोबाइल नंबर द्वारा लाग इन करें और अपना रेजिस्ट्रेशन कोड प्राप्त करें <br> प्रतियोगिता के प्रश्न १५ सितंबर २०१८ को साझा किये जायेंगे
                            
                            <form action="" method="POST" id="my_form">
                              <input type="hidden" name="code" id="code">
                              <input type="hidden" name="csrf_nonce" id="csrf_nonce">
                            </form>
                            </div>  
                   
                   
                    <?php
                    }
                    else{
                    ?>
                   
                            <div class="p-5">
                            <p class="ac">You're logged in!<br>आप लाग इन हो गये!</p>

                            <h3 class="ac">Your Information<br>आपकी जानकारी</h3>
                            <p class="ac">
                            <!-- show account information -->
                            <strong>ID|आइडी:</strong> <?=$final->id?> <br>



                   
                    <?php
                    if(isset($final->email)){
                    ?>
                  
                            <strong>Email|ई मेल:</strong> <?=$final->email->address?>

                                
                    <?php
                    }
                    else{
                    ?>
                    
                            <strong>Country Code|राष्ट्रीय दूरभाष कोड:</strong> +<?=$final->phone->country_prefix?> <br>
                            <strong>Phone Number|मोबाइल नम्बर:</strong> <?=$final->phone->national_number?> 
                 
                    <?php
                    }
                    ?>
                    
                            </div>
                                          
                     <?php
                    if ($alreadysubmitted===true){
                    ?>
                            <div class="p-5">
                            <h3 class="ac">Looks like you've already signed up! </h3> We will be releasing problem statements on 15 September 2018! Please check back after then!<br>
                                <h3 class="ac">लगता है आप पहले ही साइन अप कर चुके है! </h3> प्रतियोगिता की चुनौतियां १५ सितम्बर २०१८ को रिलीज़ करी जायेंगी। कृपया १५ सितम्बर के उपरांत पुनः लाग इन करें
                            
                                                      
                    <?php
                    }
                    else
                    {
                    ?>


                </div>
            </div>
            <div class="row align-items-center">

                            <div class="stepwizard col-md-offset-12">

                            <div class="stepwizard-row setup-panel">
                              <div class="stepwizard-step">
                                <a href="#step-1" type="button" class="btn btn-primary btn-circle">1</a>
                                <p>You<br>आप</p>
                                </div>
                              <div class="stepwizard-step">
                                <a href="#step-2" type="button" class="btn btn-default btn-circle" disabled="disabled">2</a>
                                <p>Go!<br>भेजें!</p>
                              </div>
                            </div>
                            </div>
            </div>
            <div class="row align-items-center">

                <div class="stepwizard-content col-md-offset-3">
                    <form role="form"  action="signup-success.php" method="post" id="submission">

                            <div class="row align-items-center setup-content" id="step-1">
                                  <div class="col-xs-6 col-md-offset-3 text-center">
                                    <div class="col-md-offset-12">
                                      <h3> Tell us about you<br>हमें अपने बारे में बतायें</h3>
                                      <div class="form-group">
                                        <label class="control-label">Name|नाम</label>
                                        <input name="name" id= "name"  maxlength="100" type="text" required="required" class="form-control" placeholder="Name|नाम "  />
                                      </div>
                                      <div class="form-group">
                                        <label class="control-label">Email|ईमेल</label>
                                        <input name="email" id= "email" maxlength="200" type="email" required="required" class="form-control" placeholder="Email|ईमेल" />
                                      </div>
                                        <div class="form-group">
                                        <label class="control-label">Location|स्थान</label>
                                        <input name="location" id= "location" maxlength="100" type="text" required="required" class="form-control" placeholder="Your Location|आपका स्थान" />
                                      </div>
                                      <button class="btn btn-primary nextBtn btn-lg pull-right" type="button" >Next</button>
                                    </div>
                                  </div>
                                </div>
                              
                            
                                <div class="row align-items-center setup-content" id="step-2">
                                  <div class="col-xs-6 col-md-offset-3 text-center">
                                    <div class="col-md-12">
                                      <h3> Go!<br>भेजें!</h3>

                                      <button class="btn btn-success btn-xl rounded-pill mt-5" type="submit" ><i class="fa fa-paper-plane fa-flip-horizontal" style="font-size: 36px"></i><br>Go!|भेजें!</button>
                                         <!--

                                        <a onclick="step2()" class="btn btn-primary btn-xl rounded-pill mt-5"></a> -->
                                    </div>
                                  </div>
                                </div>

                                <input type="hidden" id="access_token" name="access_token" value="<?=$info->access_token?>">
                </form>

                       
                </div>
            </div>

                                
                                
                                   
               
                <?php
                }
                ?>
                    
                    <div class="buttons">
                    <button onclick="logout();">Logout</button>
                    </div>
                
                <?php
                }
                ?>

           
        
               
                 
        </section>    
        <footer class="py-5 bg-black">
            <div class="container">
                <p class="m-0 text-center text-white small"><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>
                <br/>This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
                <br>
                <a href="https://www.freepik.com/free-photos-vectors/icon">Icon vector created by Freepik</a>
                </p>
            </div>
          <!-- /.container -->
        </footer>
        <!-- Bootstrap core JavaScript -->
        <script src="vendor/jquery/jquery.min.js"></script>
        <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
        <script type="text/javascript">
  $(document).ready(function () {
  var navListItems = $('div.setup-panel div a'),
          allWells = $('.setup-content'),
          allNextBtn = $('.nextBtn');

  allWells.hide();

  navListItems.click(function (e) {
      e.preventDefault();
      var $target = $($(this).attr('href')),
              $item = $(this);

      if (!$item.hasClass('disabled')) {
          navListItems.removeClass('btn-primary').addClass('btn-default');
          $item.addClass('btn-primary');
          allWells.hide();
          $target.show();
          $target.find('input:eq(0)').focus();
      }
  });

  allNextBtn.click(function(){
      var curStep = $(this).closest(".setup-content"),
          curStepBtn = curStep.attr("id"),
          nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
          curInputs = curStep.find("input[type='text'],input[type='url']"),
          isValid = true;

      $(".form-group").removeClass("has-error");
      for(var i=0; i<curInputs.length; i++){
          if (!curInputs[i].validity.valid){
              isValid = false;
              $(curInputs[i]).closest(".form-group").addClass("has-error");
          }
      }

      if (isValid)
          nextStepWizard.removeAttr('disabled').trigger('click');
  });

  $('div.setup-panel div a.btn-primary').trigger('click');
});
            
$(document).ready(function() {
    $('#submission').submit(function() {
        window.open('', 'formpopup', 'width=400,height=550,resizeable,scrollbars');
        this.target = 'formpopup';
    });
});
  </script>

      
    </body>
</html>
    