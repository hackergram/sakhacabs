var decodeEntities = (function() {
  // this prevents any overhead from creating the object each time
  var element = document.createElement('div');

  function decodeHTMLEntities (str) {
    if(str && typeof str === 'string') {
      // strip script/html tags
      str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
      str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
      element.innerHTML = str;
      str = element.textContent;
      element.textContent = '';
    }

    return str;
  }

  return decodeHTMLEntities;
})();




var sakha={
    fillData: function(){
        console.log("Filling data");

        this.fillDrivers();
        this.fillBookings();
        this.fillVehicles();
        this.fillLocationUpdates();
        this.fillDutySlips();

    },
    fillBookings: function(){
        console.log("Filling bookings data");
        /*
        $.getJSON('http://'+serverip+':5984/sakhacabs/_design/user/_view/drivers_check_in', function(data) {
            myItems = data['rows'];
            console.log(myItems);
        });
        */
        var table=$('#bookingtable').DataTable({
            select: true,
            ajax: {
                url: 'http://'+serverip+':5000/booking',
                dataSrc: 'resp'
            },
            columns: [
                //{ data: function (row){'value.meta.first_name' + "value.meta.last_name" }}
                { width:"5%",data: null,render: function(data){
                    bookingid='"'+data.booking_id+'"'
                    return "<button onclick='sakha.deleteBooking("+bookingid+")'>Delete</button>"

                }},
                {width:"10%", data: 'booking_id', defaultContent:"None", render: function(data){
                    if(data){

                        var bookingid='<a class="nav-link" data-toggle="modal" data-target="#editbookingform" data-bookingid="'+data+'">\
                        <i class="material-icons">content_paste</i> '+data+'\
                        </a>'

                        return bookingid


                    }
                }},

                { width:"15%",data: 'pickup_timestamp',defaultContent:"None",render: function(data){

                    //console.log(data)
                    return moment(data.$date+1).format("YYYY-MMM-DD HH:mm:ss")
                    }},
                {width:"25%", data: 'pickup_location',defaultContent:"None",render: function(data){if(data){
                    return data
                    }}},
                {width:"25%", data: 'passenger_detail', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"10%", data: 'cust_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"10%", data: 'assignment', defaultContent:"None", render: function(data){if(data){return data}}},

            ],
            scrollY: 200,
            scrollX:true
        });
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
         $("#exportbookings").on("click",function(){
             console.log("exporing bookings")
            $.getJSON('http://'+serverip+':5000/booking/export',function(data){
                window.open(data.resp,"_blank")
            })
        })

    },
    fillLocationUpdates: function(){
        console.log("Filling location data");
        /*
        $.getJSON('http://'+serverip+':5984/sakhacabs/_design/locationupdate/_view/all', function(data) {
            location_updates = data['rows'];
            console.log(location_updates);
        });
        */
        var table=$('#locationupdatetable').DataTable({
            ajax: {
                url: 'http://'+serverip+':5000/locupdate',
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
        }, 30000 );
          $("#exportlocupdates").on("click",function(){
            $.getJSON('http://'+serverip+':5000/locupdate/export',function(data){
                window.open(data.resp,"_blank")
            })
        })
    },
    fillDrivers: function(){
        console.log("Filling driver data");
        var table = $('#drivertable').DataTable({
            //ajax: 'http://'+serverip+':5000/driver/all'
            select: true,
            buttons: [
            'excel'
            ],
            ajax: {
                url: 'http://'+serverip+':5000/driver',
                dataSrc: "resp"
            },

            columns: [
                //{ data: function (row){retturn'metadata.first_name' + "metadata.last_name" }},
                { data: null, render: function (data){

                    var driverid='<a class="nav-link" data-toggle="modal" data-target="#createdriverform" data-driverid="'+data.driver_id+'">\
                        <i class="material-icons">content_paste</i> '+data.driver_id+'\
                        </a>'
                    return driverid
                }},
                { data: null,render: function(data){
                    if(data.mobile_num){
                    return data.mobile_num
                        }
                    else{
                        return "None"
                    }
                }},
                { data: 'checkedin', defaultContent: "None", render:function(data){if(data===true){return "Checked In"}else{return "Checked Out"}} },
                { data: 'onduty', defaultContent: "None", render:function(data){if(data){return data}else{return "Unknown"}}  },
                { data: null,render: function(data){
                    driverid='"'+data.driver_id+'"'
                    return "<button onclick='sakha.deleteDriver("+driverid+")'>Delete</button>"
                }}


            ],
            scrollY: 200
        });

        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
        $("#exportdrivers").on("click",function(){
            $.getJSON('http://'+serverip+':5000/driver/export',function(data){
                console.log(data.resp)
                window.open(data.resp,"_blank")
            })
        })
    },
    fillVehicles: function(){
        console.log("Filling vehicle data");

        var table = $('#vehicletable').DataTable({
            //ajax: 'http://'+serverip+':5000/driver/all'
            select: true,
            ajax: {
                url: 'http://'+serverip+':5000/vehicle',
                dataSrc: "resp"
            },
            columns: [
                //{ data: function (row){retturn'metadata.first_name' + "metadata.last_name" }},
                //{ data: 'metadata', render: function (data){return data.first_name +" "+ data.last_name }},
                //{ data: 'checkedin' },
                {data:null, defaultContent:"None", render: function(data){      //

                    var vehicle_id='<a class="nav-link" data-toggle="modal" data-target="#createvehicleform" data-vehicle_id="'+data.vehicle_id+'">\
                        <i class="material-icons">content_paste</i> '+data.vehicle_id+'\
                        </a>'
                    return vehicle_id
                }},
                { data: 'driver_id', defaultContent: "None", render:function(data){if(data){return data}else{return "Checked Out"}}  },
                { data: 'reg_num', defaultContent: "Unknown", render:function(data){return data}  }

            ],
            scrollY: 200

        });





        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
          $("#exportvehicles").on("click",function(){
            $.getJSON('http://'+serverip+':5000/vehicle/export',function(data){
                console.log(data.resp)
                window.open(data.resp,"_blank")
            })
        })

    },
    fillDutySlips: function(){
         console.log("Filling dutyslip data");
        var table = $('#dutysliptable').DataTable({
            //ajax: 'http://'+serverip+':5000/driver/all'
            select: true,
            ajax: {
                url: 'http://'+serverip+':5000/dutyslip',
                dataSrc: "resp"
            },
            columns: [
                //{ data: function (row){retturn'metadata.first_name' + "metadata.last_name" }},
                { data: null, render: function (data){

                    var dutyslip_id='<a class="nav-link" data-toggle="modal" data-target="#editdutyslipform" data-dsid="'+data._id.$oid+'">\
                        <i class="material-icons">content_paste</i> '+data.dutyslip_id+'\
                        </a>'
                    return dutyslip_id
                }},
                { data: null,render: function(data){
                    if(data.created_time){
                    return moment(data.created_time.$date)
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.driver){
                    return data.driver
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.status){
                    return data.status.toUpperCase()
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.open_time){
                    return moment(data.open_time.$date)
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.close_time){
                    return moment(data.close_time.$date)
                        }
                    else{
                        return "None"
                    }
                }},
                 { data: null,render: function(data){
                    if(data.open_kms){
                    return data.open_kms
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.close_kms){
                    return data.close_kms
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.payment_mode){
                    return data.payment_mode.toUpperCase()
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.amount){
                    return data.amount
                        }
                    else{
                        return "None"
                    }
                }},
                 { data: null,render: function(data){
                    dsid='"'+data._id.$oid+'"'
                    return "<button onclick='sakha.deleteDutySlip("+dsid+")'>Delete</button>\
                            <button onclick='sakha.updateDutySlipStatus("+dsid+",\"verified\")'>Verify</button>"
                }}

            ]
        });

        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
    },


    fillAssignmentModal: function(assignmentid){
        console.log("Editing Assignment - " +  assignmentid);
        if(assignmentid=="newassignment"){
            console.log("Creating new assignment")
            assignmentdict.assignment['id']="newid"
        }
        this.updateassignmentbookinglist();
        this.updateassignmentvehiclelist();
        this.updateassignmentdutysliplist();



    },
    updateassignmentdutysliplist: function(){
     var table,dutysliplist,driverlist,vehiclelist;
     dutysliplist=[];
     driverlist=[];
     vehiclelist=[];

        if($.fn.dataTable.isDataTable("#dutysliplist"))
     {
         if ($('#dutysliplist').hasClass("editing")) {
            $('#dutysliplist').removeClass("editing");
         }
         table=$('#dutysliplist').DataTable();
         table.clear().destroy();
         $('#dutysliplist tbody').empty();
         //builddutysliptable()
     }
     //else
     //{
         console.log("Building dutyslip table")
         var gotdrivers=false;
         var gotvehicles=false;

         $.getJSON("http://"+serverip+":5000/driver",function(data){

             driverlist=data.resp;
             console.log(driverlist);
             gotdrivers=true;
             if(gotvehicles){
                 builddutysliptable();

             }
             else{
                 console.log("vehicles not set")
             }
          });
         $.getJSON("http://"+serverip+":5000/vehicle",function(data){

             //console.log(data);
             //vehiclelist=data.resp;
             for (i=0;i<data.resp.length;i++){
                 vehiclelist.push(data.resp[i].vehicle_id)
             }
             gotvehicles=true;
             console.log(vehiclelist)
             if(gotdrivers){
                 builddutysliptable();
             }
              else{
                 console.log("drivers not set")
             }
          });
       //}
        builddutysliptable = function(){
              for (i=0;i<driverlist.length;i++){
                     var dutyslip={}
                     dutyslip['driver']=driverlist[i].driver_id
                     dutysliplist.push(dutyslip)

              }
              console.log("Building dutyslip table2")
              table=$('#dutysliplist').DataTable({
                        rowId: 'driver',
                        //destroy: true,
                        columnDefs: [ {
                            orderable: false,
                            className: 'select-checkbox',
                            targets:   0
                        } ],
                        select: {
                            style:    'multi',
                            selector: 'td:first-child'
                        },
                        order: [[ 1, 'asc' ]],
                        //responsive: true,
                        /*
                        ajax: {
                            url: 'http://'+serverip+':5000/driver',
                            dataSrc: 'resp'
                        },
                        */
                        data: dutysliplist,
                        columns: [
                              {width:"15%", defaultContent:""},
                              {data: 'driver',defaultContent:"None"},
                              {data: 'driver.onduty', defaultContent:"None", render: function(data){if(data){return data}else{return "Unknown"}}},
                              {data: null, defaultContent:"None", render: function(row){if(row.vehicle){
                                            return row.vehicle;
                                    }
                                  //console.log(row);

                                }
                              }
                        ],
                        scrollY: 100
                    });

            }

      $('#dutysliplist').on('click',"tr", function() {
           // var row = this.parentElement;
          console.log(table.row(this).id())
          //if (!$('#dutysliplist').hasClass("editing")) {
                $('#dutysliplist').addClass("editing");
                var data = table.row(this).data();
                console.log(data)
                var $row = $(this);
                var thisVehicle = $row.find("td:nth-child(4)");
                var thisVehicleText = thisVehicle.text();
                thisVehicle.empty().append($("<select></select>", {
                    "id": "Vehicle_" + data.driver.driver_id,
                    "class": "changeVehicle"
                }).append(function() {
                    var options = [];
                    $.each(vehiclelist, function(k, v) {
                        options.push($("<option></option>", {
                            "text": v,
                            "value": v
                        }))
                    })
                    options.push($("<option></option>", {
                            "text": "None",
                            "value": null
                        }))
                    return options;
                }));
                $("#Vehicle_" + data.driver.driver_id).val(thisVehicleText)
            //}
        });

      $('#dutysliplist').on("change", ".changeVehicle", function() {
            var $this = $(this);
            //console.log(table.row($this.parent("td").parent("tr")).data())
            var tempData = table.row($this.closest("tr")).data();
            //console.log(tempData)
            tempData['vehicle']=$this.val();
            //tempData[2] = $this.val();
            table.row($this.closest("tr")).data(tempData);
            console.log(dutysliplist)
            $this.parent("td").empty().text($this.val());
            $('#dutysliplist').removeClass("editing");
        });
    },
    updateassignmentvehiclelist: function(){
        if($.fn.dataTable.isDataTable("#vehiclelist"))
         {
             var table=$('#vehiclelist').DataTable()
         }
         else
         {
            var table=$('#vehiclelist').DataTable({
                select: true,
                responsive: true,
                ajax: {
                    url: 'http://'+serverip+':5000/vehicle',
                    dataSrc: 'resp'
                },
                columns: [
                    { data: 'vehicle_id',defaultContent:"None",render: function(data){if(data){return data}}},
                    { data: 'driver_id', defaultContent:"None", render: function(data){if(data){return data}}},
                    {data: 'reg_num', defaultContent:"None", render: function(data){if(data){return data}}}
                ],
                scrollY: 100
            });
          }


    },
    updateassignmentbookinglist: function(){
     if($.fn.dataTable.isDataTable("#bookinglist"))
     {
         var table=$('#bookinglist').DataTable()
     }
     else
     {
        var table=$('#bookinglist').DataTable({
            select: true,
            responsive: true,
            ajax: {
                url: 'http://'+serverip+':5000/booking',
                dataSrc: 'resp'
            },
             columnDefs: [ {
                            orderable: false,
                            className: 'select-checkbox',
                            targets:   0
                        } ],
             select: {
                            style:    'multi',
                            selector: 'td:first-child'
                        },
            columns: [
                //{ data: function (row){'value.meta.first_name' + "value.meta.last_name" }}
                 {width:"5%", defaultContent:""},
                { width:"15%",data: 'pickup_timestamp',defaultContent:"None",render: function(data){

                    return new moment(data['$date']+1).format('MMMM Do YYYY, h:mm:ss a')
                }},
                {width:"15%", data: 'pickup_location',defaultContent:"None",render: function(data){if(data){return data}}},
                 {width:"15%", data: 'drop_location',defaultContent:"None",render: function(data){if(data){return data}}},

                {width:"25%", data: 'passenger_detail',defaultContent:"None",render: function(data){if(data){return data}}},
                {width:"10%", data: 'cust_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"5%", data: 'booking_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"5%", data: 'assignment', defaultContent:"None", render: function(data){if(data){
                    return "Assigned"
                }}}
            ],
            scrollY: 400

        });
      }
    },
    saveAssignment: function(){
        console.log(assignmentdict)
        assignmentdict['assignment']={}
        assignmentdict.assignment['bookings']=[]
        assignmentdict['dutyslips']=[]

        bookings=$("#bookinglist").DataTable().rows({selected: true }).data()
        for (i=0;i<bookings.length;i++){
            assignmentdict.assignment.bookings.push(bookings[i])
        }
        console.log(assignmentdict.assignment.bookings)
        if (assignmentdict.assignment.bookings.length===0){
            alert("Please select some bookings first")
        }
        assignmentdict.assignment.cust_id=assignmentdict.assignment.bookings[0].cust_id
        dutyslips=$("#dutysliplist").DataTable().rows({selected: true }).data()
        for (i=0;i<dutyslips.length;i++){
            //dutyslips[i]['vehicle']=$("Vehicle_"+dutyslips[i].driver.driver_id).val()
            assignmentdict.dutyslips.push(dutyslips[i])
            if(dutyslips[i].vehicle===""){
                dutyslips[i].vehicle=null
            }
        }
        var createassign=true;
        console.log(assignmentdict)
        if(assignmentdict.assignment.bookings[0].pickup_timestamp.$date.valueOf() < moment().valueOf()){
          createassign=confirm("Pickup Time Has Already Passed! Still create assignment?")
          console.log(moment(assignmentdict.assignment.bookings[0].pickup_timestamp).valueOf())
         console.log(moment().valueOf())

        }

        var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
        var url = "http://"+serverip+":5000/assignment";
        var params = JSON.stringify(assignmentdict);
        http.open("POST", url, true);

        //Send the proper header information along with the request
        http.setRequestHeader("Content-type", "application/json");

        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 && http.status == 200) {
                response=JSON.parse(http.responseText)
                if (response.status==="success"){
                    alert("Successfully created assignment");
                    $("#reporting_timestamp").text(JSON.stringify(response.resp[0].reporting_timestamp))
                    $("#reporting_location").text(JSON.stringify(response.resp[0].reporting_location))
                }
                else{
                    alert("Failed to create assignment");
                    $("#assignmentdetail").text(response.resp)
                }

            }
        }
        if (createassign===true){
            http.send(params);
        }

    },
    updateAssignmentStatus: function(assignment_id,status){
        dict={}
        dict.assignment_id=assignment_id
        dict.status=status
        var params=JSON.stringify(dict)
        var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
        var url = "http://"+serverip+":5000/assignment/updatestatus";
        http.open("POST", url, true);

        //Send the proper header information along with the request
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 && http.status == 200) {
                //alert(http.responseText);
                alert(http.responseText)
                window.location.reload(false);
            }
        }
        http.send(params);
    },
    updateDutySlipStatus: function(dsid,status){
        console.log(dsid,status)
        dict={}
        dict.dsid=dsid
        dict.status=status
        var params=JSON.stringify(dict)
        var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
        var url = "http://"+serverip+":5000/dutyslip/updatestatus";
        http.open("POST", url, true);
        console.log(url,dict)
        //Send the proper header information along with the request
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 && http.status == 200) {
                //alert(http.responseText);
                alert(http.responseText)
                window.location.reload(false);
            }
        }
        http.send(params);
    },
    deleteAssignment: function(id){
       console.log("Clicked "+ id)
       //console.log("Deleting assignment with id: "+ id.split("_")[1]+" and associated duty slips")
       console.log("Deleting assignment with id: "+ id+" and associated duty slips")

        var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
          var url = "http://"+serverip+":5000/assignment/by_id/"+id;

        //var url = "http://"+serverip+":5000/assignment/by_id/"+id.split("_")[1];
        //var params = JSON.stringify(assignmentdict);
        http.open("DELETE", url, true);

        //Send the proper header information along with the request
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 && http.status == 200) {
                //alert(http.responseText);
                //$("#assignmentdetail").text(http.responseText)
                window.location.reload(false);
            }
        }
        http.send();
    },
    fillDriverModal: function(driverid){
        if(driverid==="newdriver"){
            console.log("creating new driver")
            $("#driverid").val("")
            $("#mobnum").val("")
            $("#firstname").val("")
            $("#lastname").val("")

        }
        else{
            console.log("editing driver "+driverid)
            $.getJSON('http://'+serverip+':5000/driver/by_driver_id/'+driverid,function(data){
                console.log(data.resp[0])
                $("#driverid").attr("readonly",true).val(decodeEntities(data.resp[0].driver_id))
                $("#mobnum").val(decodeEntities(data.resp[0].mobile_num))
                $("#firstname").val(decodeEntities(data.resp[0].first_name))
                $("#lastname").val(decodeEntities(data.resp[0].last_name))
            })
        }

       document.getElementById("savedriver").setAttribute("onclick","sakha.saveDriver('"+driverid+"')")

    },
    fillDutySlipModal: function(dsid){
       console.log("editing dutyslip "+dsid)
       var url = 'http://'+serverip+':5000/dutyslip/by_id/'+dsid
       console.log("getting url "+url)

            $.getJSON(url,function(data){
                console.log(data.resp[0])
                $("#driver").val(data.resp[0].driver)
                $("#vehicle").val(data.resp[0].vehicle)
                $("#dutyslip_id").val(data.resp[0].dutyslip_id)
                $("#status").val(data.resp[0].status).change()
                //$("#created_time").val(moment(data.resp[0].created_time.$date).format('MMMM Do YYYY, h:mm:ss a'));
                $("#created_time").empty()
                $("#created_time").append( moment(data.resp[0].created_time.$date).format('ddd MMM Do YYYY, h:mm:ss a'));
                if (data.resp[0].hasOwnProperty("open_time")){
                    $("#open_time").val(moment(data.resp[0].open_time.$date).format('YYYY-MM-DD HH:mm:ss'));
                }
                else{
                    $("#open_time").val(null)
                }
                if (data.resp[0].hasOwnProperty("close_time")){

                    $("#close_time").val(moment(data.resp[0].close_time.$date).format('YYYY-MM-DD HH:mm:ss'));
                   $("#total_time").val(moment(data.resp[0].close_time.$date).diff(moment(data.resp[0].open_time.$date),"hours",true).toFixed(2));

                    //'YYYY-MM-DD HH:mm'
                }     //$("#total_time").text=moment(data.resp[0].close_time.$date).diff(moment(data.resp[0].open_time.$date),"hours",true).toFixed(2);
                $("#open_kms").val(decodeEntities(data.resp[0].open_kms))
                $("#close_kms").val(decodeEntities(data.resp[0].close_kms))
                $("#total_kms").val(parseFloat(data.resp[0].close_kms)-parseFloat(data.resp[0].open_kms))
                $("#payment_mode").val(decodeEntities(data.resp[0].payment_mode.toUpperCase()))
                $("#parking_charges").val(data.resp[0].parking_charges)
                $("#toll_charges").val(decodeEntities(data.resp[0].toll_charges))
                $("#amount").val(decodeEntities(data.resp[0].amount))
                $("#ds_remarks").val(decodeEntities(data.resp[0].remarks))
            })

       document.getElementById("savedutyslip").setAttribute("onclick","sakha.saveDutySlip('"+dsid+"')")

    },



    fillVehicleModal: function(vehicle_id){
           console.log("editing vehicl"+vehicle_id)
           var url = 'http://'+serverip+':5000/vehicle/by_vehicle_id/'+vehicle_id
           console.log("getting url "+url)

                $.getJSON(url,function(data){
                    console.log(data.resp[0])
                  //  $("#vehicle_pickup_timestamp").empty()
                    $("#vehicle_id").append(data.resp[0].vehicle_id )
                    $("#vehid").val(decodeEntities(data.resp[0].vehicle_id))



                    $("#vehcat").val(decodeEntities(data.resp[0].vehicle_cat))
                    $("#vehname").val(decodeEntities(data.resp[0].vehicle_name))

              })

         document.getElementById("savevehicle").setAttribute("onclick","sakha.savevehicle('"+vehicle_id+"')")
    },
        savevehicle: function(vehicle_id){
             console.log("Trying to save "+vehicle_id)
             vehicledict={}
             vehicledict.vehicle_id=$("#vehid").val()
             vehicledict.vehicle_cat=$("#vehcat").val()
             vehicledict.vehicle_name=$("#vehname").val()
         //    vehicledict.last_name=$("#lastname").val()
             var params = JSON.stringify(vehicledict);
             var http = new XMLHttpRequest();
             if(vehicle_id==="newvehicle"){
                 //$.post("http://"+serverip+":5000/assignment",assignmentdict)
                 var url = "http://"+serverip+":5000/vehicle";
                 http.open("POST", url, true);
             }
             else{
                 var url = "http://"+serverip+":5000/vehicle/by_vehicle_id/"+vehicle_id;
                 http.open("PUT", url, true);

             }
             if (vehicledict.vehicle_id.length>4){
                 http.setRequestHeader("Content-type", "application/json");
                 http.onreadystatechange = function() {//Call a function when the state changes.
                 if(http.readyState == 4 ) {
                     if(http.status == 200){
                         response=JSON.parse(http.responseText)
                         console.log(response)
                         if(response.status==="success"){
                            document.getElementById("vehiclelist").innerHTML="<span style='color:green'>Success!</span>"
                             alert("Saved vehicle Successfully!")
                             console.log("success")
                         }
                         if (response.status==="error"){
                             console.log("error")
                             alert("Failed to Save   vehicle!")
                              document.getElementById("vehiclelist").innerHTML="<span style='color:red'>"+response.resp+"</span>"
                         }
                         }
                         else{
                         alert("Network Error Saving vehicle.")
                         }
                         }

                         }
                         http.send(params);
                         }
                         else{
                         alert(" vehicle ID must be at least 5 characters")
                         }



           },








    fillCustomerModal: function(cust_id){
       console.log("editing customer "+cust_id)
       var url = 'http://'+serverip+':5000/customer/by_cust_id/'+cust_id
       console.log("getting url "+url)

            $.getJSON(url,function(data){
                console.log(data.resp[0])
              //  $("#customer_pickup_timestamp").empty()
               $("#cust_id").append(data.resp[0].cust_id )
                $("#customerid").val(decodeEntities(data.resp[0].cust_id))


            //    $("#customer_product_id").val(data.resp[0].product_id)
            //    $("#customer_status").val(data.resp[0].status).change()
                //$("#created_time").val(moment(data.resp[0].created_time.$date).format('MMMM Do YYYY, h:mm:ss a'));
                //$("#customer_pickup_timestamp").empty()
            //    $("#customer_pickup_timestamp").val(moment(data.resp[0].pickup_timestamp.$date+1).format('YYYY-MM-DD HH:mm:ss'))

            //    $("#customer_created_timestamp").empty()

              //  $("#customer_created_timestamp").append(moment(data.resp[0].created_timestamp.$date).format('MMMM Do YYYY, h:mm:ss a'));
              // $("#customer_channel").val(data.resp[0].customer_channel);
                //$("#total_time").text=moment(data.resp[0].close_time.$date).diff(moment(data.resp[0].open_time.$date),"hours",true).toFixed(2);
              //  $("#customer_cust_meta").val(JSON.stringify(data.resp[0].cust_meta))
            //    $("#customer_remarks").val(data.resp[0].remarks)
                $("#customermobnum").val(decodeEntities(data.resp[0].mobile_num))
                $("#customerbillingdisplay").val(decodeEntities(data.resp[0].cust_billing))
            //    $("#customer_passenger_detail").val(data.resp[0].passenger_detail)

              //  $("#customer_pickup_location").val(data.resp[0].pickup_location)
            //    $("#customer_drop_location").val(data.resp[0].drop_location)


          })

     document.getElementById("savecustomer").setAttribute("onclick","sakha.saveCustomer('"+cust_id+"')")





  },//kj-v101-
    saveCustomer: function(cust_id){
        console.log("Trying to save "+cust_id)
        customerdict={}
        customerdict.cust_id=$("#customerid").val()
        customerdict.mobile_num=$("#customermobnum").val()
        customerdict.cust_billing=$("#customerbillingdisplay").val()
    //    customerdict.last_name=$("#lastname").val()
        var params = JSON.stringify(customerdict);
        var http = new XMLHttpRequest();
        if(customerid==="newcustomer"){
            //$.post("http://"+serverip+":5000/assignment",assignmentdict)
            var url = "http://"+serverip+":5000/customer";
            http.open("POST", url, true);
        }
        else{
            var url = "http://"+serverip+":5000/customer/by_cust_id/"+cust_id;
            http.open("PUT", url, true);

        }
        if (customerdict.cust_id.length>4){
            http.setRequestHeader("Content-type", "application/json");
            http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 ) {
                if(http.status == 200){
                    response=JSON.parse(http.responseText)
                    console.log(response)
                    if(response.status==="success"){
                       document.getElementById("customerlist").innerHTML="<span style='color:green'>Success!</span>"
                        alert("Saved Customer Successfully!")
                        console.log("success")
                    }
                    if (response.status==="error"){
                        console.log("error")
                        alert("Failed to Save   customer!")
                         document.getElementById("customerlist").innerHTML="<span style='color:red'>"+response.resp+"</span>"
                    }
                    }
                    else{
                    alert("Network Error Saving Customer.")
                    }
                    }

                    }
                    http.send(params);
                    }
                    else{
                    alert(" Customer ID must be at least 5 characters")
                    }



      },



      fillProductModal: function(product_id){
         console.log("editing product "+product_id)
         var url = 'http://'+serverip+':5000/product/by_product_id/'+product_id
         console.log("getting url "+url)

              $.getJSON(url,function(data){
                  console.log(data.resp[0])
                //  $("#product_pickup_timestamp").empty()
                  $("#productid").append(data.resp[0].product_id )
                  $("#productid").val(decodeEntities(data.resp[0].product_id))
                  $("#inclu_hrs").val(decodeEntities(data.resp[0].included_hrs))
                  $("#ext_hrs").val(decodeEntities(data.resp[0].extra_hrs_rate ))
                  $("#incl_kms").val(decodeEntities(data.resp[0].included_kms))
                  $("#ext_kms").val(decodeEntities(data.resp[0].extra_kms_rate))
                  $("#pri").val(decodeEntities(data.resp[0].price))

                })

              document.getElementById("saveproduct").setAttribute("onclick","sakha.saveproduct('"+product_id+"')")

  },
  saveproduct: function(product_id){
      console.log("Trying to save "+product_id)
      productdict={}
      productdict.product_id=$("#productid").val()
      productdict.included_hrs=$("#inclu_hrs").val()
      productdict.extra_hrs_rate=$("#ext_hrs").val()
      productdict.included_kms=$("#incl_kms").val()
      productdict.extra_kms_rate=$("#ext_kms").val()
      productdict.price=$("#pri").val()


      var params = JSON.stringify(productdict);
      var http = new XMLHttpRequest();
      if(productid==="newproduct"){
          //$.post("http://"+serverip+":5000/assignment",assignmentdict)
          alert("Do you want a new product?")
          var url = "http://"+serverip+":5000/product";
          http.open("POST", url, true);
      }
      else{
          var url = "http://"+serverip+":5000/product/by_product_id/"+product_id;
          http.open("PUT", url, true);

      }
      if (productdict.product_id.length>4){
          http.setRequestHeader("Content-type", "application/json");
          http.onreadystatechange = function() {//Call a function when the state changes.
          if(http.readyState == 4 ) {
              if(http.status == 200){
                  response=JSON.parse(http.responseText)
                  console.log(response)
                  if(response.status==="success"){
                     document.getElementById("productlist").innerHTML="<span style='color:green'>Success!</span>"
                      alert("Saved product Successfully!")
                      console.log("success")
                  }
                  if (response.status==="error"){
                      console.log("error")
                      alert("Failed to Save product!")
                       document.getElementById("productlist").innerHTML="<span style='color:red'>"+response.resp+"</span>"
                  }
                  }

                  else{
                  alert("Network Error Saving product.")
                  }
                  }

                  }
                  http.send(params);
                  }
                  else{
                  alert(" product ID must be at least 5 characters")
                  }



    },



    saveDriver: function(driverid){
        console.log("Trying to save "+driverid)
        driverdict={}
        driverdict.driver_id=$("#driverid").val()
        driverdict.mobile_num=$("#mobnum").val()
        driverdict.first_name=$("#firstname").val()
        driverdict.last_name=$("#lastname").val()
        var params = JSON.stringify(driverdict);
        var http = new XMLHttpRequest();
        if(driverid==="newdriver"){
            //$.post("http://"+serverip+":5000/assignment",assignmentdict)
            var url = "http://"+serverip+":5000/driver";
            http.open("POST", url, true);
        }
        else{
            var url = "http://"+serverip+":5000/driver/by_driver_id/"+driverid;
            http.open("PUT", url, true);

        }
        //Send the proper header information along with the request
        if (driverdict.driver_id.length>4){
            http.setRequestHeader("Content-type", "application/json");
            http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 ) {
                if(http.status == 200){
                    response=JSON.parse(http.responseText)
                    console.log(response)
                    if(response.status==="success"){
                       document.getElementById("driverstatus").innerHTML="<span style='color:green'>Success!</span>"
                        alert("Saved Driver Successfully!")
                        console.log("success")
                    }

                    if (response.status==="error"){
                        console.log("error")
                        alert("Failed to Save Driver!")
                         document.getElementById("driverstatus").innerHTML="<span style='color:red'>"+response.resp+"</span>"
                    }
                }
                else{
                    alert("Network Error Saving Driver")
                }
                }

            }
            console.log(driverdict)
            http.send(params);
        }
        else{
            alert("Driver ID must be at least 5 characters")
        }
    },
    deleteDutySlip: function(dsid){
        t=confirm("Really Delete Duty Slip with ID "+dsid)
        if (t===true){

            var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
            var url = "http://"+serverip+":5000/dutyslip/by_id/"+dsid;
            //var params = JSON.stringify(assignmentdict);
            console.log(url)
            http.open("DELETE", url, true);

            //Send the proper header information along with the request
            http.setRequestHeader("Content-type", "application/json");
            http.onreadystatechange = function() {//Call a function when the state changes.
                if(http.readyState == 4 && http.status == 200) {
                    //alert(http.responseText);
                    //$("#assignmentdetail").text(http.responseText)
                    alert("deleted "+dsid)
                    window.location.reload(true);
                }
            }
            http.send();
        }
        else{
            alert("Cancelled delete!")
        }
    },

    deleteDriver: function(driverid){
        t=confirm("Really Delete Driver with ID "+driverid)
        if (t===true){

            var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
            var url = "http://"+serverip+":5000/driver/by_driver_id/"+driverid;
            //var params = JSON.stringify(assignmentdict);
            console.log(url)
            http.open("DELETE", url, true);

            //Send the proper header information along with the request
            http.setRequestHeader("Content-type", "application/json");
            http.onreadystatechange = function() {//Call a function when the state changes.
                if(http.readyState == 4 && http.status == 200) {
                    //alert(http.responseText);
                    //$("#assignmentdetail").text(http.responseText)
                    alert("deleted "+driverid)
                    window.location.reload(true);
                }
            }
            http.send();
        }
        else{
            alert("Cancelled delete!")
        }
    },
    deleteBooking: function(booking_id){
        t=confirm("Really Delete Booking with ID "+booking_id)
        if (t===true){
            var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
            var url = "http://"+serverip+":5000/booking/by_booking_id/"+booking_id;
            //var params = JSON.stringify(assignmentdict);
            console.log(url)
            http.open("DELETE", url, true);
            //Send the proper header information along with the request
            http.setRequestHeader("Content-type", "application/json");
            http.onreadystatechange = function() {//Call a function when the state changes.
                if(http.readyState == 4 && http.status == 200) {
                    //alert(http.responseText);
                    //$("#assignmentdetail").text(http.responseText)
                    alert("deleted "+booking_id)
                    window.location.reload(true);
                }
            }
            http.send();
        }
        else{
            alert("Cancelled delete!")
        }
    },

    fillBookingModal: function(bookingid){
     console.log("editing booking "+bookingid)
     var url = 'http://'+serverip+':5000/booking/by_booking_id/'+bookingid
     console.log("getting url "+url)

          $.getJSON(url,function(data){
              console.log(data.resp[0])
              $("#booking_pickup_timestamp").empty()
              $("#booking_id").append(data.resp[0].booking_id )
              $("#booking_product_id").val(data.resp[0].cust_id)

              $("#booking_product_id").val(data.resp[0].product_id)
              $("#booking_status").val(data.resp[0].status).change()
              //$("#created_time").val(moment(data.resp[0].created_time.$date).format('MMMM Do YYYY, h:mm:ss a'));
              //$("#booking_pickup_timestamp").empty()
              $("#booking_pickup_timestamp").val(moment(data.resp[0].pickup_timestamp.$date+1).format('YYYY-MM-DD HH:mm:ss'))

              $("#booking_created_timestamp").empty()

              $("#booking_created_timestamp").append(moment(data.resp[0].created_timestamp.$date).format('MMMM Do YYYY, h:mm:ss a'));
             $("#booking_channel").val(data.resp[0].booking_channel);
              //$("#total_time").text=moment(data.resp[0].close_time.$date).diff(moment(data.resp[0].open_time.$date),"hours",true).toFixed(2);
              $("#booking_cust_meta").val(JSON.stringify(data.resp[0].cust_meta))
              $("#booking_remarks").val(data.resp[0].remarks)
              $("#booking_passenger_mobile").val(data.resp[0].passenger_mobile)
              $("#booking_passenger_detail").val(data.resp[0].passenger_detail)

              $("#booking_pickup_location").val(data.resp[0].pickup_location)
              $("#booking_drop_location").val(data.resp[0].drop_location)


          })

     document.getElementById("savebooking").setAttribute("onclick","sakha.saveBooking('"+bookingid+"')")

},
    saveBooking: function(booking_id){
        console.log(booking_id)
        booking_dict={}
        booking_dict.pickup_timestamp=moment($("#booking_pickup_timestamp").val(),"YYYY-MM-DD HH:mm:ss").toDate();
        booking_dict.pickup_location=$("#booking_pickup_location").val();
        booking_dict.cust_meta=JSON.parse($("#booking_cust_meta").val())
        booking_dict.product_id=$("#booking_product_id").val()
        booking_dict.status=$("#booking_status").val()
        booking_dict.booking_channel=$("#booking_channel").val()
        booking_dict.remarks=$("#booking_remarks").prop("value")
        booking_dict.drop_location=$("#booking_drop_location").val()
        booking_dict.passenger_mobile=$("#booking_passenger_mobile").val()
        booking_dict.passenger_detail=$("#booking_passenger_detail").val()
        console.log(booking_dict)

        params=JSON.stringify(booking_dict)
        console.log(params)
        var url = "http://"+serverip+":5000/booking/by_booking_id/"+booking_id;
        var http = new XMLHttpRequest();
        http.open("PUT", url, true);
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 ) {
                if(http.status == 200){
                    response=JSON.parse(http.responseText)
                    console.log(response)
                    if (response.status==="success"){
                        sakha.fillBookingModal(booking_id)
                        alert("Saved booking successfully")

                    }
                    else{
                        alert("Caught Error saving booking - " + response.resp )
                    }
                }
                else{
                    alert("Uncaught Error saving booking!")
                }

            }
        }
        http.send(params);


    },
    saveDutySlip: function(dsid){
        console.log("Saving duty slip with ID "+dsid)
        dutyslipdict={}
        dutyslipdict.driver=$("#driver").val()
        dutyslipdict.vehicle=$("#vehicle").val()
        dutyslipdict.dutyslip_id=$("#dutyslip_id").val()
        dutyslipdict.status=$("#status").val()
        //dutyslipdict.created_time=moment($("#created_time").val(),'MMMM Do YYYY, h:mm:ss a').valueOf()
        //moment(.$date).format('MMMM Do YYYY, h:mm:ss a'));
        //dutyslipdict.open_time=moment($("#open_time").val(),'MMMM Do YYYY, h:mm:ss a').valueOf()
        //dutyslipdict.open_time=$("#open_time").val()
        dutyslipdict.open_time=moment($("#open_time").val(),'YYYY-MM-DD HH:mm:ss').utc().format('YYYY-MM-DD HH:mm:ss')
        //moment(.$date).format('MMMM Do YYYY, h:mm:ss a'));
        //dutyslipdict.close_time=moment($("#close_time").val(),'MMMM Do YYYY, h:mm:ss a').valueOf()
        //dutyslipdict.close_time=$("#close_time").val()
        dutyslipdict.close_time=moment($("#close_time").val(),'YYYY-MM-DD HH:mm:ss').utc().format('YYYY-MM-DD HH:mm:ss')
        //moment(.$date).format('MMMM Do YYYY, h:mm:ss a'));
        dutyslipdict.open_kms=$("#open_kms").val()
        dutyslipdict.close_kms=$("#close_kms").val()
        dutyslipdict.payment_mode=$("#payment_mode").val()
        dutyslipdict.parking_charges=$("#parking_charges").val()
        dutyslipdict.toll_charges=$("#toll_charges").val()
        dutyslipdict.amount=$("#amount").val()
        dutyslipdict.remarks=$("#ds_remarks").prop("value")
        params=JSON.stringify(dutyslipdict)
        console.log(params)
        var url = "http://"+serverip+":5000/dutyslip/by_id/"+dsid;
        var http = new XMLHttpRequest();
        http.open("PUT", url, true);
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 ) {
                if(http.status == 200){
                    response=JSON.parse(http.responseText)
                    console.log(response)
                    if (response.status==="success"){
                        sakha.fillDutySlipModal(dsid)
                        alert("Saved dutyslip successfully")

                    }
                    else{
                        alert("Caught Error saving dutyslip  - " + response.resp)
                    }
                }
                else{
                    alert("Uncaught Error saving duty slip!")
                }

            }
        }
        http.send(params);

    },
    JSONtoCSV: function(jsonstring){
        console.log(jsonstring)
        function parseJSONToCSVStr(jsonData) {
            if(jsonData.length == 0) {
                return '';
            }

            let keys = Object.keys(jsonData[0]);

            let columnDelimiter = ',';
            let lineDelimiter = '\n';

            let csvColumnHeader = keys.join(columnDelimiter);
            let csvStr = csvColumnHeader + lineDelimiter;

            jsonData.forEach(item => {
                keys.forEach((key, index) => {
                    if( (index > 0) && (index < keys.length-1) ) {
                        csvStr += columnDelimiter;
                    }
                    csvStr += item[key];
                });
                csvStr += lineDelimiter;
            });

            return encodeURIComponent(csvStr);;
        }

        function exportToCsvFile(jsonData) {
            let csvStr = parseJSONToCSVStr(jsonData);
            let dataUri = 'data:text/csv;charset=utf-8,'+ csvStr;

            let exportFileDefaultName = 'data.csv';
            console.log("exporting " + csvStr)
            let linkElement = document.createElement('a');
            linkElement.setAttribute('href', dataUri);
            linkElement.setAttribute('download', exportFileDefaultName);
            console.log("clicking")
            linkElement.click();
        }
        exportToCsvFile(jsonstring)
    }
}
