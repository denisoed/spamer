const sel_portal = document.getElementById('select_portal');
const name_inp = document.getElementById('id_name');

sel_portal.addEventListener('change', function () {
    name_inp.value = this.value;
}, false);
