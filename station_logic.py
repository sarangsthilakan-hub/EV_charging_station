import station_logic


def render_inventory(inventory: dict) -> str:
    lines = [
        "--------------------------------",
        "      EV ENERGY STATION",
        "--------------------------------",
        "",
        "Battery Inventory:"
    ]
    for b_id in sorted(inventory.keys()):
        data = inventory[b_id]
        lines.append(station_logic.format_inventory_line(b_id, data["charge"], data["status"]))
    return "\n".join(lines)


def main() -> None:
    inventory = {
        "B01": {"charge": 100, "status": "Available"},
        "B02": {"charge": 90, "status": "Available"},
        "B03": {"charge": 75, "status": "Available"},
        "B04": {"charge": 60, "status": "Available"},
        "B05": {"charge": 45, "status": "Available"}
    }
    past_customers = set()

    while True:
        print(render_inventory(inventory))
        print()
        print("1. Charge EV")
        print("2. Swap Battery")
        print("3. Exit")
        print()

        choice_str = input("Enter choice: ")

        if choice_str == "3":
            print("Goodbye!")
            break

        elif choice_str == "1":
            while True:
                ev_id = input("EV ID: ")
                if not ev_id.strip():
                    print("Invalid ID.")
                else:
                    break

            while True:
                battery_id = input("Battery ID: ")
                if not battery_id.strip():
                    print("Invalid ID.")
                else:
                    break

            while True:
                start_str = input("Starting charge (%): ")
                try:
                    start_chg = int(start_str)
                    if start_chg < 0 or start_chg > 100:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid charge value.")

            while True:
                target_str = input("Target charge (%): ")
                try:
                    target_chg = int(target_str)
                    if target_chg < 0 or target_chg > 100:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid charge value.")

            if target_chg <= start_chg:
                print("Target must be higher than the starting charge.")
                continue

            units = target_chg - start_chg
            cost = station_logic.calculate_charge_cost(start_chg, target_chg)

            is_repeat = ev_id in past_customers
            discount = station_logic.get_charge_discount(cost, is_repeat)
            total = cost - discount

            past_customers.add(ev_id)

            print()
            print("--------------------------------")
            print("              BILL")
            print("--------------------------------")
            print()
            print(f"{'EV ID:':<20}{ev_id}")
            print(f"{'Battery ID:':<20}{battery_id}")
            print()
            print(f"{'Starting charge:':<20}{start_chg}%")
            print(f"{'Target charge:':<20}{target_chg}%")
            print()
            print(f"{'Energy charged:':<20}{units} units")
            print(f"{'Energy cost:':<20}Rs {cost}")
            print(f"{'Returning discount:':<20}Rs {discount}")
            print("--------------------------------")
            print(f"{'TOTAL:':<20}Rs {total}")
            print("--------------------------------")
            print()

        elif choice_str == "2":
            while True:
                ev_id = input("EV ID: ")
                if not ev_id.strip():
                    print("Invalid ID.")
                else:
                    break

            while True:
                battery_id = input("Battery ID: ")
                if not battery_id.strip():
                    print("Invalid ID.")
                    continue

                # Check is now trapped securely inside the loop
                if battery_id in inventory:
                    print("That battery ID is already in the station inventory.")
                    continue

                break

            while True:
                curr_str = input("Current charge of that battery (%): ")
                try:
                    curr_chg = int(curr_str)
                    if curr_chg < 0 or curr_chg > 100:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid charge value.")

            while True:
                req_str = input("Required charge (%): ")
                try:
                    req_chg = int(req_str)
                    if req_chg < 0 or req_chg > 100:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid charge value.")

            if req_chg <= curr_chg:
                print("Required charge must be higher than your current charge.")
                continue

            new_battery_id = station_logic.find_closest_battery(inventory, req_chg)
            if not new_battery_id:
                print("No battery available for your requirement.")
                continue

            new_chg = inventory[new_battery_id]["charge"]
            cost = station_logic.calculate_swap_cost(curr_chg, req_chg)

            is_repeat = ev_id in past_customers
            discount = station_logic.get_swap_discount(cost, is_repeat)
            total = cost - discount

            past_customers.add(ev_id)

            returned_chg = min(curr_chg + 30, 100)

            for b_id, data in inventory.items():
                if data["status"] == "Returned":
                    data["status"] = "Available"

            del inventory[new_battery_id]
            inventory[battery_id] = {"charge": returned_chg, "status": "Returned"}

            print()
            print("--------------------------------")
            print("          BATTERY SWAP")
            print("--------------------------------")
            print()
            print(f"{'EV ID:':<20}{ev_id}")
            print(f"Old battery: {battery_id} -> {curr_chg}%  (returned at {returned_chg}%)")
            print()
            print(f"New battery: {new_battery_id} -> {new_chg}%")
            print()
            print(f"{'Swap price:':<20}Rs {cost}")
            print(f"{'Returning discount:':<20}Rs {discount}")
            print("--------------------------------")
            print(f"{'TOTAL:':<20}Rs {total}")
            print("--------------------------------")
            print()

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()