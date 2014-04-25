function createTimeline(data, reload){
    var reload = typeof reload !== 'undefined' ? reload : false;
    $("#my-timeline").empty();
    createStoryJS({
        type:          'timeline',
        width:         '800',
        height:        '600',
        source:        data,
        embed_id:      'my-timeline',
        start_at_slide:0,
        debug:         true,
    });
}

function getCategories(){
var cat_ids = []
$.each($(".cats:checked"), function(i,v){
        cat_ids.push($(v).val());
    });
return {cat_ids:cat_ids}
}

function loadDataForTimeline(reload){
    var reload = typeof reload !== 'undefined' ? reload : true;
    $.ajax({
       type: "GET",
       data: getCategories(),
       url: "/timeline/get_json",
       dataType:'json',
       success: function(data){
         createTimeline(data, reload);
       }
    });
}
function isCategoriesChecked(){
    var ch = true;
    $.each($('.cats'), function(i, v){ch = ch && $(v).prop('checked')})
    return ch;
}
$(".cats").change(function(){
    loadDataForTimeline();
    if(isCategoriesChecked()){
      $("#chk_check_all").prop('checked', true);
    }else{
      $("#chk_check_all").prop('checked', false);
    }
});

$("#chk_check_all").click(function(){
if(isCategoriesChecked()){
  $(".cats").prop('checked', false);
}else{
  $(".cats").prop('checked', true);
}
loadDataForTimeline(reload=false);
});

loadDataForTimeline(reload=false);
