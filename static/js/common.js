const selected_portal = $('#id_name');
const messages = $('#messages');
const selected_portals = $('.selected_portals')
const sel_portal = document.getElementById('select_portal');
const name_inp = document.getElementById('id_name');

sel_portal.addEventListener('change', function () {
    name_inp.value = this.value;
}, false);


// Hide message after 4 seconds
(function hideMessage() { 
    setTimeout(function () {
        messages.fadeOut('slow');
    }, 4000);
})();

(function checkSelectedPortals() {
    let portals = $('.selected_portal')
    for (let i = 0; i < portals.length; i++) {
        $('.selected_portals_form').html('<input type="text" name="selected_portals" value="%s">' % portals[i]);
    }
})();

$('.the_portal').click(function (event) {
    elem = $(this);
    $(elem).toggleClass('the_portal_disable');
    $(elem).children('span').toggleClass('lamp_disable');
    // the_portal = $(elem).text()
    // a = $(selected_portals).find('<input type="text" value="' + $.trim(the_portal) + '" name="selected_portal">');
    // if () {
        // $(selected_portals).remove('<input type="text" value="' + $.trim(the_portal) +'" name="selected_portal">');
    // } else {
        // $(selected_portals).append('<input type="text" value="' + $.trim(the_portal) +'" name="selected_portal">');
    // }
});



