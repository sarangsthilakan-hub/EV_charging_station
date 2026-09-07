import math


def calculate_charge_cost(start_chg: int, target_chg: int) -> int:
    return (target_chg - start_chg) * 10


def calculate_swap_cost(curr_chg: int, req_chg: int) -> int:
    return ((req_chg - curr_chg) * 10) + 50


def get_charge_discount(units: int, is_repeat: bool) -> int:
    if is_repeat:
        return units
    return 0


def get_swap_discount(cost: int, is_repeat: bool) -> int:
    if is_repeat:
        return math.ceil(cost * 0.15)
    return 0


def find_closest_battery(inventory: dict, req_chg: int) -> str | None:
    valid_batteries = []
    for b_id, data in inventory.items():
        if data["status"] == "Available" and data["charge"] >= req_chg:
            valid_batteries.append((b_id, data["charge"]))

    if not valid_batteries:
        return None

    valid_batteries.sort(key=lambda x: (x[1], x[0]))
    return valid_batteries[0][0]


def format_inventory_line(b_id: str, chg: int, status: str) -> str:
    return f"  {b_id}  {chg:>3}%   {status}"