function(doc) { 
     if (doc.role == "driver") 
               emit(doc.telegram_id, doc); 
               }



