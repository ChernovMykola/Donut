// $(document).ready(function() {
//     $('.messages .close').on('click', function() {
//         $(this).parent().fadeOut();
//     });
// });
//
// $('.open-popup').click(function (e){
//     e.preventDefault();
//     $('.popup-bg').fadeIn(600);
// })
//
// $('.close-popup').click(function (){
//     $('.popup-bg').fadeOut(600);
// })
// document.addEventListener('DOMContentLoaded', function() {
//   var closeButtons = document.querySelectorAll('.messages .close');
//   for (var i = 0; i < closeButtons.length; i++) {
//     closeButtons[i].addEventListener('click', function() {
//       this.parentNode.style.display = 'none';
//     });
//   }
//
//   var openPopupButtons = document.querySelectorAll('.open-popup');
//   for (var j = 0; j < openPopupButtons.length; j++) {
//     openPopupButtons[j].addEventListener('click', function(e) {
//       e.preventDefault();
//       document.querySelector('.popup-bg').style.display = 'block';
//     });
//   }
//
//   var closePopupButtons = document.querySelectorAll('.close-popup');
//   for (var k = 0; k < closePopupButtons.length; k++) {
//     closePopupButtons[k].addEventListener('click', function() {
//       document.querySelector('.popup-bg').style.display = 'none';
//     });
//   }
// });
document.addEventListener('DOMContentLoaded', function() {
  var closeButtons = document.querySelectorAll('.messages .close');
  for (var i = 0; i < closeButtons.length; i++) {
    closeButtons[i].addEventListener('click', function() {
      this.parentNode.style.display = 'none';
    });
  }

  var openPopupButtons = document.querySelectorAll('.open-popup');
  for (var j = 0; j < openPopupButtons.length; j++) {
    openPopupButtons[j].addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.popup-bg').style.display = 'block';
    });
  }

  var closePopupButtons = document.querySelectorAll('.close-popup');
  for (var k = 0; k < closePopupButtons.length; k++) {
    closePopupButtons[k].addEventListener('click', function() {
      document.querySelector('.popup-bg').style.display = 'none';
    });
  }
});
