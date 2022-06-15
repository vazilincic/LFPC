def mean(a, b, c) {
    var sum = 0
    var count = 0

    if(a > 0 and a < 100) {
        sum = sum + a
        count = count + 1
    }

    if(b > 0 and b < 200) {
        sum = sum + b
        count = count + 1
    }

    if(c > 0 and c < 300) {
        sum = sum + c
        count = count + 1
    }

    if(sum = 0 or count = 0) {
        return 0
    } else {
        return sum / count
    }
}

def main() {
    var a = input()
    var b = input()
    var c = input()

    result = mean(a, b, c)
    print(result)
}
