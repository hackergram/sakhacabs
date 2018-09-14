function(doc) { 
     if (doc.doc_type == "Vehicle") 
               emit(doc._id, doc); 
               }




