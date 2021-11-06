$('#process_html_form').submit(function(event) {
  event.preventDefault();
  if ($("#output_format").val() === 'GraphML'){
    return alertify.error(`${$("#output_format").val()} output format is not supported currently!`);
  }
  this.submit();
  alertify.success(`File Parsed Successfully!`)
  $('#html_file').val(null); // blank the input_file
  
});