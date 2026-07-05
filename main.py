MIN_VAL = 10.0
VARIANT_COEF = 1.07
DEDUCTIBLE_COEF = 1.11
PRODUCT_LEVEL_COEF = 1.20

MAX_ITER = 15

def fix_insurance_prices(prices: dict[str, float]) -> tuple[dict[str, float], list[str]]:

    fixed_prices = prices.copy()
    all_logs = []
    numIter = 0
    while True:
        logs = []

        mtpl_price = fixed_prices.get("mtpl", 0.0)
        min_allowed = MIN_VAL if mtpl_price <= 0.0 else round(PRODUCT_LEVEL_COEF * mtpl_price, 2)

        products = ["limited_casco", "casco"]
        variants = ["compact", "basic", "comfort", "premium"]
        deductibles = [500, 200, 100]

        for key in fixed_prices:
            if key != "mtpl" and fixed_prices[key] <= mtpl_price:
                old_val = fixed_prices[key]
                fixed_prices[key] = min_allowed
                logs.append(f"Uvecan {key} ({old_val} -> {fixed_prices[key]}) jer je bio manji od mtpl")

        deductible_order = [500, 200, 100]
        for prod in products:
            for var in variants:
                for i in range(len(deductible_order) - 1):
                    lower_d = deductible_order[i]
                    higher_d = deductible_order[i + 1]

                    key_lower = f"{prod}_{var}_{lower_d}"
                    key_higher = f"{prod}_{var}_{higher_d}"

                    if key_lower in fixed_prices and key_higher in fixed_prices:
                        if fixed_prices[key_higher] <= fixed_prices[key_lower]:
                            old_val = fixed_prices[key_higher]
                            fixed_prices[key_higher] = round(fixed_prices[key_lower] * DEDUCTIBLE_COEF, 2)
                            logs.append(
                                f"Korigovan {key_higher} ({old_val} -> {fixed_prices[key_higher]}) jer je bio jeftiniji od {key_lower}")

            for d in deductibles:
                key_b = f"{prod}_basic_{d}"
                key_c = f"{prod}_comfort_{d}"
                if key_b in fixed_prices and key_c in fixed_prices:
                    if fixed_prices[key_c] <= fixed_prices[key_b]:
                        old_val = fixed_prices[key_c]
                        fixed_prices[key_c] = round(fixed_prices[key_b] * VARIANT_COEF, 2)
                        logs.append(
                            f"Korigovan {key_c} ({old_val} -> {fixed_prices[key_c]}) - comfort mora biti skuplja od basic.")

                key_b = f"{prod}_compact_{d}"
                if key_b in fixed_prices and key_c in fixed_prices:
                    if fixed_prices[key_c] <= fixed_prices[key_b]:
                        old_val = fixed_prices[key_c]
                        fixed_prices[key_c] = round(fixed_prices[key_b] * VARIANT_COEF, 2)
                        logs.append(
                            f"Korigovan {key_c} ({old_val} -> {fixed_prices[key_c]}) - comfort mora biti skuplja od compact.")


                key_p = f"{prod}_premium_{d}"
                if key_c in fixed_prices and key_p in fixed_prices:
                    if fixed_prices[key_p] <= fixed_prices[key_c]:
                        old_val = fixed_prices[key_p]
                        fixed_prices[key_p] = round(fixed_prices[key_c] * VARIANT_COEF, 2)
                        logs.append(
                            f"Korigovan {key_p} ({old_val} -> {fixed_prices[key_p]}) - premium mora biti skuplji od comfort.")

        for var in variants:
            for d in deductibles:
                l_key = f"limited_casco_{var}_{d}"
                c_key = f"casco_{var}_{d}"

                if l_key in fixed_prices and c_key in fixed_prices:
                    if fixed_prices[c_key] <= fixed_prices[l_key]:
                        old_val = fixed_prices[c_key]
                        fixed_prices[c_key] = round(fixed_prices[l_key] * PRODUCT_LEVEL_COEF, 2)
                        logs.append(
                            f"Korigovan {c_key} ({old_val} -> {fixed_prices[c_key]}) - Casco mora biti skuplji od Limited Casco.")
        if (len(logs) == 0):
            break
        all_logs.extend(logs)
        if(numIter > MAX_ITER):
            print("\n Greska, preveliki broj ponavljanja petlje - povecaj MAX_ITER \n")
            break
        numIter+= 1
        print(f"\nBroj iteracija: {numIter} \n")
    return fixed_prices, all_logs


example_prices = {
    "mtpl": 200,
    "limited_casco_compact_100": 820,
    "limited_casco_compact_200": 760,
    "limited_casco_compact_500": 650,
    "limited_casco_basic_100": 900,
    "limited_casco_basic_200": 780,
    "limited_casco_basic_500": 600,
    "limited_casco_comfort_100": 950,
    "limited_casco_comfort_200": 870,
    "limited_casco_comfort_500": 720,
    "limited_casco_premium_100": 1100,
    "limited_casco_premium_200": 980,
    "limited_casco_premium_500": 800,
    "casco_compact_100": 750,
    "casco_compact_200": 700,
    "casco_compact_500": 620,
    "casco_basic_100": 830,
    "casco_basic_200": 760,
    "casco_basic_500": 650,
    "casco_comfort_100": 900,
    "casco_comfort_200": 820,
    "casco_comfort_500": 720,
    "casco_premium_100": 1050,
    "casco_premium_200": 950,
    "casco_premium_500": 780
}


corrected_data, changes = fix_insurance_prices(example_prices)

print("=== ISPRAVLJENI CENOVNIK ===")
for k, v in corrected_data.items():
    print(f"{k:30} : {v:>8.2f}")

print("\n=== DETEKTOVANE I POPRAVLJENE NEPRAVILNOSTI ===")
for log in changes:
    print(f"• {log}")