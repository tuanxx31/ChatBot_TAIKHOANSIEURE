from collections import defaultdict

def format_grouped_product_packages(packages):
    grouped = defaultdict(list)
    for p in packages:
        grouped[p["product_name"]].append(p)

    if not grouped:
        return "Không tìm thấy gói nào phù hợp với yêu cầu."

    response = []
    for product_name, gói_list in grouped.items():
        response.append(f"{product_name} hiện có {len(gói_list)} gói:")
        for p in gói_list:
            price = float(p["price"])
            discount = float(p["discountPrice"])
            percent = round((1 - discount / price) * 100) if discount < price else 0
            stock_note = "" if str(p["stock"]).lower() == "true" else " (hết hàng)"
            gói_tên = p["name"].replace(product_name, "").strip()
            response.append(f"- {gói_tên}: {price:,.0f}đ → {discount:,.0f}đ (giảm {percent}%)" + stock_note)
        response.append("")  # tách nhóm
    return "\n".join(response)
