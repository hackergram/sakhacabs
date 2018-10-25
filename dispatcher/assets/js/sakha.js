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
            ajax: {
                url: 'http://'+serverip+':5000/driver',
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
        }, 30000 );
       
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

    fillData: function(){
        console.log("Filling data");
        this.fillDrivers();
        this.fillBookings();
        this.fillVehicles();
        this.fillLocationUpdates();
    },
    
    fillAssignments: function(pagenum=1){
        
        function AssignmentViewModel() {
            var self = this;
            self.assignments = ko.observableArray().extend({ paged: { pageSize: 3 } });;
            self.setPage = function(newPage) {
                self.chars.pageNumber(newPage);
            };
            var baseUri = 'http://'+serverip+':5000/assignment';

            $.getJSON(baseUri, function (data) {
                assigns=data.resp;
               
                //console.log(data.resp)
               ko.mapping.fromJS(data.resp, {}, self.assignments);
                console.log(self.assignments())
            });
        }
        ko.applyBindings(new AssignmentViewModel());
        ko.bindingHandlers.date = {
        update: function (element, valueAccessor) {
            
            var value = valueAccessor();
            
            //var date = moment(value());
           //var strDate=new 
           var strDate=new Date(value())
            //var strDate = date.format();
            //console.log(element)
            $(element).text(strDate)
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
                { width:"35%",data: 'pickup_timestamp',defaultContent:"None",render: function(data){return new Date(data['$date'])}},
                {width:"40%", data: 'pickup_location',defaultContent:"None",render: function(data){if(data){return data}}},
                {width:"10%", data: 'cust_id', defaultContent:"None", render: function(data){if(data){return data}}},
                {width:"15%", data: 'booking_id', defaultContent:"None", render: function(data){if(data){return data}}}
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
    }
    
}