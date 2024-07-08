$("#new_material").click(function (e) { 
    $("#new_material_content").removeClass('d-none');
    $("#old_material_content").addClass('d-none');
    $("#new_material").addClass('mmn-nav-bottom');
    $("#old_material").removeClass('mmn-nav-bottom');
});

$("#old_material").click(function (e) {
    $("#old_material_content").removeClass('d-none');
    $("#new_material_content").addClass('d-none');
    $("#old_material").addClass('mmn-nav-bottom');
    $("#new_material").removeClass('mmn-nav-bottom');
});

$(document).ready(function () {
    
});