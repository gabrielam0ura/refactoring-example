import locale

def format_currency(amount):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.currency(amount, grouping=True)

def calculate_amount(play, perf):
    match play["type"]:
            case "tragedy":
                this_amount = 40000
                if perf["audience"] > 30:
                    this_amount += 1000 * (perf["audience"] - 30)
            case "comedy":
                this_amount = 30000
                if perf["audience"] > 20:
                    this_amount += 10000 + 500 * (perf["audience"] - 20)
                this_amount += 300 * perf["audience"]
            case _:
                raise Exception(f"unknown type: ${play['type']}")
    return this_amount

def calculate_volume_credits(play, perf):
    volume_credits = max(perf["audience"] - 30, 0)
    if "comedy" == play["type"]:
        volume_credits += perf["audience"] // 5
    return volume_credits

def format_line(play, perf, this_amount):
    return f"  {play['name']}: {format_currency(this_amount/100)} ({perf['audience']} seats)\n"

def statement(invoice: dict, plays: dict):
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        volume_credits += calculate_volume_credits(play, perf)
        this_amount = calculate_amount(play, perf)

        # print line for this order
        result += format_line(play, perf, this_amount)
        total_amount += this_amount

    result += f"Amount owed is {format_currency(total_amount/100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result
