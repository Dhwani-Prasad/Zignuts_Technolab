
function printSeries() {
  let n = Number(document.getElementById("num").value);

  let a = 0;
  let b = 1;
  let result = "";

  for (let i = 0; i < n; i++) {
    result += a + " ";

    let next = a + b;
    a = b;
    b = next;
  }

  document.getElementById("result").innerText = result;
}
