function(doc) { 
     if (doc.telegram_id&&doc.role=="customer") 
               emit(doc.telegram_id, doc); 
               }



