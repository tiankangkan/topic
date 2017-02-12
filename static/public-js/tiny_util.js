
/* 浮点数取小数点位数 */
function round_float(number, num_round)
{
    var number_str = number + "";
    return number_str.substr(0, number_str.indexOf(".") + num_round+1);
}

function show_loading(elem_id){
    $('#'+elem_id).show();
}

function hide_loading(elem_id){
    $('#'+elem_id).hide();
}

function scroll_to_elem(elem_id, ms){
    $("html,body").animate({
        scrollTop: $("#"+elem_id).offset().top
    }, ms);
}

function set_page_url(url, page_name) {
    history.pushState({}, page_name || "SNGAPM", url);
}

function open_urls_in_new_tab(bug_urls){
    console.log('open all: ' + bug_urls);
    var bugs = bug_urls.split(";");
    for (var i = 0; i < bugs.length; i ++) {
        var bug = bugs[i];
        var $link = $("<a id='bug_' " + i + " href='" + bug + "' target='_blank'>链接</a>");
        $('body').append($link);
        console.log('open: ' + bug);
        $('#bug_' + i).click();
    }
}