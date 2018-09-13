function(doc) { 
     if (doc.doc_type == "LocationUpdate") 
               emit(doc.driver_id, doc); 
               }




