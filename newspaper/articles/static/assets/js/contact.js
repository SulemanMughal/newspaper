$(document).ready(function () {
  (function ($) {
    "use strict";

    jQuery.validator.addMethod(
      "answercheck",
      function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value);
      },
      "type the correct answer -_-"
    );

    $(function () {
      $("#contactForm").validate({
        rules: {
          message: {
            required: true,
            minlength: 20,
          },
        },
        messages: {
          message: {
            required: "um...yea, you have to write something to comment .",
            minlength: "thats all? really?",
          },
        },
        submitHandler: function (form) {
          $.ajaxSetup({
            beforeSend: function (xhr, settings) {
              xhr.setRequestHeader(
                "X-CSRFToken",
                $('input[name="csrfmiddlewaretoken"]').val()
              );
            },
          });
          $(form).ajaxSubmit({
            type: "POST",
            data: $(form),
            url: $(form).attr("action"),
            success: function () {
              $("#contactForm :input").attr("disabled", "disabled");
              $("#contactForm").fadeTo("slow", 1, function () {
                $(this).find(":input").attr("disabled", "disabled");
                $(this).find("label").css("cursor", "default");
                $("#success").fadeIn();
                $(".modal").modal("hide");
                $("#success").modal("show");
              });
            },
            error: function (response) {
              alert(response.responseJSON.error);
              $("#contactForm").fadeTo("slow", 1, function () {
                $("#error").fadeIn();
                $(".modal").modal("hide");
                $("#error").modal("show");
              });
            },
          });
        },
      });
    });
  })(jQuery);
});
