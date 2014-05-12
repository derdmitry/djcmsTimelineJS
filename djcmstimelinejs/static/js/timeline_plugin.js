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
            debug: true
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
    var start_date = $('#start-date').val();
    var end_date = $('#end-date').val();
    return {cat_ids: cat_ids,
        start_date: start_date,
        end_date: end_date,
        page: window.page ? window.page : 0,
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
            window.page = data.timeline.current_page;
            window.total_page = data.timeline.total_page;
            $('#start-date').val(data.timeline.start_date);
            $('#end-date').val(data.timeline.end_date);
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
        loadDataForTimeline(reload = true);
    });

    loadDataForTimeline(reload = false);
    $("body").on("UPDATE", ".vco-navigation", function () {
        alert("MY!!!!!!!!!!!!!!!!");
    });

//    $(document).on("click", "div.nav-next", function () {
//        if(window.current_marker + 1 ==  window.count_marker){
//            window.page++;
//            $.ajax({
//                type: "GET",
//                data: getCategories(),
//                url: "/timeline/timeline/" + window.timeline_id,
//                dataType: 'json',
//                success: function (data) {
//                    window.data = data;
//                    window.date_count = data.timeline.date_count;
//                    window.page = data.timeline.current_page;
//                    window.total_page = data.timeline.total_page;
//                    storyjs_embedjs.reload(data);
//                    /*
//                    VMM.Timeline.DataObj.getData(data);
//                    window.goToSlide(1, "easeOutExpo", 0, true);
//                    window.goToEvent(1)
//
//                    VMM.Lib.visible("div.nav-next", true);*/
//                }
//            });
//        }
//    });
//    $(document).on("click", "div.nav-previous", function () {
//        if(window.current_marker  ==  1  && window.page > 0){
//            window.page--;
//            $.ajax({
//                type: "GET",
//                data: getCategories(),
//                url: "/timeline/timeline/" + window.timeline_id,
//                dataType: 'json',
//                success: function (data) {
//                    window.data = data;
//                    window.date_count = data.timeline.date_count;
//                    window.page = data.timeline.current_page;
//                    window.total_page = data.timeline.total_page;
//                    storyjs_embedjs.reload(data);
//                    VMM.Timeline.DataObj.getData(data);
//                    window.goToSlide(3, "easeOutExpo", 0, true);
//                    window.goToEvent(3)
//                    VMM.Lib.visible("div.nav-next", true);
//                }
//            });
//        }
//    });
    $("#categories input").checkbox({
        buttonStyle: 'btn-base',
        buttonStyleChecked: 'btn-success',
        checkedClass: 'icon-check',
        uncheckedClass: 'icon-check-empty'
    });

    $('#start-date').datepicker();
    $('#end-date').datepicker();

});
