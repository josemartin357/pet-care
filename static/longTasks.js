$(document).ready(function () {
  $("#delete_button").click(function () {
    if ($("form").serialize().length != 0) {
      $.ajax({
        type: "POST",
        url: "delete_long_task",
        data: $("form").serialize(),
        success: function (data) {
          $("#longTasksTable").empty();

          var newLongTaskshtml = "";
          if (data.length != 0) {
            $.each(data, function (i, item) {
              newLongTaskshtml +=
                '<tr><td class="checkbox"><form action="/checked" method="post"><input type="checkbox" value="' +
                data[i]["id"] +
                '" id="' +
                data[i]["id"] +
                '" name="click_longTask"></form></td>';
              newLongTaskshtml += "<td>" + data[i]["name"] + "</td>";
              newLongTaskshtml += "<td>" + data[i]["datetime"] + "</td>";
              newLongTaskshtml += "</tr>";
            });
          }
          $("#longTasksTable").append(newLongTaskshtml);
        },
      });
    }
  });
});
