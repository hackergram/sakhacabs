function(doc) { 
     if (doc.role == "customer") 
               emit(doc.telegram_id, doc); 
               }



