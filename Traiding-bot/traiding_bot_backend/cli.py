from basic_bot import BasicBot

def main():
    bot = BasicBot()

    while True:
        print("\n=== Trading Menu ===")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Exit")
        
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            symbol = input("Symbol (e.g., BTCUSDT): ").upper()
            side = input("BUY or SELL: ").upper()
            qty = float(input("Quantity: "))

            try:
                result = bot.market_order(symbol, side, qty)
                print("\nOrder Executed:")
                print(result)
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            symbol = input("Symbol (e.g., BTCUSDT): ").upper()
            side = input("BUY or SELL: ").upper()
            qty = float(input("Quantity: "))
            price = float(input("Limit Price: "))

            try:
                result = bot.limit_order(symbol, side, qty, price)
                print("\nLimit Order Placed:")
                print(result)
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            print("Exiting…")
            break

        else:
            print("Invalid option. Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
