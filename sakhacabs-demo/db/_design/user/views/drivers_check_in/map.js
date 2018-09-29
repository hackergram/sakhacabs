function(doc) { 
     if (doc.role=="driver") 
               emit(doc.checkedin, doc); 
               }



