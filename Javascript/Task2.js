function sumString(str) {
    let numbers = str.split(",");
    let sum = 0;

    for (let num of numbers) {
        sum += Number(num);
    }

    return sum;
}

console.log(sumString("1.5, 2.3, 3.1, 4, 5.5, 6, 7, 8, 9, 10.9"));