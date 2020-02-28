        function getDb() {
            jQuery.ajax({
                type: "GET",
                url: "{% url 'showModels' %}",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                success: function (data) {
                    jQuery("#db").html(data);
                },
                error: function (data) {
                    alert('error');
                    console.log("Error: Ajax call failed.");
                }
            });
        }