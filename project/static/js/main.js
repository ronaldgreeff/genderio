const docReady = (fn) => {
  document.readyState === 'complete' || document.readyState === 'interactive' ? setTimeout(fn, 1) : document.addEventListener('DOMContentLoaded', fn);
}
docReady(function() {

  var uploadImage = document.getElementById('upload-image');
  var image = document.getElementById('image');
  var input = document.getElementById('input');
  var cropper;

  // FILE UPLOAD LOGIC
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

    var initialImage;
    var canvas;

    if (cropper) {
      canvas = cropper.getCroppedCanvas()
      initialImage = uploadImage.src;
      uploadImage.src = canvas.toDataURL();
      canvas.toBlob(function(blob) {

        var form = document.forms.namedItem("predict-form");
        var formData = new FormData(form);

        formData.append('imageType', blob.type);
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
            uploadImage.src = initialImage;
            console.log(xhr.status);
            console.log(thrownError);
          },
        });

      });
    }
  });
});
// });
