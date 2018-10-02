type = ['','info','success','warning','danger'];


demo = {
    initPickColor: function(){
        $('.pick-class-label').click(function(){
            var new_class = $(this).attr('new-class');
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if(display_div.length) {
            var display_buttons = display_div.find('.btn');
            display_buttons.removeClass(old_class);
            display_buttons.addClass(new_class);
            display_div.attr('data-class', new_class);
            }
        });
    },

    checkScrollForTransparentNavbar: debounce(function() {
            $navbar = $('.navbar[color-on-scroll]');
            scroll_distance = $navbar.attr('color-on-scroll') || 500;

            if($(document).scrollTop() > scroll_distance ) {
                if(transparent) {
                    transparent = false;
                    $('.navbar[color-on-scroll]').removeClass('navbar-transparent');
                    $('.navbar[color-on-scroll]').addClass('navbar-default');
                }
            } else {
                if( !transparent ) {
                    transparent = true;
                    $('.navbar[color-on-scroll]').addClass('navbar-transparent');
                    $('.navbar[color-on-scroll]').removeClass('navbar-default');
                }
            }
    }, 17),

    initDocChartist: function(){
        var dataSales = {
          labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
          series: [
             [287, 385, 490, 492, 554, 586, 698, 695, 752, 788, 846, 944],
            [67, 152, 143, 240, 287, 335, 435, 437, 539, 542, 544, 647],
            [23, 113, 67, 108, 190, 239, 307, 308, 439, 410, 410, 509]
          ]
        };

        var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: 800,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
        };

        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);


        var data = {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
            [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695]
          ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Bar('#chartActivity', data, options, responsiveOptions);

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        Chartist.Pie('#chartPreferences', {
          labels: ['62%','32%','6%'],
          series: [62, 32, 6]
        });
    },

    initChartist: function(){

        var dataSales = {
          labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
          series: [
             [287, 385, 490, 492, 554, 586, 698, 695, 752, 788, 846, 944],
            [67, 152, 143, 240, 287, 335, 435, 437, 539, 542, 544, 647],
            [23, 113, 67, 108, 190, 239, 307, 308, 439, 410, 410, 509]
          ]
        };

        var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: 800,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
        };

        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);


        var data = {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
            [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695]
          ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Bar('#chartActivity', data, options, responsiveOptions);

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        Chartist.Pie('#chartPreferences', {
          labels: ['62%','32%','6%'],
          series: [62, 32, 6]
        });
    },

    initGoogleMaps: function(){
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
          zoom: 13,
          center: myLatlng,
          scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
          styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]

        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title:"Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },

	showNotification: function(from, align){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "pe-7s-gift",
        	message: "Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer."

        },{
            type: type[color],
            timer: 4000,
            placement: {
                from: from,
                align: align
            }
        });
	},
    
    fillTrips: function(){
        console.log("Filling trip data");
        $.getJSON('http://192.168.56.101:5984/sakhacabs/_design/user/_view/drivers_check_in', function(data) {
            myItems = data['rows'];
            console.log(myItems);
        });
    },
    fillBookings: function(){
        console.log("Filling bookings data");
        /*
        $.getJSON('http://192.168.56.101:5984/sakhacabs/_design/user/_view/drivers_check_in', function(data) {
            myItems = data['rows'];
            console.log(myItems);
        });
        */
        var table=$('#bookingtable').DataTable({
            ajax: {
                url: 'http://192.168.56.101:5000/booking',
                dataSrc: 'resp'
            },
            columns: [
                //{ data: function (row){'value.meta.first_name' + "value.meta.last_name" }}
                { width:"20%",data: 'pickup_timestamp',defaultContent:"None",render: function(data){return new Date(data['$date'])}},
                {width:"20%", data: 'pickup_location',defaultContent:"None",render: function(data){if(data){return data}}},
                {width:"20%", data: 'passenger_detail', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"20%", data: 'cust_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"20%", data: 'booking_id', defaultContent:"None", render: function(data){if(data){return data}}}
            ],
            scrollY: 200,
            scrollX:true
        });
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 8000 );
        
    },
    fillLocationUpdates: function(){
        console.log("Filling location data");
        /*
        $.getJSON('http://192.168.56.101:5984/sakhacabs/_design/locationupdate/_view/all', function(data) {
            location_updates = data['rows'];
            console.log(location_updates);
        });
        */
        var table=$('#locationupdatetable').DataTable({
            ajax: {
                url: 'http://192.168.56.101:5000/locupdate',
                dataSrc: 'resp'
            },
            columns: [
                //{ data: function (row){'value.meta.first_name' + "value.meta.last_name" }},
                { data: 'driver_id',render: function(data){return data;}},
                { data: 'checkin',render: function(data){if(data===true){return "Check In"}else{return "Check Out"}}, defaultContent:"None"},
                { data: 'timestamp',render: function(data){return new Date(data['$date'])}, defaultContent:"None"},
                { data: 'location', defaultContent:"None"},
                { data: 'vehicle_id',render: function(data){if(data){return data}}, defaultContent:"None"}
            ],
            scrollY: 200
        });
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 8000 );
    },
    fillDrivers: function(){
        console.log("Filling driver data");
        var table = $('#drivertable').DataTable({
            //ajax: 'http://192.168.56.101:5000/driver/all'
            
            ajax: {
                url: 'http://192.168.56.101:5000/driver',
                dataSrc: "resp" 
            },
            columns: [
                //{ data: function (row){retturn'metadata.first_name' + "metadata.last_name" }},
                { data: null, render: function (data){return data.driver_id }},
                //{ data: 'checkedin' },
                { data: 'checkedin', defaultContent: "None", render:function(data){if(data===true){return "Checked In"}else{return "Checked Out"}} },
                { data: 'onduty', defaultContent: "None", render:function(data){if(data){return data}else{return "Unknown"}}  }
                
            ],
            scrollY: 200
        });
         
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 8000 );
       
    },
    fillVehicles: function(){
        console.log("Filling vehicle data");
        
        var table = $('#vehicletable').DataTable({
            //ajax: 'http://192.168.56.101:5000/driver/all'
            
            ajax: {
                url: 'http://192.168.56.101:5000/vehicle',
                dataSrc: "resp" 
            },
            columns: [
                //{ data: function (row){retturn'metadata.first_name' + "metadata.last_name" }},
                //{ data: 'metadata', render: function (data){return data.first_name +" "+ data.last_name }},
                //{ data: 'checkedin' },
                { data: 'vehicle_id', defaultContent: "None"},
                { data: 'driver_id', defaultContent: "None", render:function(data){if(data){return data}else{return "Checked Out"}}  },
                { data: 'reg_num', defaultContent: "Unknown", render:function(data){return data}  }
                
            ],
            scrollY: 200
            
        });
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 8000 );
       
        
    },

    fillData: function(){
        console.log("Filling data");
        this.fillTrips();
        this.fillDrivers();
        this.fillBookings();
        this.fillVehicles();
        this.fillLocationUpdates();
    }
}
