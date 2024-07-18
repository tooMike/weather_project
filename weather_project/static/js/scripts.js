// static/your_app/js/scripts.js

// Функция для отправки формы по названию города
function submitCityForm(cityName) {
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        if (form.city_name && form.city_name.value === cityName) {
            form.submit();
        }
    });
}

$(function() {
    var cityInput = $("#id_city_name");
    var autoCompleteUrl = cityInput.data('autocomplete-url');

    // Очищаем скрытые поля при изменении значения в поле города
    cityInput.on('input', function() {
        $("#id_latitude").val('');
        $("#id_longitude").val('');
    });

    cityInput.autocomplete({
        source: function(request, response) {
            $.ajax({
                url: autoCompleteUrl,
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.city_name + ', ' + item.country,
                            value: item.city_name,
                            latitude: item.latitude,
                            longitude: item.longitude
                        };
                    }));
                }
            });
        },
        minLength: 2,
        select: function(event, ui) {
            $("#id_latitude").val(ui.item.latitude);
            $("#id_longitude").val(ui.item.longitude);
        }
    });
});
