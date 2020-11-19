var orgName=""

$('#org_name').keydown(function(e){
    console.log("input was changed")
    console.log(e.target.value)
    orgName=e.target.value
})

$('#createOrg').submit(function(e){
    e.preventDefault();
    console.log(e);
    console.log("Form was submitted");
    console.log(this)
    if(orgName.length < 5){
        alert("Org name must be longer than 5 characters")
        return null
    }
    $.ajax({
        url: '/create_org',
        method: 'post',
        data: $(this).serialize(),
        success: function(serverResponse){
            console.log("This is AJAX working!!")
            console.log(serverResponse);
            $('#groups').append(serverResponse);
        }
    })
    $(this).trigger('reset');
})