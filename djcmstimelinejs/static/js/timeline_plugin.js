function createTimeline(data, reload){
    var reload = typeof reload !== 'undefined' ? reload : false;
    if(reload && storyjs_embedjs){
          storyjs_embedjs.reload(data);
    }else{
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
    storyjs_embedjs = new VMM.Timeline('my-timeline');
  }
}

function getCategories(){
//return params for ajax request to get timeline
var cat_ids = []
$.each($(".cats:checked"), function(i,v){
        cat_ids.push($(v).val());
    });
return {cat_ids:cat_ids}//, timeline_id:window.timeline_id}
}

function loadDataForTimeline(reload){
  console.log(getCategories());
    var reload = typeof reload !== 'undefined' ? reload : true;
    $.ajax({
       type: "GET",
       data: getCategories(),
       url: "/timeline/timeline/" + window.timeline_id,
       dataType:'json',
       success: function(data){
         window.data = data;
         createTimeline(data, reload);
       }
    });
}
function isCategoriesChecked(){
    var ch = true;
    $.each($('.cats'), function(i, v){ch = ch && $(v).prop('checked')})
    return ch;
}
$(document).ready(function(){
    $(".cats").change(function(){
        loadDataForTimeline(reload=true);
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
    $("body").on("UPDATE", ".vco-navigation", function() {
      alert("MY!!!!!!!!!!!!!!!!");
    });

    $(document).on("click", "div.nav-next", function() {

    });
});
