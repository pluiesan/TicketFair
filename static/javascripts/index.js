var nowTime = new Date();
const salesPeriod = document.getElementsByClassName('sales-period');
const start = document.getElementsByClassName('start-time');
const end = document.getElementsByClassName('end-time');
const button = document.getElementsByClassName('checkout-button');

for (var i = 0; i < salesPeriod.length; i++) {
  console.log('aaa')
  let startTime = Date.parse(start.item(i).innerText.toString());
  let endTime = Date.parse(end.item(i).innerText.toString());
  if (startTime > nowTime) {
    button.item(i).disabled = true;
    button.item(i).innerText = '販売前です';
    button.item(i).className = 'btn btn-secondary checkout-button';
  } else if (nowTime > endTime) {
    button.item(i).disabled = true;
    button.item(i).innerText = '販売終了しました';
    button.item(i).className = 'btn btn-secondary checkout-button';
  };
};


// $(document).ready(function(event){
//   $(document).on('click', '#bookmark', function (event) {
//         console.log('test')
//         event.preventDefault();
//         $.ajax({
//             type: 'POST',
//             url: "{% url 'bookmark' %}",
//             data: {
//                 'event_id': $(this).attr('name'),
//                 'csrfmiddlewaretoken': '{{ csrf_token }}'
//             },
//             dataType: 'json',
//             success: function(response){
//                 selector = document.getElementsByName(response.event_id);
//                 if(response.bookmarked){
//                     $(selector).html("<i class='fas fa-lg fa-heart'></i>");
//                 }
//                 else {
//                     $(selector).html("<i class='far fa-lg fa-heart'></i>");
//                 }
//                 // selector2 = document.getElementsByName(response.bookmark_id + "-count");
//                 // $(selector2).text(response.count);
//             }
//         });
//     });
// });

console.log('test');
document.on('click', '#bookmark', function (event) {
  console.log('test');
  event.preventDefault();
});
