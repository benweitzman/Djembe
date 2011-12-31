jQuery.fn.nextUntil = function(selector) {
    iter = this.next();
    while (iter && !iter.is(selector)) {
        iter = iter.next();
    }
    return iter;
}
for (i=0;i<$(".multitext").length;i++) {
    multi = $(".multitext")[i]
    $(multi).data("choices",$.parseJSON($(multi).children(".choices").val()))
    console.log($(multi).data("choices"));
    map = {};
    artists = []
    choices = $(multi).data("choices")
    for (key in choices) {
        if (map[choices[key]] == undefined) {
            map[choices[key]] = [parseInt(key)];
            artists.push(choices[key]);
        } else {
            map[choices[key]].push(parseInt(key))
        }
    }
    console.log(map);
    console.log(artists);
    $(multi).children('.remove').click(function(e) {
        console.log($(multi).children("input[type='text']"));
        if ($(multi).children('input[type="text"]').length>1) {
            $(multi).children('br:last-child').remove();
            $(multi).children('input[type="hidden"]:last-child').remove()
            $(multi).children('select:last-child').remove();
            $(multi).children('input[type="text"]:last-child').remove();
        }
        return false;
    });
    $(multi).children('.add').click(function (e) {
        newInput = document.createElement("input");
        newInput.type = "text";
        newHidden = document.createElement("input");
        newHidden.type = "hidden";
        newHidden.name = $(multi).attr("value")
        newInput.secret = newHidden;
        br = document.createElement("br");
        $(multi).append(newInput).append(newHidden).append(br);
        $(multi).children("input[type='text']").unbind('change');
        $(multi).children("input[type='text']").bind('change keyup',function (e) {
            v = $(e.target).val();
            ids = map[v];
            if (ids && ids.length>1) {
                if ($(e.target).next()[0].tagName!="SELECT") {
                select = document.createElement("select");
                select.className =" mini"
                for (j=0;j<ids.length;j++) {
                    select.innerHTML += "<option>"+ids[j]+"</option>";
                }
                $(select).insertAfter($(e.target));
                $(select).change(function (q) {
                    console.log($(q.target).next("input"))
                    console.log($(q.target).next("input[type='hidden']"))
                    $(q.target).next("input[type='hidden']").val($(q.target).val());
                });

            }
            } else {
                console.log($(e.target).next()[0].tagName)
                if ($(e.target).next()[0].tagName=="SELECT") {
                    $(e.target).next().remove();
                    $(e.target).next("input[type='hidden']").val(undefined)
                }
            }
        });

        return false;
    });
    form = $(multi).parents("form:first");
    $(form).submit(function(e) {
        inputs = $(multi).children("input[type='text']");
        //console.log(inputs)
        for (j=0;j<inputs.length;j++) {
            //console.log($(inputs[j]).nextUntil("input"))
            if (!$(inputs[j]).nextUntil("input[type='hidden']").val()) {
                $(inputs[j]).nextUntil("input[type='hidden']").val(map[$(inputs[j]).val()][0]);
            }
        }
       //return false;

    });

}