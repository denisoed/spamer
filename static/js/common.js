const sel_portal = document.getElementById('select_portal');
const name_inp = document.getElementById('id_name');
const messages = $('#messages');

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

