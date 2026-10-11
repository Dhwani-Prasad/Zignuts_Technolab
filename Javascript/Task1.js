function sumNumbers(str) {
  let numbers = str.match(/\d/g);
  let sum = 0;

  for (let num of numbers) {
    sum += Number(num);
  }

  return sum;
}

console.log(sumNumbers("foo8bar8cat2tc2"));