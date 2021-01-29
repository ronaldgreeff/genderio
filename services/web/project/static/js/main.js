const docReady = (fn) => {
  document.readyState === 'complete' || document.readyState === 'interactive' ? setTimeout(fn, 1) : document.addEventListener('DOMContentLoaded', fn);
}

docReady(function() {

  $('.pickdate').datepicker({
    format: 'dd-mm-yyyy',
  });

});
