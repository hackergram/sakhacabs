function getDict(entry){
    dict=[]
	$(entry).each(function(){
        template={}
        template['id']=this.title.$t
        valuepairs=this.content.$t.split(", ")
            $(valuepairs).each(function(){
					key=$.trim(this.split(": ")[0]);
					value=$.trim(this.split(": ")[1]);
					value=value.replace(",",", ")
					template[key]=value;
        });
        dict.push(template)		
    });
    return dict
}


function render(template,data){
    for (key in data){
        //console.log("{"+key+"}"+data[key])
        template=template.replace("{"+key+"}",data[key])
    }
    //console.log(template)   
    return template
}



function addTemplateRows(data,template,section,classname){
	data.forEach(function(d){
        var div=document.createElement("div")
        div.setAttribute("class",classname)
        div.innerHTML=render(template,d)
        sec=document.getElementById(section)
        sec.appendChild(div)
	})
}



function displayList(template,url=null,section,classname){
	if (url!=null){
		console.log(teamurl)
		$.getJSON(url,function(data){
            entry=data.feed.entry
			list=getDict(entry)
			console.log(team)
			addTemplateRows(list,template,section,classname)
		});
	}
}

function generateGrid(parent,members,mincolspan=3){
    numrows=Math.floor(members.length/(12/mincolspan))+1
    numcols=Math.ceil(members.length/numrows)
    colspan=Math.ceil(12/numcols)
    console.log(parent,members.length,numcols,numrows,colspan)
    titlerow=document.createElement("div")
    titlerow.setAttribute("class","row align-items-center")
    titlecol=document.createElement("div")
    titlecol.setAttribute("class","col-sm-12 text-center")
    titlecol.innerHTML='<h2 class="display-4">'+parent+'</h2>'
    titlerow.append(titlecol)
    
    par=document.getElementById(parent)
    par.append(titlerow)
    memindex=0
    for (i = 0; i < numrows; i++) {
        row=document.createElement("div")
        row.setAttribute("class","row align-items-center")
        console.log(colspan.toString())
        colclass="col-sm-"+colspan.toString()+" text-center"
        for (j=0;j<numcols;j++){
            col=document.createElement("div")
            col.setAttribute("class",colclass)
            if (memindex<members.length){
                //console.log(members[memindex])
                col.innerHTML= '<div class="p-5 btn" onclick="window.open('+members[memindex]['url']+')"> <img class="img-fluid rounded-circle profile" src="'+members[memindex]['image']+'" alt=""><h5>'+members[memindex]['id']+'</h5><h6>'+members[memindex]['heading']+'<br><small><strong>'+members[memindex]['subheading']+'</strong></small></h6></div>'
                row.append(col)
                memindex=memindex+1    
            }
        }
        par.append(row)
    } 
}


