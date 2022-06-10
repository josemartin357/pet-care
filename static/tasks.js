// using jquery to manipulate state at items
// source: https://learn.jquery.com/using-jquery-core/document-ready/
$(document).ready(function () {
  // using jquery to delete items
  //   when id delete_button clicked ...
  $("#delete_button").click(function () {
    // using serialize() from jquery to identify if there is data in form
    // then we make an ajax request to /delete
    if ($("form").serialize().length != 0) {
      $.ajax({
        type: "POST",
        url: "delete",
        data: $("form").serialize(),
        // we use the success callback hook to run function that empties body from index.html
        success: function (data) {
          $("#tasksTable").empty();
          // initial empty field to replace tbody in index.html
          var newhtmlcode = "";
          // if there is data ...
          if (data.length != 0) {
            // we run function that fills newhtmlcode with data
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
          //   appending table body with new html code
          $("#tasksTable").append(newhtmlcode);
        },
      });
    }
  });

  // COMPLETED ITEMS
  $("#accomplished_button").click(function () {
    if ($("form").serialize().length != 0) {
      $.ajax({
        type: "POST",
        url: "move_task",
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
          //   append
          $("#tasksTable").append(newhtmlcode);
        },
      });
    }
  });
});
