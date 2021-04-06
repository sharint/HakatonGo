
    var contacts =[
        {name:"John Doe", number:"432-234-5432", address:"1234 Some Street Austin, Texas", notes:""},
        {name:"Sam Clark", number:"321-876-1454", address:"4322 Some Other Street Austin, Texas", notes:"Old high school buddy."},
        {name:"Ryan Smith", number:"433-123-8900", address:"8093 Some Lane Austin, Texas", notes:""},
        {name:"Sally Jane", number:"938-783-5099", address:"4893 Some Circle Austin, Texas", notes:""},
        {name:"Nicole Smith", number:"432-132-4032", address:"2980 Some Place Austin, Texas", notes:"Friend from college."}
    
    ]
    var output='';
    for(var i in contacts)
    {
       output+='<tr><td>'+contacts[i].name+'</td><td>'+contacts[i].number+'</td><td>'+contacts[i].address+'</td><td>'+contacts[i].notes+'</td></tr>';
    }
    let tab = document.getElementById("tab");
    tab.innerHTML = output;