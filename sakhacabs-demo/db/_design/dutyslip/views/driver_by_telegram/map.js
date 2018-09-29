function(doc) { 
     if (doc.telegram_id&&doc.role=="driver") 
               emit(doc.telegram_id, doc); 
               }



