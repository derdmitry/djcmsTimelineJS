function createTimeline(data){
    $("#my-timeline").empty();
    createStoryJS({
        type:       'timeline',
        width:      '800',
        height:     '600',
        source:     data,
        embed_id:   'my-timeline',
        debug:      true,
    });
}

function getCategories(){
var cat_ids = []
$.each($(".cats:checked"), function(i,v){
        cat_ids.push($(v).val());
    });
return {cat_ids:cat_ids}
}

function loadDataForTimeline(){
    $.ajax({
       type: "GET",
       data: getCategories(),
       url: "/timeline/get_json",
       dataType:'json',
       success: function(data){
         createTimeline(data);
       }
    });
}

$(".cats").change(function(){
    loadDataForTimeline();
});

loadDataForTimeline();