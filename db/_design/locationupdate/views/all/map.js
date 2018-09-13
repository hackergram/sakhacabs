function(doc) { 
     if (doc.doc_type == "LocationUpdate") 
               emit(doc.checkin, doc); 
               }




