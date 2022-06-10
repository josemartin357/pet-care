// using jquery to manipulate state of items
// source: https://learn.jquery.com/using-jquery-core/document-ready/

$(document).ready(function () {
  // using jquery to delete items
  //   when id delete_button clicked ...
  $("#delete_button").click(function () {
    // using serialize() from jquery to identify if there is data in form
    // source: https://www.w3schools.com/jquery/ajax_serialize.asp
    // then we make an ajax request to /delete_long_task
    if ($("form").serialize().length != 0) {
      $.ajax({
        type: "POST",
        url: "delete_long_task",
        data: $("form").serialize(),
        // we use the success callback hook to run function that empties body from goals.html
        success: function (data) {
          $("#longTasksTable").empty();
          // initial empty field to replace table body in html
          var newLongTaskshtml = "";
          // if there is data ...
          if (data.length != 0) {
            // we run function that fills newLongTaskhtml with existing data
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
          //   appending table body with new html code
          $("#longTasksTable").append(newLongTaskshtml);
        },
      });
    }
  });
});
