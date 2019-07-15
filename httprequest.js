var socket = io.connect('http://cd5de449.ngrok.io');

socket.on( 'connect', function() {
  socket.emit( 'my event', {
    data: 'User Connected'
  })
  var form = $( 'form' ).on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = $('input.name').val();
    let user_email = $('input.email').val();
    let user_password = $('input.password').val();
    socket.emit( 'json', {
      name : user_name,
      email : user_email,
      password: user_password
    })
  })
})

socket.on('after connect', function(msg){
    console.log('After connect', msg);
});

socket.on( 'my response', function( msg ) {
    console.log( msg );
})
