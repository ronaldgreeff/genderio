const docReady = (fn) => {
  document.readyState === 'complete' || document.readyState === 'interactive' ? setTimeout(fn, 1) : document.addEventListener('DOMContentLoaded', fn);
}

docReady(function() {

  $('#dob').datepicker({
    format: 'dd-mm-yyyy',
  });

});
