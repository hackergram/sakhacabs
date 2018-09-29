function(doc) { 
     if (doc.doc_type == "User") 
               emit([doc.telegram_id,doc.role], doc); 
               }
