const docReady = (fn) => {
  document.readyState === 'complete' || document.readyState === 'interactive' ? setTimeout(fn, 1) : document.addEventListener('DOMContentLoaded', fn);
}
docReady(function() {
  // window.addEventListener('DOMContentLoaded', function () {
  var avatar = document.getElementById('avatar');
  var image = document.getElementById('image');
  var input = document.getElementById('input');
  var cropper;

  input.addEventListener('change', function(e) {
    var files = e.target.files;
    var done = function(url) {
      input.value = '';
      image.src = url;
    };
    var reader;
    var file;
    var url;

    if (files && files.length > 0) {
      file = files[0]

      if (URL) {
        done(URL.createObjectURL(file));
      } else if (FileReader) {
        reader = new FileReader();
        reader.onload = function(e) {
          done(reader.result);
        };
        reader.readAsDataURL(file);
      }
      initiate_cropper();
    }
  });

  function initiate_cropper() {
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
    cropper = new Cropper(image, {
      viewMode: 2,
      dragMode: 'move',
      initialAspectRatio: 16 / 9,
      preview: '.preview',
      scalable: false,
      zoomable: false,
      zoomOnTouch: false,
      center: false,
      guides: false,
    });
  };

  // FORM LOGIC
  document.getElementById('predict-button').addEventListener('click', function () {

    var initialAvatarURL;
    var canvas;

    if (cropper) {
      canvas = cropper.getCroppedCanvas()
      initialAvatarURL = avatar.src;
      avatar.src = canvas.toDataURL();
      canvas.toBlob(function(blob) {

        var form = document.forms.namedItem("predict-form");
        var formData = new FormData(form);
        formData.append("image", blob);

        $.ajax('/predict', {
          method: 'POST',
          data: formData,
          processData: false,
          contentType: false,

          success: function (data) {
            console.log(data)
          },

          error: function (xhr, ajaxOptions, thrownError) {
            avatar.src = initialAvatarURL;
            console.log(xhr.status);
            console.log(thrownError);
          },
        });

      });
    }


    // if (cropper) {
    //   canvas = cropper.getCroppedCanvas({
    //     // width: 160,
    //     // height: 160,
    //   });
    //   initialAvatarURL = avatar.src;
    //   avatar.src = canvas.toDataURL();
    //   $alert.removeClass('alert-success alert-warning');
    //   canvas.toBlob(function (blob) {
    //     var formData = new FormData();
    //
    //     formData.append('avatar', blob, 'avatar.jpg');
    //
    //     $.ajax('/predict', {
    //       method: 'POST',
    //       data: formData,
    //       processData: false,
    //       contentType: false,
    //
    //       xhr: function () {
    //         var xhr = new XMLHttpRequest();
    //
    //         xhr.upload.onprogress = function (e) {
    //           var percent = '0';
    //           var percentage = '0%';
    //
    //           if (e.lengthComputable) {
    //             percent = Math.round((e.loaded / e.total) * 100);
    //             percentage = percent + '%';
    //             $progressBar.width(percentage).attr('aria-valuenow', percent).text(percentage);
    //           }
    //         };
    //
    //         return xhr;
    //       },
    //
    //       success: function (data) {
    //         $alert.show().addClass('alert-success').text('Upload success');
    //         console.log(data)
    //       },
    //
    //       error: function (xhr, ajaxOptions, thrownError) {
    //         avatar.src = initialAvatarURL;
    //         $alert.show().addClass('alert-warning').text('Upload error');
    //         console.log(xhr.status);
    //         console.log(thrownError);
    //       },
    //
    //       complete: function () {
    //         $progress.hide();
    //       },
    //     });
    //   });
    // }
  });
});
// });
