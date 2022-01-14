from loader import db
from data.config import input_path
from excel.excel import ExcelHandler


def export_models_from_excel_to_db():
    excel = ExcelHandler(input_path)
    for name, price in excel.get_models().items():
        try:
            db.add_model(name, price)
        except ValueError as e:
            print(e)


if __name__ == '__main__':
    try:
        db.get_model("Merrylock 220").update_prices()
    except ValueError as e:
        print(e)

# TODO: Узнать, нужно ли брать цену которой нет на сайте

# def update_products():
#     products = get_products_from_sewing_kingdom()
#     print(3)
#     output = load(products, 'Продукты.xlsx')
#     if output:
#         email = EmailSender(Email.sender, Email.password)
#         email.send(email=Email.receiver,
#                    text="\n".join(output),
#                    title=f"Отчет по \"Швейное королевство\" ({datetime.now().date()})")
#
#
# if __name__ == '__main__':
#     update_products()
#
#     schedule.every().day.do(update_products)
#
#     while True:
#         schedule.run_pending()
#         sleep(60)
