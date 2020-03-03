function makeMark(mark, cell_id) {
    var html = '<div id=mark></div>';
    document.getElementById(cell_id).outerHTML = html.replace('mark', mark);
}

function makePrompt(mark, name) {
    var html = '<span id=mark></span>';
    document.getElementById("prompt_name").innerHTML = name;
    document.getElementById("prompt_mark").innerHTML = html.replace('mark', mark);
}

function makeMoveViaAjax(cell_id) {
    $.ajax({
        type: "POST",
        url: "{% url 'make_move' %}",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}"
        },
        data: {
            "cell_id": cell_id
        },
        dataType: 'json',
        success: function (data) {
            makeMark(data.current_player["mark"], cell_id);

            if (data.result) {
                window.location.href = "{% url 'game_over' %}";
            } else {
                makePrompt(data.next_player["mark"], data.next_player["name"]);
            }
        },
        error: function (data) {
            alert("Error response:\n" + data);
        }
    });
}
