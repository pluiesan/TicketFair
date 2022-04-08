var nowTime = new Date();
const salesPeriod = document.getElementsByClassName('sales-period');
const start = document.getElementsByClassName('start-time');
const end = document.getElementsByClassName('end-time');
const button = document.getElementsByClassName('checkout-button');

for (var i = 0; i < salesPeriod.length; i++) {
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
}
