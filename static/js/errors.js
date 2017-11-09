const button_submit = $('#btn_submit');
const portal_button_submit = $('.add_portal_btn');
const input_title = $('#inp_title');
const input_url = $('#inp_url');
const portal_login = $('.portal_login');
const portal_password = $('.portal_password');
let all_inputs_portal = $('.right_part :input');

function inputTitleValidation(input) {   
    $(input).keyup( () => {
        let inp_value = $(input).val();
        if (inp_value === '') {
            $(input).prev().html(
                '<li><i class="fa fa-warning"></i> Это поле обязательное!</li>'
            )
        } else if (inp_value.length < 5 || inp_value.length > 50) {
            $(input).prev().html(
                '<li><i class="fa fa-warning"></i> Заголовок должен быть более 5 и менее 50 символов!</li>'
            )
        } else {
            $(input).prev().empty()
        }
        disableSubmit();
    });
}

function inputUrlValidation(input) {   
    $(input).keyup( () => {
        let inp_value = $(input).val();
        if (inp_value === '') {
            $(input).prev().html(
                '<li><i class="fa fa-warning"></i> Это поле обязательное!</li>'
            )
        } else if (/^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:[/?#]\S*)?$/i.test(inp_value) == false) {
            $(input).prev().html(
                '<li><i class="fa fa-warning"></i> Введите корректный url!</li>'
            )
        } else {
            $(input).prev().empty();
        }
        disableSubmit();
    });
}


function disableSubmit() {
    let inp_value_title = $(input_title).val();
    let inp_value_url = $(input_url).val();
    if (inp_value_title == '' || inp_value_url == '') {
        $(button_submit).prop("disabled", true);
    } else {
        if (inp_value_title.length < 5 || inp_value_title.length > 50) {
            $(button_submit).prop("disabled", true);
        } else {
            $(button_submit).prop("disabled", false);
        }
    }
}

function checkEmptyInput(input) {
    $(input).keyup(() => {
        let input_val = $(input).val();
        if (input_val == '') {
            $('.add_auth_new_portal > .inp_error').html(
                '<li><i class="fa fa-warning"></i> Все поля должны быть заполнены!</li>'
            )
            $(portal_button_submit).prop("disabled", true);
        } else {
            $('.add_auth_new_portal > .inp_error').empty();
            $(portal_button_submit).prop("disabled", false);
        }
    })
}


// function checkSelectedPortal(portals) {
//     let inpChecked = 0;
//     for (var i = 0; i < portals.length; i++) {
//         if (inpChecked != 1) {
//             $(button_submit).prop("disabled", true);
//             if ($(portals[i]).is(':checked')) {
//                 inpChecked += 1;
//                 $(button_submit).prop("disabled", false);
//                 $('.right_part > .inp_error').empty();
//             } else {
//                 $(button_submit).prop("disabled", true);
//                 $('.right_part > .inp_error').html(
//                     '<li><i class="fa fa-warning"></i> Нужно что нибудь выбрать!</li>'
//                 )
//             }
//         } return true;
//     }
// }

checkEmptyInput(portal_password);
checkEmptyInput(portal_login);
inputTitleValidation(input_title);
inputUrlValidation(input_url);
disableSubmit();