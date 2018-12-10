

function loadData(department){
    $(document).ready(function(){
    $.getJSON("./example.json", function(data){
       $("#art_table tr").remove();// clean so can add data
       $('#art_table').append("<tr style=\"border-width: 1px;border-color: lightgray;\">\
                         <th>Image</th>\
                        <th>Title</th>\
                        <th>Tombstone</th>\
                        <th>Department</th>\
                        <th>Creators</th>\
                   </tr>");//headers
       //$('#art_table').css({borderColor: 'lightgray', borderWidth: '1px'});
        var art_data = '';
        $.each(data, function(key, value){
            console.log(department)
            if(value.department.indexOf(department)>-1)// indexof to check department
            {
                art_data += '<tr>';
                art_data += '<td><img height="100px" width="100px" src="./images/'+value.accession_number+'_reduced.jpg"/></td>';
                // art_data += '<td>' + value.id+'</td>';
                // art_data += '<td>' + value.accession_number+'</td>';
                art_data += '<td>' + value.title+'</td>';
                art_data += '<td>' + value.tombstone+'</td>';
                art_data += '<td>' + value.department+'</td>';
                art_data += '<td>';
                $.each(value.creators, function(key, value){
                    art_data += value.role+': ' + value.description+',\n';
                    });
                art_data += '</td>';
            }
        });

           $('#art_table').append(art_data);// Data 
        });
    });
}
      

function loadDepartments() {
    $(document).ready(function(){
    $.getJSON("./departments.json", function(data){
       var art_data = '';
            var j  = 4;
            art_data += '<tr>';

            for(var i =0; i < data.length; i++)
            {
                art_data += '<td><button class="button button1" onclick="load(\''+data[i]+'\')">'+data[i]+'</button></td>';
                if(parseInt((i+1)%j) === 0 && i+1 !== 0)//&& i+1 !== 0 check or leave it
                    art_data += '</tr><tr>';
            }
            art_data += '</tr>';
            console.log(art_data);

            $('#art_table').append(art_data);
        });
    });
}
//  <button class="back" id="backButton" style="visibility:hidden" onclick="back()"><img  height="50px" width="50px" src="https://cdn1.iconfinder.com/data/icons/ui-color/512/Untitled-21-512.png"/></button>

function load(department)// button to back
{
    document.getElementById("backButton").style.visibility = "visible";
    console.log("clicked arg:",department);
    loadData(department);
}
function back()
{
    document.getElementById("backButton").style.visibility = "hidden";
    $("#art_table tr").remove();
    loadDepartments();
}
loadDepartments();
