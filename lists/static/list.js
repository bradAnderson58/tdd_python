window.superlists = {};

window.superlists.updateItems = function(url) {
  $.get(url).done(function(response) {
    var rows = '';
    for (var i = 0; i < response.length; ++i) {
      var item = response[i];
      rows += '\n<tr><td>' + (i+1) + ': ' + item.text + '</td></tr>';
    }
    $('#id_list_table').html(rows);
  })
}

window.superlists.initialize = function(url) {
  $('input[name="text"]').on('keypress', function() {
    $('.has-error').hide();
  });

  if (url) {
    window.superlists.updateItems(url);

    var form = $('#id_item_form');
    form.on('submit', function(event) {
      event.preventDefault();
      $.post(url, {
        'text': form.find('input[name="text"]').val(),
        'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
      }).done(function() {
        window.superlists.updateItems(url);
      });
    });
  }
}
