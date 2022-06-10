$(document).ready(function () {
  // using jquery to delete items
  //   when id delete_button clicked ...
  $("#delete_button").click(function () {
    if ($("form").serialize().length != 0) {
      $.ajax({
        type: "POST",
        url: "delete",
        data: $("form").serialize(),
        success: function (data) {
          $("#tasksTable").empty();
          var newhtmlcode = "";
          if (data.length != 0) {
            $.each(data, function (i, item) {
              newhtmlcode += '<tr><td class="checkbox">';
              newhtmlcode += '<form action="/checked" method="post">';
              newhtmlcode += '<input type="checkbox" value="' + data[i]["id"];
              newhtmlcode += '" id="' + data[i]["id"];
              newhtmlcode += '" name="click_task"></form></td>';
              newhtmlcode += "<td>" + data[i]["name"] + "</td>";
              newhtmlcode += "<td>" + data[i]["datetime"] + "</td>";
              newhtmlcode += "<tr>";
            });
          }

          $("#tasksTable").append(newhtmlcode);
        },
      });
    }
  });
});
