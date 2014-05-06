function createTimeline(data, reload) {
    var reload = typeof reload !== 'undefined' ? reload : false;
    if (reload && storyjs_embedjs) {
        storyjs_embedjs.reload(data);
    } else {
        $("#my-timeline").empty();
        createStoryJS({
            type: 'timeline',
            width: '800',
            height: '600',
            source: data,
            embed_id: 'my-timeline',
            start_at_slide: 0,
            debug: true,
        });
        storyjs_embedjs = new VMM.Timeline('my-timeline');
    }
}

function getCategories() {
//return params for ajax request to get timeline
    var cat_ids = []
    $.each($(".cats:checked"), function (i, v) {
        cat_ids.push($(v).val());
    });
    return {cat_ids: cat_ids,
        page: window.page ? window.page : 1,
        count: window.count ? window.count : 3}
}

function loadDataForTimeline(reload) {
    console.log(getCategories());
    var reload = typeof reload !== 'undefined' ? reload : true;
    $.ajax({
        type: "GET",
        data: getCategories(),
        url: "/timeline/timeline/" + window.timeline_id,
        dataType: 'json',
        success: function (data) {
            window.data = data;
            window.date_count = data.timeline.date_count;
            createTimeline(data, reload);
        }
    });
}
function isCategoriesChecked() {
    var ch = true;
    $.each($('.cats'), function (i, v) {
        ch = ch && $(v).prop('checked')
    })
    return ch;
}
function addDateToTimeline() {
    //
    VMM.Timeline.DataObj.getData(x);
}
$(document).ready(function () {
    window.$data = "undefined";
    $(".cats").click(function () {
        loadDataForTimeline(reload = true);
        if (isCategoriesChecked()) {
            $("#chk_check_all").prop('checked', true);
        } else {
            $("#chk_check_all").prop('checked', false);
        }
    });

    $("#chk_check_all").click(function () {
        if (isCategoriesChecked()) {
            $(".cats").prop('checked', false);
            $(".cats").click();
            //$(".cats").checkbox('toggleDisable');
        } else {
            $(".cats").prop('checked', true);
            $(".cats").click();
            //$(".cats").checkbox('toggleEnabled');
        }
        loadDataForTimeline(reload = false);
    });

    loadDataForTimeline(reload = false);
    $("body").on("UPDATE", ".vco-navigation", function () {
        alert("MY!!!!!!!!!!!!!!!!");
    });

    $(document).on("click", "div.nav-next", function () {

    });
    $(document).on("click", "div.nav-prev", function () {

    });
    $("#categories input").checkbox({
        buttonStyle: 'btn-base',
        buttonStyleChecked: 'btn-success',
        checkedClass: 'icon-check',
        uncheckedClass: 'icon-check-empty'
    });
    $("#my-timeline").click(function(){
        if(window.current_marker + 1 ==  window.count_marker){
            window.page++;
            loadDataForTimeline(reload = true);
        }
    });
     window.page = 1;
});
