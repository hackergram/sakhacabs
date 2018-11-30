sakha={
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
                { width:"15%",data: 'pickup_timestamp',defaultContent:"None",render: function(data){return new Date(data['$date'])}},
                {width:"15%", data: 'pickup_location',defaultContent:"None",render: function(data){if(data){return data}}},
                {width:"20%", data: 'passenger_detail', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"15%", data: 'cust_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"15%", data: 'booking_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"10%", data: 'assignment', defaultContent:"None", render: function(data){if(data){return data}}},
                { data: null,render: function(data){
                    bookingid='"'+data.booking_id+'"'
                    return "<button onclick='sakha.deleteBooking("+bookingid+")'>Delete</button>"
                }}
            ],
            scrollY: 200,
            scrollX:true
        });
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
       
        
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
                window.open(data.resp[0],"_blank")
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
                { data: 'vehicle_id', defaultContent: "None"},
                { data: 'driver_id', defaultContent: "None", render:function(data){if(data){return data}else{return "Checked Out"}}  },
                { data: 'reg_num', defaultContent: "Unknown", render:function(data){return data}  }
                
            ],
            scrollY: 200
            
        });
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
       
        
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
                    return String.toUpperCase(data.status)
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.open_time){
                    return new Date(data.open_time.$date)
                        }
                    else{
                        return "None"
                    }
                }},
                { data: null,render: function(data){
                    if(data.close_time){
                    return new Date(data.close_time.$date)
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
                    return String.toUpperCase(data.payment_mode)
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
                    return "<button onclick='sakha.deleteDutySlip("+dsid+")'>Delete</button>"
                }}
                
            ]
        });
         
        setInterval( function () {
                table.ajax.reload( null, false ); // user paging is not reset on reload
        }, 30000 );
    },
    fillData: function(){
        console.log("Filling data");
        
        this.fillDrivers();
        this.fillBookings();
        this.fillVehicles();
        this.fillLocationUpdates();
        this.fillDutySlips();
        
    },
    fillAssignments: function(pagenum=1){
        
        function AssignmentViewModel() {
            var self = this;
            self.assignments = ko.observableArray().extend({ paged: { pageSize: 3 } });;
            self.setPage = function(newPage) {
                self.chars.pageNumber(newPage);
            };
            var baseUri = 'http://'+serverip+':5000/assignment';
            var dutyslipuri = 'http://'+serverip+':5000/dutyslip/by_assignment_id';
            var assigns,assignswithids
            $.getJSON(baseUri, function (data) {
               assigns=data.resp;
               mapassignments=function(){
                    ko.mapping.fromJS(assigns, {}, self.assignments);
                    console.log(self.assignments())
               }
               mapassignments()
               
                
            });
        }
        ko.applyBindings(new AssignmentViewModel());
        ko.bindingHandlers.date = {
        update: function (element, valueAccessor) {
            
            var value = valueAccessor();
            
            //var date = moment(value());
           //var strDate=new 
           var strDate=new Date(value())
           console.log(moment(value()).format('MMMM Do YYYY, h:mm:ss a'))
            //var strDate = date.format();
            //console.log(element)
            $(element).text(moment(value()).format('MMMM Do YYYY, h:mm:ss a'))
             //console.log(strDate)
        }
    };
       
        
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
                            style:    'os',
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
          if (!$('#dutysliplist').hasClass("editing")) {
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
                    return options;
                }));
                $("#Vehicle_" + data.driver.driver_id).val(thisVehicleText)
            }
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
            columns: [
                //{ data: function (row){'value.meta.first_name' + "value.meta.last_name" }}
                { width:"10%",data: 'pickup_timestamp',defaultContent:"None",render: function(data){return new Date(data['$date'])}},
                {width:"15%", data: 'pickup_location',defaultContent:"None",render: function(data){if(data){return data}}},
                 {width:"15%", data: 'drop_location',defaultContent:"None",render: function(data){if(data){return data}}},
               
                {width:"25%", data: 'passenger_detail',defaultContent:"None",render: function(data){if(data){return data}}},
                {width:"10%", data: 'cust_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"15%", data: 'booking_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"10%", data: 'assignment', defaultContent:"None", render: function(data){if(data){return data}}}
            ],
            scrollY: 100
         
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
        
        dutyslips=$("#dutysliplist").DataTable().rows({selected: true }).data()
        for (i=0;i<dutyslips.length;i++){
            //dutyslips[i]['vehicle']=$("Vehicle_"+dutyslips[i].driver.driver_id).val()
            assignmentdict.dutyslips.push(dutyslips[i])
        }
        console.log(assignmentdict)
        var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
        var url = "http://"+serverip+":5000/assignment";
        var params = JSON.stringify(assignmentdict);
        http.open("POST", url, true);

        //Send the proper header information along with the request
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 && http.status == 200) {
                //alert(http.responseText);
                $("#assignmentdetail").text(http.responseText)
            }
        }
        http.send(params);
    },
    deleteAssignment: function(id){
       console.log("Clicked "+ id)
       console.log("Deleting assignment with id: "+ id.split("_")[1]+" and associated duty slips")    
       var http = new XMLHttpRequest(); //$.post("http://"+serverip+":5000/assignment",assignmentdict)
        var url = "http://"+serverip+":5000/assignment/by_id/"+id.split("_")[1];
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
                $("#driverid").val(data.resp[0].driver_id)
                $("#mobnum").val(data.resp[0].mobile_num)
                $("#firstname").val(data.resp[0].first_name)
                $("#lastname").val(data.resp[0].last_name)
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
                $("#status").val(String.toUpperCase(data.resp[0].status))
                $("#created_time").val(moment(data.resp[0].created_time.$date).format('MMMM Do YYYY, h:mm:ss a'));
                $("#open_time").val(moment(data.resp[0].open_time.$date).format('MMMM Do YYYY, h:mm:ss a'));
                $("#close_time").val(moment(data.resp[0].close_time.$date).format('MMMM Do YYYY, h:mm:ss a')); 
                $("#total_time").val(moment(data.resp[0].close_time.$date).diff(moment(data.resp[0].open_time.$date),"hours",true).toFixed(2));
                $("#open_kms").val(data.resp[0].open_kms)
                $("#close_kms").val(data.resp[0].close_kms)
                $("#total_kms").val(parseFloat(data.resp[0].close_kms)-parseFloat(data.resp[0].open_kms))
                $("#payment_mode").val(data.resp[0].payment_mode)
                $("#parking_charges").val(data.resp[0].parking_charges)
                $("#toll_charges").val(data.resp[0].toll_charges)
                $("#amount").val(data.resp[0].amount)
            })
       
       document.getElementById("savedutyslip").setAttribute("onclick","sakha.saveDutySlip('"+dsid+"')")
                    
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
            if(http.readyState == 4 && http.status == 200) {
                    //alert(http.responseText);
                    response=JSON.parse(http.responseText)
                    console.log(response)
                    if(response.status==="success"){
                       document.getElementById("driverstatus").innerHTML="<span style='color:green'>Success!</span>"
                        console.log("success")
                    }
                    
                    if (response.status==="error"){
                        console.log("error")
                         document.getElementById("driverstatus").innerHTML="<span style='color:red'>"+response.resp+"</span>" 
                    }
                    
                }
            }
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
    saveDutySlip: function(dsid){
        console.log("Saving duty slip with ID "+dsid)
        dutyslipdict={}
        dutyslipdict.driver=$("#driver").val()
        dutyslipdict.vehicle=$("#vehicle").val()
        dutyslipdict.dutyslip_id=$("#dutyslip_id").val()
        dutyslipdict.status=String.toLowerCase($("#status").val())
        dutyslipdict.created_time=moment($("#created_time").val(),'MMMM Do YYYY, h:mm:ss a').valueOf()
        //moment(.$date).format('MMMM Do YYYY, h:mm:ss a'));
        dutyslipdict.open_time=moment($("#open_time").val(),'MMMM Do YYYY, h:mm:ss a').valueOf()
        //moment(.$date).format('MMMM Do YYYY, h:mm:ss a'));
        dutyslipdict.close_time=moment($("#close_time").val(),'MMMM Do YYYY, h:mm:ss a').valueOf()
        //moment(.$date).format('MMMM Do YYYY, h:mm:ss a'));
        dutyslipdict.open_kms=$("#open_kms").val()
        dutyslipdict.close_kms=$("#close_kms").val()
        dutyslipdict.payment_mode=$("#payment_mode").val()
        dutyslipdict.parking_charges=$("#parking_charges").val()
        dutyslipdict.toll_charges=$("#toll_charges").val()
        dutyslipdict.amount=$("#amount").val()
        params=JSON.stringify(dutyslipdict)
        console.log(params)
        var url = "http://"+serverip+":5000/dutyslip/by_id/"+dsid;
        var http = new XMLHttpRequest();
        http.open("PUT", url, true);
        http.setRequestHeader("Content-type", "application/json");
        http.onreadystatechange = function() {//Call a function when the state changes.
            if(http.readyState == 4 && http.status == 200) {
                response=JSON.parse(http.responseText)
                console.log(response)
       
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

